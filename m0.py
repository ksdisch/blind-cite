"""m0.py — Milestone 0 (fit-pilot) verdict script. docs/M0-BRIEF.md is the
pre-commitment this file implements; the D7 triggers and D8 caps are code here,
not judgment calls later.

Subcommands (free ones never touch the network except `ping`):
  ping      verify roster slugs + pinned prices against live OpenRouter
  fidelity  detector-fidelity gate on data/handlabeled.json (must be 16/16)
  gen-docs  draft + mechanically verify the frozen doc set   (paid, cap $0.10)
  smoke     N=5 x roster x worst cell, measured cost/trial    (paid, cap $0.05)
  pilot     12 pairs x 4 cells x roster                       (paid, cap $0.45)
  verdict   apply D7 triggers to pilot data, render FIT/NO-FIT
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

from assemble import CELLS, assemble, cell_id
import corpus as _corpus
from corpus import N_PAIRS_M0, load_corpus
from detectors import classify, verify_doc
from prompts import evidence_doc_prompt, null_doc_prompt, trial_prompt
from stats import wilson

DATA = Path(__file__).parent / "data"
DOCS_PATH = DATA / "docs.json"
GEN_LOG_PATH = DATA / "gen_log.json"
SMOKE_PATH = DATA / "smoke.jsonl"
PILOT_PATH = DATA / "pilot.jsonl"
VERDICT_PATH = DATA / "m0_verdict.json"

CAP_GEN_DOCS = 0.10  # D8
CAP_SMOKE = 0.05
CAP_PILOT = 0.45
N_CLEAN_TARGET = 20  # KICKOFF: N>=20 clean per gated cell per model


# --- free gates --------------------------------------------------------------

def run_fidelity() -> tuple[int, int, list[str]]:
    hl = json.loads((DATA / "handlabeled.json").read_text())
    pair, docs_bank = hl["pair"], hl["docs"]
    failures = []
    for case in hl["cases"]:
        docs = [{"doc_id": f"doc{i + 1}", "text": docs_bank[k]}
                for i, k in enumerate(case["docs"])]
        got = classify(case["answer"], pair, docs)
        for key, want in case["expect"].items():
            if got[key] != want:
                failures.append(
                    f"{case['id']}: {key} = {got[key]!r}, expected {want!r}")
    n = len(hl["cases"])
    return n - len({f.split(':')[0] for f in failures}), n, failures


def cmd_fidelity(_args) -> int:
    ok, n, failures = run_fidelity()
    for f in failures:
        print(f"  MISS {f}")
    print(f"detector fidelity: {ok}/{n}")
    return 0 if ok == n else 1


def cmd_ping(_args) -> int:
    from client import ping_models
    problems = ping_models()
    for p in problems:
        print(f"  {p}")
    print("ping: clean" if not problems else
          f"ping: {len(problems)} problem(s) — resolve before spending")
    return 0 if not problems else 1


# --- paid waves ---------------------------------------------------------------

def cmd_gen_docs(args) -> int:
    from client import GENERATOR, GENERATOR_TEMPERATURE, BudgetExceeded, CostMeter, chat
    # This command writes the SHARED evidence bank, and it writes a dict it
    # builds from scratch. Once the corpus grew past M0's 12 that became a
    # truncating write: it would replace an 80-pair data/docs.json with 12
    # freshly sampled pairs, deleting the evidence every later milestone's
    # committed logs re-verify against — and it would do so even on the
    # BudgetExceeded path, since the writes sit outside the try. The verdict
    # writers got this guard in the same commit; this one is the write that
    # deletes evidence rather than merely restating it (PR #12 review F6).
    if _corpus.N_PAIRS != N_PAIRS_M0:
        raise SystemExit(
            f"HALT: corpus.N_PAIRS is {_corpus.N_PAIRS}, not M0's "
            f"{N_PAIRS_M0}. `m0.py gen-docs` rebuilds data/docs.json from "
            f"scratch and would truncate the shared {_corpus.N_PAIRS}-pair "
            f"bank to {N_PAIRS_M0}. Later milestones generate incrementally "
            f"(`m1.py gen-docs`, `m1c.py gen-docs`); use those.")
    corpus = load_corpus()
    meter = CostMeter(CAP_GEN_DOCS)
    docs: dict = {}
    log: list[dict] = []
    incomplete = []
    try:
        for pair in corpus["pairs"][:N_PAIRS_M0]:
            jobs = [
                ("x", evidence_doc_prompt(pair["x"], pair["theme"])),
                ("y_completing", evidence_doc_prompt(pair["y"], pair["theme"])),
                ("y_null", null_doc_prompt(pair["y"])),
            ]
            entry = {}
            for doc_type, prompt in jobs:
                accepted = None
                for attempt in range(1, 4):
                    resp = chat(GENERATOR, prompt, max_tokens=450,
                                temperature=GENERATOR_TEMPERATURE, meter=meter)
                    text = resp["text"].strip()
                    violations = verify_doc(text, doc_type, pair)
                    log.append({"pair_id": pair["pair_id"], "doc_type": doc_type,
                                "attempt": attempt, "violations": violations,
                                "cost": resp["cost"]})
                    if not violations:
                        accepted = text
                        break
                if accepted is None:
                    incomplete.append((pair["pair_id"], doc_type))
                else:
                    entry[doc_type] = accepted
            docs[pair["pair_id"]] = entry
    except BudgetExceeded as e:
        print(f"HALT: {e}")
    rejected = sum(1 for row in log if row["violations"])
    rate = rejected / len(log) if log else 0.0
    summary = {"attempts": len(log), "rejected_attempts": rejected,
               "rejection_rate": round(rate, 3),
               "incomplete": [list(t) for t in incomplete],
               "cost": round(meter.total, 4), "generator": GENERATOR}
    DOCS_PATH.write_text(json.dumps(docs, indent=2) + "\n")
    GEN_LOG_PATH.write_text(json.dumps(
        {"summary": summary, "attempts": log}, indent=2) + "\n")
    print(f"gen-docs: {len(log)} attempts, rejection rate {rate:.1%}, "
          f"cost ${meter.total:.4f}")
    if incomplete:
        print(f"  INCOMPLETE after 3 attempts: {incomplete}")
    print(f"  D7 generator-viability trigger (>60%): "
          f"{'TRIPPED' if rate > 0.6 else 'ok'}")
    return 1 if incomplete or rate > 0.6 else 0


def _run_trial(model, pair, cx, cy, docs_for_pair, meter):
    from client import chat
    docs = assemble(pair, cx, cy, docs_for_pair)
    prompt = trial_prompt(pair["question"], docs)
    row = {"pair_id": pair["pair_id"], "cell": cell_id(cx, cy), "model": model}
    try:
        resp = chat(model, prompt, meter=meter)
    except Exception as e:  # noqa: BLE001 — error rows feed the K3 trigger
        row.update(ok=False, error=f"{type(e).__name__}: {e}")
        return row
    row.update(ok=True, answer=resp["text"], cost=resp["cost"],
               prompt_tokens=resp["prompt_tokens"],
               completion_tokens=resp["completion_tokens"],
               finish_reason=resp["finish_reason"],
               **{"scored": classify(resp["text"], pair, docs)})
    return row


def _models(args):
    from client import ROSTER
    return args.models.split(",") if args.models else ROSTER


def cmd_smoke(args) -> int:
    from client import BudgetExceeded, CostMeter
    corpus = load_corpus()
    docs_all = json.loads(DOCS_PATH.read_text())
    meter = CostMeter(CAP_SMOKE)
    rows = []
    try:
        for model in _models(args):
            for pair in corpus["pairs"][:5]:
                rows.append(_run_trial(model, pair, "complete", "completing",
                                       docs_all[pair["pair_id"]], meter))
    except BudgetExceeded as e:
        print(f"HALT: {e}")
    SMOKE_PATH.write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n" if rows else "")
    ok_rows = [r for r in rows if r.get("ok")]
    for model in {r["model"] for r in rows}:
        mine = [r for r in ok_rows if r["model"] == model]
        labels = Counter(r["scored"]["label"] for r in mine)
        cost = sum(r["cost"] for r in mine) / len(mine) if mine else float("nan")
        print(f"{model}: {len(mine)} ok, labels {dict(labels)}, "
              f"${cost:.5f}/trial")
    if ok_rows:
        mean_cost = sum(r["cost"] for r in ok_rows) / len(ok_rows)
        n_pilot = N_PAIRS_M0 * len(CELLS) * 3
        projected = mean_cost * n_pilot
        print(f"projected pilot ({n_pilot} trials, worst-cell rate): "
              f"${projected:.3f} vs cap ${CAP_PILOT} — "
              f"{'GO' if projected < CAP_PILOT else 'NO-GO'}")
    print(f"smoke cost: ${meter.total:.4f}")
    return 0


def cmd_pilot(args) -> int:
    from client import BudgetExceeded, CostMeter
    corpus = load_corpus()
    docs_all = json.loads(DOCS_PATH.read_text())
    done = set()
    if PILOT_PATH.exists():
        for line in PILOT_PATH.read_text().splitlines():
            r = json.loads(line)
            if r.get("ok"):
                done.add((r["pair_id"], r["cell"], r["model"]))
    meter = CostMeter(CAP_PILOT)
    n_new = 0
    with PILOT_PATH.open("a") as fh:
        try:
            for model in _models(args):
                for pair in corpus["pairs"][:N_PAIRS_M0]:
                    for cx, cy in CELLS:
                        if (pair["pair_id"], cell_id(cx, cy), model) in done:
                            continue
                        row = _run_trial(model, pair, cx, cy,
                                         docs_all[pair["pair_id"]], meter)
                        fh.write(json.dumps(row) + "\n")
                        fh.flush()
                        n_new += 1
        except BudgetExceeded as e:
            print(f"HALT: {e}")
    print(f"pilot: {n_new} new trials (skipped {len(done)} done), "
          f"cost ${meter.total:.4f}")
    return 0


# --- verdict (pure logic kept importable for test_m0.py) ----------------------

def funnel(rows: list[dict]) -> dict:
    """Per-model funnel over pilot rows. Needs keys: model, cell, ok, and for
    ok rows scored.label / scored.grounded."""
    out: dict = {}
    for r in rows:
        m = out.setdefault(r["model"], {
            "n": 0, "n_err": 0, "vague": 0,
            "cells": {cell_id(*c): Counter() for c in CELLS},
            "grounded_complete_null": [0, 0], "engaged_absent_completing": [0, 0]})
        m["n"] += 1
        if not r.get("ok"):
            m["n_err"] += 1
            continue
        label = r["scored"]["label"]
        m["cells"][r["cell"]][label] += 1
        if label == "vague":
            m["vague"] += 1
        if r["cell"] == "completexnull_control":
            m["grounded_complete_null"][1] += 1
            m["grounded_complete_null"][0] += bool(r["scored"]["grounded"])
        if r["cell"] == "absentxcompleting":
            m["engaged_absent_completing"][1] += 1
            m["engaged_absent_completing"][0] += label in ("DG", "discriminated")
    return out


def apply_triggers(model_funnel: dict) -> dict:
    """D7 kill/swap triggers, mechanically. Returns per-model verdicts."""
    verdicts = {}
    for model, f in model_funnel.items():
        n_ok = f["n"] - f["n_err"]
        g_k, g_n = f["grounded_complete_null"]
        kills, flags = [], []
        if g_k < 6:
            kills.append(f"K1 capability cliff: grounding {g_k}/{g_n} at "
                         f"complete x null_control (< 6)")
        if n_ok > 0 and f["vague"] * 2 >= n_ok:
            kills.append(f"K2 parseability: vague {f['vague']}/{n_ok} (>= 1/2)")
        if f["n"] > 0 and f["n_err"] / f["n"] > 0.2:
            kills.append(f"K3 API health: {f['n_err']}/{f['n']} errors (> 20%)")
        ac = f["cells"]["absentxcompleting"]
        right_reason = ac["correct-refusal"] + ac["discriminated"]
        if not kills and g_k >= 6 and right_reason >= 10:
            flags.append(f"K4 competence ceiling: robust-low-DG (right reason) "
                         f"— refuses/discriminates {right_reason}/12 at the "
                         f"adversarial cell")
        verdicts[model] = {"survives": not kills, "kills": kills, "flags": flags}
    return verdicts


def m1_sizing(model_funnel: dict, survivors: list[str]) -> dict:
    """Corpus size for M1 (clean N>=20/cell/model), computed from the measured
    funnel — never guessed (KICKOFF open-q 3). Clean = ok and not vague."""
    sizing = {}
    for model in survivors:
        f = model_funnel[model]
        per_cell = {}
        for cell in ("absentxnull_control", "absentxcompleting"):
            c = f["cells"][cell]
            n_cell = sum(c.values())
            clean = n_cell - c["vague"]
            rate = clean / n_cell if n_cell else 0.0
            per_cell[cell] = (math.ceil(N_CLEAN_TARGET / rate)
                              if rate > 0 else None)
        sizing[model] = per_cell
    needs = [v for per in sizing.values() for v in per.values()]
    sizing["pairs_needed"] = max((v for v in needs if v), default=None)
    return sizing


def cmd_verdict(_args) -> int:
    # Same guard as m1.py's, same reason (PR #12 review F2): run_fidelity's
    # inputs scale with the shared pool, so once the corpus grows past M0's 12
    # this file would be rewritten with counts M0 never measured.
    if _corpus.N_PAIRS != N_PAIRS_M0:
        raise SystemExit(
            f"HALT: corpus.N_PAIRS is {_corpus.N_PAIRS}, not M0's {N_PAIRS_M0}. "
            f"M0's verdict cannot be re-rendered against a grown corpus. "
            f"data/m0_verdict.json stands as the record; read it, do not "
            f"regenerate it.")
    rows = [json.loads(line) for line in PILOT_PATH.read_text().splitlines()]
    fid_ok, fid_n, _ = run_fidelity()
    gen = json.loads(GEN_LOG_PATH.read_text())["summary"]
    f = funnel(rows)
    verdicts = apply_triggers(f)
    survivors = [m for m, v in verdicts.items() if v["survives"]]
    sizing = m1_sizing(f, survivors)

    print("=== M0 verdict (docs/M0-BRIEF.md D7/exit criteria) ===")
    print(f"fidelity gate: {fid_ok}/{fid_n} "
          f"{'PASS' if fid_ok == fid_n else 'FAIL'}")
    print(f"generator rejection rate: {gen['rejection_rate']:.1%} "
          f"{'PASS' if gen['rejection_rate'] <= 0.6 else 'FAIL'} "
          f"(cost ${gen['cost']:.4f})")
    for model, v in verdicts.items():
        fm = f[model]
        g_k, g_n = fm["grounded_complete_null"]
        e_k, e_n = fm["engaged_absent_completing"]
        lo, hi = wilson(g_k, g_n)
        print(f"\n{model}: {'SURVIVES' if v['survives'] else 'KILLED'}")
        print(f"  grounding complete x null: {g_k}/{g_n} "
              f"(Wilson 95% [{lo:.2f}, {hi:.2f}])")
        print(f"  engagement absent x completing (DG+discriminated): {e_k}/{e_n}")
        for cell, counts in fm["cells"].items():
            print(f"  {cell}: {dict(counts)}")
        for k in v["kills"]:
            print(f"  KILL {k}")
        for fl in v["flags"]:
            print(f"  FLAG {fl}")
    fit = (fid_ok == fid_n and gen["rejection_rate"] <= 0.6
           and len(survivors) >= 2)
    print(f"\nsurvivors: {survivors}")
    print(f"M1 sizing (clean N>={N_CLEAN_TARGET}/cell/model): "
          f"{sizing.get('pairs_needed')} pairs")
    print(f"\nM0: {'FIT' if fit else 'NO-FIT'}"
          + ("" if len(survivors) >= 2 else
             " — roster floor: promote bench (client.BENCH order) and rerun "
             "pilot with --models"))
    VERDICT_PATH.write_text(json.dumps({
        "fit": fit, "fidelity": [fid_ok, fid_n],
        "generator_rejection_rate": gen["rejection_rate"],
        "verdicts": verdicts, "survivors": survivors, "m1_sizing": sizing,
        "funnel": {m: {**v, "cells": {c: dict(k) for c, k in v["cells"].items()}}
                   for m, v in f.items()},
    }, indent=2) + "\n")
    print(f"wrote {VERDICT_PATH}")
    return 0 if fit else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in [("ping", cmd_ping), ("fidelity", cmd_fidelity),
                     ("gen-docs", cmd_gen_docs), ("smoke", cmd_smoke),
                     ("pilot", cmd_pilot), ("verdict", cmd_verdict)]:
        p = sub.add_parser(name)
        if name in ("smoke", "pilot"):
            p.add_argument("--models", default=None,
                           help="comma-separated slugs (default: client.ROSTER)")
        p.set_defaults(fn=fn)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
