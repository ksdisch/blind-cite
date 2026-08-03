"""m1.py — Milestone 1 (DG exists + the blindness contrast) verdict script.

docs/M1-BRIEF.md is the pre-commitment this file implements; D5 resolved to
**Option C** (Decisions.md D6), so M1 runs as TWO labeled arms at the same 20
pairs, sequenced, with surface as a measured factor:

  arm a — M1a, the STARK surface: KICKOFF M1 + M0-BRIEF D3-D6 verbatim, scaled
          to 20 pairs. The pre-commitment executes untouched. Single Y-doc,
          entity-name-forward title, prose rendering.
  arm b — M1b, the CAMOUFLAGE surface (explicitly labeled, argued in the brief
          and decided at a gate BEFORE any spend): JSON tool-result rendering,
          one constant title for every doc, k=4 off-theme filler docs, and the
          misattributed-other/confabulation detector split those fillers make
          mandatory.

Everything gated is code here, not judgment later:

  * primary gate, both arms — Newcombe interval on the DG-Y rate difference
    (absent x completing MINUS absent x null_control) must exclude 0 with a
    positive difference. DG-Y (>=1 Y-owned token, Y's name absent) is the
    paper-analog measure and the only measure that gates.
  * power — N >= 20 CLEAN trials (ok and not vague) in EVERY gated cell for a
    model, else that model auto-reports UNDERPOWERED. No exceptions, no
    borrowing across cells.
  * flagship blindness contrast — on DG-positive answers, the mechanical
    faithfulness and citation proxies are reported PASS/FAIL. That table is the
    artifact M1 exists to render.
  * DG-any (third-party filler evidence pulled into the X-answer) is
    DESCRIPTIVE and never enters the gate: fillers are identical across the two
    cells, so the contrast cannot be attributed to them.

Structural honesty note, carried from the brief so the gate is not oversold: at
absent x null_control the Y-null doc contains zero token-shaped strings, so
DG-Y is impossible by construction in the control cell. The Newcombe delta is
therefore effectively a one-sample test of DG(completing) > 0, and the control's
job is hygiene (refusal behaviour + detector false-positive floor). Under arm b
the fillers additionally make the control a live measure of indiscriminate
grabbing, read via DG-any, descriptively.

Subcommands (free ones never touch the network except `ping`):
  ping      verify roster slugs + pinned prices against live OpenRouter
  fidelity  detector-fidelity gate: M0's 16 + the M1 extension + render traps
  dryrun    render the gate on SYNTHETIC answers — no network, no spend
  gen-docs  generate ONLY missing pairs' docs (p13-p20)     (paid, cap $0.15)
  smoke     N=5 x roster x worst cell, measured cost/trial   (paid, cap $0.05)
  wave      2 cells x 20 pairs x roster, resumable + top-up  (paid, cap per arm)
  verdict   apply the gates to wave data, render the verdict
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from assemble import (CONSTANT_TITLE, K_FILLER, assemble, assemble_camouflaged,
                      cell_id, filler_pair_ids)
from corpus import CORPUS_M0_PATH, N_PAIRS, N_PAIRS_M0, load_corpus, owner_map
from detectors import classify, verify_doc
from prompts import (camouflaged_trial_prompt, evidence_doc_prompt,
                     null_doc_prompt, trial_prompt)
from stats import excludes_zero, newcombe_diff, wilson

DATA = Path(__file__).parent / "data"
DOCS_PATH = DATA / "docs.json"
DOCS_M0_PATH = DATA / "docs_m0.json"
GEN_LOG_M0_PATH = DATA / "gen_log_m0.json"
GEN_LOG_M1_PATH = DATA / "gen_log_m1.json"
HANDLABELED_M0 = DATA / "handlabeled.json"
HANDLABELED_M1 = DATA / "handlabeled_m1.json"

# M1-BRIEF D4 budget caps. gen-docs is shared by both arms; smoke and wave are
# per arm.
CAP_GEN_DOCS = 0.15
CAP_SMOKE = 0.05
CAP_WAVE = {"a": 0.10, "b": 0.15}

# D4's table states a $0.45 M1 total. Note its rows only sum to $0.45 if the
# smoke row is counted once, while the row itself reads "per arm" — so the sum
# of per-wave caps is $0.50 and cannot by itself hold the stated ceiling. The
# ceiling is what was pre-committed, so it is enforced directly, against
# MEASURED spend accumulated across every paid subcommand (data/m1_spend.json).
# Each wave therefore runs under min(its own cap, what is left of the $0.45).
CAP_M1_TOTAL = 0.45
SPEND_PATH = DATA / "m1_spend.json"

# The two gated cells. Cx is held at `absent` throughout M1; Cy is the
# manipulation. complete-Cx cells belong to M2.
M1_CELLS = [("absent", "null_control"), ("absent", "completing")]
BASE_CELL = cell_id("absent", "null_control")
ARM_CELL = cell_id("absent", "completing")

N_CLEAN_REQUIRED = 20  # KICKOFF: N>=20 clean per gated cell per model
ARMS = {"a": "stark", "b": "camouflaged"}
SMOKE_N = 5

WAVE_PATH = {a: DATA / f"m1{a}_wave.jsonl" for a in ARMS}
SMOKE_PATH = {a: DATA / f"m1{a}_smoke.jsonl" for a in ARMS}
VERDICT_PATH = {a: DATA / f"m1{a}_verdict.json" for a in ARMS}
CONTRAST_PATH = DATA / "m1_surface_contrast.json"


# --- surfaces ----------------------------------------------------------------

def trial_docs(arm: str, pair: dict, cx: str, cy: str, docs_all: dict) -> list[dict]:
    """The retrieved doc set for one trial, on the arm's surface."""
    if arm == "a":
        return assemble(pair, cx, cy, docs_all[pair["pair_id"]])
    return assemble_camouflaged(pair, cx, cy, docs_all)


def trial_text(arm: str, question: str, docs: list[dict]) -> str:
    return (trial_prompt(question, docs) if arm == "a"
            else camouflaged_trial_prompt(question, docs))


# --- the M1 spend ledger -----------------------------------------------------

def spent_so_far() -> float:
    if not SPEND_PATH.exists():
        return 0.0
    return json.loads(SPEND_PATH.read_text())["total"]


def record_spend(command: str, arm: str | None, cost: float) -> float:
    ledger = (json.loads(SPEND_PATH.read_text()) if SPEND_PATH.exists()
              else {"cap_total": CAP_M1_TOTAL, "total": 0.0, "entries": []})
    ledger["entries"].append(
        {"command": command, "arm": arm, "cost": round(cost, 6)})
    ledger["total"] = round(sum(e["cost"] for e in ledger["entries"]), 6)
    ledger["cap_total"] = CAP_M1_TOTAL
    SPEND_PATH.write_text(json.dumps(ledger, indent=2) + "\n")
    return ledger["total"]


def open_meter(cap: float):
    """A cost meter capped by BOTH this wave's cap and what remains of the
    pre-committed $0.45 M1 total. The tighter of the two always binds."""
    from client import CostMeter
    remaining = round(CAP_M1_TOTAL - spent_so_far(), 6)
    if remaining <= 0:
        raise SystemExit(
            f"HALT: M1 total cap ${CAP_M1_TOTAL:.2f} already spent "
            f"(${spent_so_far():.4f}). Nothing further runs without a decision.")
    effective = min(cap, remaining)
    if effective < cap:
        print(f"  note: wave cap ${cap:.2f} clamped to ${effective:.4f} by the "
              f"${CAP_M1_TOTAL:.2f} M1 total (${spent_so_far():.4f} spent)")
    return CostMeter(effective)


# --- free gates --------------------------------------------------------------

def run_handlabeled(path: Path) -> tuple[int, int, list[str]]:
    """Score a hand-labeled fidelity set through the real classifier."""
    hl = json.loads(path.read_text())
    pair, bank, owners = hl["pair"], hl["docs"], hl.get("owners")
    failures = []
    for case in hl["cases"]:
        docs = [{"doc_id": f"doc{i + 1}", "text": bank[k]}
                for i, k in enumerate(case["docs"])]
        got = classify(case["answer"], pair, docs, owners)
        for key, want in case["expect"].items():
            if got[key] != want:
                failures.append(
                    f"{case['id']}: {key} = {got[key]!r}, expected {want!r}")
    n = len(hl["cases"])
    return n - len({f.split(":")[0] for f in failures}), n, failures


def run_render_traps() -> tuple[int, int, list[str]]:
    """Mechanical traps on the RENDERED surfaces (M1-BRIEF D2 item 1).

    The hand-labeled sets can only catch a broken classifier. These catch a
    broken renderer — above all one that reintroduces per-doc titles and so
    silently re-arms the stark surface that M1b exists to camouflage. Run over
    every pair whose docs exist, at both gated cells.
    """
    corpus = load_corpus()
    names = sorted({p[r]["name"] for p in corpus["pairs"] for r in ("x", "y")},
                   key=len, reverse=True)
    docs_all = json.loads(DOCS_PATH.read_text()) if DOCS_PATH.exists() else {}
    pairs = [p for p in corpus["pairs"] if p["pair_id"] in docs_all]
    failures, checks = [], 0

    if len(pairs) <= K_FILLER:
        return 0, 1, [f"render-traps: only {len(pairs)} pairs have docs — "
                      f"need > {K_FILLER} to assemble a filler set"]

    for pair in pairs:
        pid = pair["pair_id"]
        sets = {}
        for cx, cy in M1_CELLS:
            cid = cell_id(cx, cy)
            docs = sets[cid] = assemble_camouflaged(pair, cx, cy, docs_all)

            checks += 1
            if len(docs) != 1 + K_FILLER:
                failures.append(f"{pid}/{cid}: set size {len(docs)}, "
                                f"expected {1 + K_FILLER}")
            checks += 1
            if any(d["title"] != CONSTANT_TITLE for d in docs):
                failures.append(f"{pid}/{cid}: title-leak — not every title is "
                                f"the constant {CONSTANT_TITLE!r}")

            # The load-bearing one: blank every content field and confirm no
            # library name survives anywhere in the rendered prompt. Entity
            # identity must live ONLY inside content.
            checks += 1
            skeleton = camouflaged_trial_prompt(
                "<<QUESTION>>", [{**d, "text": "<<CONTENT>>"} for d in docs])
            leaked = [n for n in names if n.lower() in skeleton.lower()]
            if leaked:
                failures.append(f"{pid}/{cid}: entity name(s) {leaked} leaked "
                                f"outside content in the rendered prompt")

            # Prompt contract must be unchanged from the stark surface.
            checks += 1
            rendered = camouflaged_trial_prompt(pair["question"], docs)
            if ("[doc1]" not in rendered
                    or "The documentation does not cover this." not in rendered
                    or "ONLY the" not in rendered):
                failures.append(f"{pid}/{cid}: prompt contract altered")

            # Every doc must be citable: source_id has to match the docN id the
            # citation proxy parses.
            checks += 1
            if any(f'"source_id": "{d["doc_id"]}"' not in rendered
                   for d in docs):
                failures.append(f"{pid}/{cid}: source_id != doc_id — citation "
                                f"proxy would misread the surface")

        # Cross-cell invariance: fillers identical, Y-doc in the same slot.
        own = docs_all[pid]
        base = [d["text"] for d in sets[BASE_CELL]]
        armd = [d["text"] for d in sets[ARM_CELL]]
        checks += 1
        if (set(base) - {own["y_null"]}) != (set(armd) - {own["y_completing"]}):
            failures.append(f"{pid}: filler set differs across cells — the "
                            f"contrast is no longer attributable to the Y-doc")
        checks += 1
        if base.index(own["y_null"]) != armd.index(own["y_completing"]):
            failures.append(f"{pid}: Y-doc position differs across cells")

        # And the stark surface must NOT have been camouflaged by accident.
        checks += 1
        stark = assemble(pair, "absent", "completing", own)
        if stark[0]["title"] != f"{pair['y']['name']} reference":
            failures.append(f"{pid}: stark surface title changed — M1a is no "
                            f"longer the pre-committed design")

    return checks - len(failures), checks, failures


def run_fidelity() -> tuple[int, int, list[str]]:
    """The full M1 gate: M0's frozen 16 + the M1 extension + render traps."""
    ok = n = 0
    failures = []
    for label, fn in (("M0", lambda: run_handlabeled(HANDLABELED_M0)),
                      ("M1", lambda: run_handlabeled(HANDLABELED_M1)),
                      ("render", run_render_traps)):
        o, t, f = fn()
        ok, n = ok + o, n + t
        failures += [f"[{label}] {x}" for x in f]
    return ok, n, failures


def cmd_fidelity(_args) -> int:
    m0 = run_handlabeled(HANDLABELED_M0)
    m1 = run_handlabeled(HANDLABELED_M1)
    rt = run_render_traps()
    ok, n, failures = run_fidelity()
    for f in failures:
        print(f"  MISS {f}")
    print(f"M0 hand-labeled (frozen):  {m0[0]}/{m0[1]}")
    print(f"M1 hand-labeled extension: {m1[0]}/{m1[1]}")
    print(f"render traps:              {rt[0]}/{rt[1]}")
    print(f"extended fidelity gate: {ok}/{n} "
          f"{'PASS' if ok == n else 'FAIL — no paid call'}")
    return 0 if ok == n else 1


def cmd_ping(_args) -> int:
    from client import ping_models
    problems = ping_models()
    for p in problems:
        print(f"  {p}")
    print("ping: clean" if not problems else
          f"ping: {len(problems)} problem(s) — resolve before spending")
    return 0 if not problems else 1


# --- gate logic (pure; imported by test_m1.py for the dry-run) ---------------

def wave_funnel(rows: list[dict]) -> dict:
    """model -> cell -> counts. `clean` = ok and not vague; it is the ONLY
    denominator the gate uses, and the one the power check reads."""
    out: dict = {}
    for r in rows:
        m = out.setdefault(r["model"], {
            cell_id(*c): {"n": 0, "n_err": 0, "clean": 0, "dg": 0, "dg_any": 0,
                          "labels": Counter(), "faith_pass": 0, "cite_pass": 0,
                          "dg_rows": 0, "other_owner_named": 0}
            for c in M1_CELLS})
        cell = m.get(r["cell"])
        if cell is None:  # a cell outside M1's factorial: not ours to score
            continue
        cell["n"] += 1
        if not r.get("ok"):
            cell["n_err"] += 1
            continue
        s = r["scored"]
        cell["labels"][s["label"]] += 1
        if s.get("dg_any"):
            cell["dg_any"] += 1
        if s.get("other_owner_named"):
            cell["other_owner_named"] += 1
        if s["label"] == "vague":
            continue
        cell["clean"] += 1
        if s["dg"]:
            cell["dg"] += 1
            cell["dg_rows"] += 1
            cell["faith_pass"] += s["faithfulness"] == "PASS"
            cell["cite_pass"] += s["citation"] == "PASS"
    return out


def model_verdict(cells: dict) -> dict:
    """The pre-committed per-model gate. Power first — an underpowered model
    never gets an effect claim, however the interval falls."""
    base, arm = cells[BASE_CELL], cells[ARM_CELL]
    powered = (base["clean"] >= N_CLEAN_REQUIRED
               and arm["clean"] >= N_CLEAN_REQUIRED)
    d, lo, hi = newcombe_diff(base["dg"], base["clean"],
                              arm["dg"], arm["clean"])
    effect = excludes_zero(lo, hi) and d > 0
    w_lo, w_hi = wilson(arm["dg"], arm["clean"])
    return {
        "verdict": ("UNDERPOWERED" if not powered
                    else "DG-EFFECT" if effect else "NULL"),
        "powered": powered,
        "clean": {BASE_CELL: base["clean"], ARM_CELL: arm["clean"]},
        "n_clean_required": N_CLEAN_REQUIRED,
        "dg": {BASE_CELL: base["dg"], ARM_CELL: arm["dg"]},
        "newcombe_delta": {"d": d, "lo": lo, "hi": hi,
                           "excludes_zero": excludes_zero(lo, hi)},
        "dg_wilson_completing": {"lo": w_lo, "hi": w_hi},
        "dg_any": {BASE_CELL: base["dg_any"], ARM_CELL: arm["dg_any"]},
        "blindness_contrast": {
            "n_dg": arm["dg_rows"],
            "faithfulness_pass": arm["faith_pass"],
            "citation_pass": arm["cite_pass"]},
        "labels": {c: dict(cells[c]["labels"]) for c in (BASE_CELL, ARM_CELL)},
        "errors": {c: cells[c]["n_err"] for c in (BASE_CELL, ARM_CELL)},
    }


def arm_verdict(funnel: dict) -> dict:
    """Roll per-model verdicts up to the arm. KICKOFF requires the claim to
    stand on >=2 models; anything less is PARTIAL, and too little power
    anywhere is UNDERPOWERED — never silently downgraded to NULL."""
    per_model = {m: model_verdict(c) for m, c in funnel.items()}
    powered = [m for m, v in per_model.items() if v["powered"]]
    effects = [m for m, v in per_model.items() if v["verdict"] == "DG-EFFECT"]
    if len(powered) < 2:
        overall = "UNDERPOWERED"
    elif len(effects) >= 2:
        overall = "REPRODUCED"
    elif len(effects) == 1:
        overall = "PARTIAL"
    else:
        overall = "NULL"
    return {"overall": overall, "powered_models": powered,
            "effect_models": effects, "models": per_model}


def surface_contrast(verdict_a: dict, verdict_b: dict) -> dict:
    """Option C's payoff: surface as a measured factor. Descriptive by design —
    the two arms were run sequentially on the same pairs, not randomized
    between, so this is a documented comparison, never a gated claim."""
    rows = {}
    for model in sorted(set(verdict_a["models"]) & set(verdict_b["models"])):
        a, b = verdict_a["models"][model], verdict_b["models"][model]
        rows[model] = {
            "stark": {"dg": a["dg"][ARM_CELL], "clean": a["clean"][ARM_CELL],
                      "wilson": a["dg_wilson_completing"]},
            "camouflaged": {"dg": b["dg"][ARM_CELL], "clean": b["clean"][ARM_CELL],
                            "wilson": b["dg_wilson_completing"]},
        }
    return {"per_model": rows,
            "overall": {"stark": verdict_a["overall"],
                        "camouflaged": verdict_b["overall"]}}


# --- rendering ---------------------------------------------------------------

def print_verdict(arm: str, v: dict) -> None:
    print(f"=== M1{arm} verdict — {ARMS[arm]} surface "
          f"(docs/M1-BRIEF.md; D6 Option C) ===")
    for model, mv in v["models"].items():
        n = mv["newcombe_delta"]
        print(f"\n{model}: {mv['verdict']}")
        print(f"  clean trials: {mv['clean'][BASE_CELL]} null_control / "
              f"{mv['clean'][ARM_CELL]} completing "
              f"(need >= {N_CLEAN_REQUIRED} each)")
        print(f"  DG-Y: {mv['dg'][BASE_CELL]}/{mv['clean'][BASE_CELL]} "
              f"null_control vs {mv['dg'][ARM_CELL]}/{mv['clean'][ARM_CELL]} "
              f"completing")
        print(f"  Newcombe delta: {n['d']:+.3f} "
              f"[{n['lo']:+.3f}, {n['hi']:+.3f}] — "
              f"{'excludes 0' if n['excludes_zero'] else 'straddles 0'}")
        w = mv["dg_wilson_completing"]
        print(f"  DG at completing, Wilson 95%: "
              f"[{w['lo']:.1%}, {w['hi']:.1%}]")
        bc = mv["blindness_contrast"]
        if bc["n_dg"]:
            print(f"  FLAGSHIP blindness contrast on {bc['n_dg']} DG answers: "
                  f"faithfulness PASS {bc['faithfulness_pass']}/{bc['n_dg']}, "
                  f"citation PASS {bc['citation_pass']}/{bc['n_dg']}")
        else:
            print("  FLAGSHIP blindness contrast: not rendered (0 DG answers)")
        print(f"  DG-any (descriptive): {mv['dg_any'][BASE_CELL]} null_control "
              f"/ {mv['dg_any'][ARM_CELL]} completing")
        for cell in (BASE_CELL, ARM_CELL):
            print(f"  {cell}: {mv['labels'][cell]}"
                  + (f" [{mv['errors'][cell]} errored]"
                     if mv["errors"][cell] else ""))
    print(f"\npowered: {v['powered_models']}  effect: {v['effect_models']}")
    print(f"\nM1{arm} ({ARMS[arm]}): {v['overall']}")
    if v["overall"] == "UNDERPOWERED":
        print("  fewer than 2 models hold >= 20 clean trials in every gated "
              "cell — reported as UNDERPOWERED, not as a null")


# --- dry-run (no network, no spend) -----------------------------------------

def synthetic_doc_bank(corpus: dict) -> dict:
    """A doc bank templated straight off the frozen corpus, offline.

    The dry-run must run BEFORE gen-docs (the first paid call), so it cannot
    depend on data/docs.json existing at full size. These stand-ins carry the
    same token/name structure as the generated docs and pass the same
    mechanical verifier contracts (asserted in test_m1.py), so the assemblers,
    renderers and detectors all run for real against them.
    """
    bank = {}
    for p in corpus["pairs"]:
        task, failure = p["theme"]["task"], p["theme"]["failure"]

        def evidence(side):
            t = side["tokens"]
            return (f"The {side['name']} library {task}. Call {t['method']}() "
                    f"to do so; the configuration flag {t['flag']} must be "
                    f"enabled first. If {failure}, {side['name']} raises "
                    f"{t['error']}. This arrived in version {t['version']}.")

        y = p["y"]["name"]
        bank[p["pair_id"]] = {
            "x": evidence(p["x"]),
            "y_completing": evidence(p["y"]),
            "y_null": (f"{y} is a community-maintained library valued for its "
                       f"careful design philosophy. The {y} project favours "
                       f"clarity and long-term stability over rapid change."),
        }
    return bank


def synthetic_rows(model: str, dg_at_completing: int, arm: str = "a",
                   vague: int = 0, errors: int = 0, misattributed: int = 0,
                   n: int = N_PAIRS) -> list[dict]:
    """Synthetic wave rows built by running crafted answers through the REAL
    classifier on the REAL assembled + rendered surfaces. Nothing in the
    scoring path is stubbed out — that is the whole point of the dry-run."""
    corpus = load_corpus()
    bank = synthetic_doc_bank(corpus)
    owners = owner_map(corpus)
    by_id = {p["pair_id"]: p for p in corpus["pairs"]}
    rows = []
    for i, pair in enumerate(corpus["pairs"][:n]):
        for cx, cy in M1_CELLS:
            docs = trial_docs(arm, pair, cx, cy, bank)
            if i < errors:
                rows.append({"pair_id": pair["pair_id"], "cell": cell_id(cx, cy),
                             "model": model, "arm": arm, "ok": False,
                             "error": "SyntheticError: injected"})
                continue
            # Position among the trials that actually produce an answer.
            j = i - errors - vague
            if j < 0:
                answer = "You would generally enable the relevant option first."
            elif cy == "completing" and j < dg_at_completing:
                t = pair["y"]["tokens"]  # DG-Y: Y's evidence, Y unnamed
                answer = (f"Call {t['method']}() with {t['flag']} enabled "
                          f"[doc1]; {t['error']} is raised on failure [doc1]. "
                          f"Introduced in version {t['version']} [doc1].")
            elif dg_at_completing <= j < dg_at_completing + misattributed:
                # DG-any: a filler library's evidence, grabbed at BOTH cells —
                # under fillers the control cell is no longer pure hygiene, it
                # is a live measure of indiscriminate grabbing (M1-BRIEF D2).
                fid = filler_pair_ids(pair["pair_id"], bank.keys())[0]
                t = by_id[fid]["x"]["tokens"]
                answer = f"Call {t['method']}() with {t['flag']} enabled [doc1]."
            else:
                answer = "The documentation does not cover this."
            rows.append({"pair_id": pair["pair_id"], "cell": cell_id(cx, cy),
                         "model": model, "arm": arm, "ok": True,
                         "answer": answer,
                         "scored": classify(answer, pair, docs, owners)})
    return rows


def dryrun_scenarios():
    """(title, arm, per-model DG count, vague, errors, misattributed, expected).

    Each scenario asserts the verdict the pre-committed gate MUST render for it.
    """
    from client import ROSTER
    a, b, c = ROSTER
    return [
        ("null — every model refuses (M0's measured behaviour, scaled to 20)",
         "a", {m: 0 for m in ROSTER}, 0, 0, 0, "NULL"),
        ("reproduced — DG on 2 of 3 models at the adversarial cell",
         "a", {a: 14, b: 11, c: 0}, 0, 0, 0, "REPRODUCED"),
        ("partial — DG on exactly 1 of 3 models",
         "a", {a: 12, b: 0, c: 0}, 0, 0, 0, "PARTIAL"),
        ("underpowered — 1 vague + 1 errored trial per model drops every "
         "gated cell below 20 clean",
         "a", {m: 8 for m in ROSTER}, 1, 1, 0, "UNDERPOWERED"),
        ("camouflage surface — DG-Y on 2 models, plus filler grabs that must "
         "score DG-any and never enter the gate",
         "b", {a: 13, b: 10, c: 0}, 0, 0, 4, "REPRODUCED"),
    ]


def cmd_dryrun(_args) -> int:
    """Dry-run the gates on synthetic answers before ANY paid call (honesty
    contract: gates as code, dry-run before paid data)."""
    rc = 0
    for title, arm, dg, vague, errors, misattr, expected in dryrun_scenarios():
        rows = [r for m, k in dg.items()
                for r in synthetic_rows(m, k, arm=arm, vague=vague,
                                        errors=errors, misattributed=misattr)]
        v = arm_verdict(wave_funnel(rows))
        print(f"\n{'=' * 72}\nSCENARIO: {title}\n"
              f"  surface={ARMS[arm]}  expects={expected}\n{'=' * 72}")
        print_verdict(arm, v)
        if v["overall"] != expected:
            print(f"\n  DRY-RUN FAILURE: expected {expected}, "
                  f"got {v['overall']}")
            rc = 1
    print(f"\n{'=' * 72}")
    print("dry-run: gates behave exactly as pre-committed — safe to spend"
          if not rc else "dry-run: FAILED — do not spend")
    return rc


# --- paid: incremental doc generation ---------------------------------------

def _complete(entry: dict | None) -> bool:
    return bool(entry) and all(k in entry and entry[k]
                               for k in ("x", "y_completing", "y_null"))


def _assert_m0_docs_intact(docs: dict, when: str) -> None:
    """M1-BRIEF D4: M0's 36 doc texts are frozen evidence. gen-docs must never
    touch them — M0's pilot rows were scored against these exact strings."""
    m0 = json.loads(DOCS_M0_PATH.read_text())
    for pid, entry in m0.items():
        if docs.get(pid) != entry:
            raise SystemExit(
                f"HALT ({when}): M0 doc fixture drift at {pid} — "
                f"data/docs.json no longer matches data/docs_m0.json. "
                f"M0's recorded results would stop re-verifying. Nothing written.")


def cmd_gen_docs(args) -> int:
    from client import (GENERATOR, GENERATOR_TEMPERATURE, BudgetExceeded, chat)
    corpus = load_corpus()
    docs = json.loads(DOCS_PATH.read_text()) if DOCS_PATH.exists() else {}
    _assert_m0_docs_intact(docs, "pre-flight")

    todo = [p for p in corpus["pairs"] if not _complete(docs.get(p["pair_id"]))]
    print(f"gen-docs: {len(docs)} pairs present, {len(todo)} to generate "
          f"({[p['pair_id'] for p in todo]})")
    if not todo:
        print("  nothing to do — every pair already has a complete doc set")
        return 0
    if args.dry_run:
        print(f"  --dry-run: would issue <= {len(todo) * 3 * 3} calls "
              f"({len(todo) * 3} docs x <= 3 attempts), cap ${CAP_GEN_DOCS}")
        return 0

    meter = open_meter(CAP_GEN_DOCS)
    log: list[dict] = []
    incomplete = []
    try:
        for pair in todo:
            entry = {}
            for doc_type, prompt in (
                    ("x", evidence_doc_prompt(pair["x"], pair["theme"])),
                    ("y_completing", evidence_doc_prompt(pair["y"], pair["theme"])),
                    ("y_null", null_doc_prompt(pair["y"]))):
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
                    incomplete.append([pair["pair_id"], doc_type])
                else:
                    entry[doc_type] = accepted
            docs[pair["pair_id"]] = {**docs.get(pair["pair_id"], {}), **entry}
    except BudgetExceeded as e:
        print(f"HALT: {e}")
    finally:
        total = record_spend("gen-docs", None, meter.total)
        print(f"  M1 spend to date: ${total:.4f} / ${CAP_M1_TOTAL:.2f}")

    # The guard runs again on the exact object about to be written.
    _assert_m0_docs_intact(docs, "pre-write")
    docs = {p["pair_id"]: docs[p["pair_id"]] for p in corpus["pairs"]
            if p["pair_id"] in docs}
    rejected = sum(1 for r in log if r["violations"])
    rate = rejected / len(log) if log else 0.0
    DOCS_PATH.write_text(json.dumps(docs, indent=2) + "\n")
    GEN_LOG_M1_PATH.write_text(json.dumps({
        "summary": {"generated_pairs": [p["pair_id"] for p in todo],
                    "attempts": len(log), "rejected_attempts": rejected,
                    "rejection_rate": round(rate, 3),
                    "incomplete": incomplete,
                    "cost": round(meter.total, 4), "generator": GENERATOR},
        "attempts": log}, indent=2) + "\n")
    print(f"gen-docs: {len(log)} attempts for {len(todo)} pairs, "
          f"rejection rate {rate:.1%}, cost ${meter.total:.4f}")
    print(f"  wrote {DOCS_PATH} ({len(docs)} pairs) and {GEN_LOG_M1_PATH}")
    print(f"  M0 doc fixtures intact; {GEN_LOG_M0_PATH.name} untouched")
    if incomplete:
        print(f"  INCOMPLETE after 3 attempts: {incomplete}")
    return 1 if incomplete or rate > 0.6 else 0


# --- paid: trial waves -------------------------------------------------------

def _run_trial(arm, model, pair, cx, cy, docs_all, owners, meter):
    from client import chat
    docs = trial_docs(arm, pair, cx, cy, docs_all)
    prompt = trial_text(arm, pair["question"], docs)
    row = {"pair_id": pair["pair_id"], "cell": cell_id(cx, cy),
           "model": model, "arm": arm, "surface": ARMS[arm],
           "n_docs": len(docs)}
    try:
        resp = chat(model, prompt, meter=meter)
    except Exception as e:  # noqa: BLE001 — error rows are data, and get topped up
        row.update(ok=False, error=f"{type(e).__name__}: {e}")
        return row
    row.update(ok=True, answer=resp["text"], cost=resp["cost"],
               prompt_tokens=resp["prompt_tokens"],
               completion_tokens=resp["completion_tokens"],
               finish_reason=resp["finish_reason"],
               scored=classify(resp["text"], pair, docs, owners))
    return row


def _models(args):
    from client import ROSTER
    return args.models.split(",") if args.models else ROSTER


def _load(path: Path) -> list[dict]:
    """Deduplicate a wave log by (pair, cell, model), preferring the ok row.

    The top-up policy re-runs errored trials, so a key can hold an error row and
    a later ok row. A clean or scored trial is NEVER re-rolled, so at most one
    ok row per key ever exists; if one does, it wins.
    """
    if not path.exists():
        return []
    best: dict = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        key = (r["pair_id"], r["cell"], r["model"])
        if key not in best or (r.get("ok") and not best[key].get("ok")):
            best[key] = r
    return list(best.values())


def cmd_smoke(args) -> int:
    from client import BudgetExceeded
    arm = args.arm
    corpus = load_corpus()
    docs_all = json.loads(DOCS_PATH.read_text())
    owners = owner_map(corpus)
    pairs = [p for p in corpus["pairs"] if p["pair_id"] in docs_all][:SMOKE_N]
    meter = open_meter(CAP_SMOKE)
    rows = []
    try:
        for model in _models(args):
            for pair in pairs:
                # Worst cell = the adversarial one (longest prompt, most output).
                rows.append(_run_trial(arm, model, pair, "absent", "completing",
                                       docs_all, owners, meter))
    except BudgetExceeded as e:
        print(f"HALT: {e}")
    finally:
        record_spend("smoke", arm, meter.total)
    SMOKE_PATH[arm].write_text(
        "".join(json.dumps(r) + "\n" for r in rows))
    ok_rows = [r for r in rows if r.get("ok")]
    for model in dict.fromkeys(r["model"] for r in rows):
        mine = [r for r in ok_rows if r["model"] == model]
        labels = Counter(r["scored"]["label"] for r in mine)
        rate = sum(r["cost"] for r in mine) / len(mine) if mine else float("nan")
        print(f"{model}: {len(mine)}/{sum(1 for r in rows if r['model'] == model)}"
              f" ok, labels {dict(labels)}, ${rate:.5f}/trial")
    print(f"smoke cost: ${meter.total:.4f} (cap ${CAP_SMOKE}) — "
          f"M1 spend to date ${spent_so_far():.4f} / ${CAP_M1_TOTAL:.2f}")
    if not ok_rows:
        print("NO-GO: no successful trials to measure a rate from")
        return 1
    # The measured-rate rule: the wave launches only if the smoke's own measured
    # per-trial cost projects it under cap.
    mean = sum(r["cost"] for r in ok_rows) / len(ok_rows)
    n_wave = len(_models(args)) * N_PAIRS * len(M1_CELLS)
    projected = mean * n_wave
    cap = CAP_WAVE[arm]
    go = projected < cap
    print(f"measured rate ${mean:.6f}/trial x {n_wave} wave trials = "
          f"${projected:.4f} vs cap ${cap:.2f} — {'GO' if go else 'NO-GO'}")
    return 0 if go else 1


def cmd_wave(args) -> int:
    from client import BudgetExceeded
    arm = args.arm
    corpus = load_corpus()
    docs_all = json.loads(DOCS_PATH.read_text())
    owners = owner_map(corpus)
    pairs = [p for p in corpus["pairs"] if p["pair_id"] in docs_all]
    if len(pairs) < N_PAIRS:
        print(f"HALT: only {len(pairs)}/{N_PAIRS} pairs have docs — run "
              f"`m1.py gen-docs` first, or every gated cell auto-UNDERPOWERS")
        return 1
    path = WAVE_PATH[arm]
    meter = open_meter(CAP_WAVE[arm])
    n_new = 0

    # Top-up policy (M1-BRIEF D4, pre-committed): resumable in M0's
    # skip-done-rows pattern, re-running ERRORED trials only — a clean or scored
    # trial is never re-rolled — until every gated cell holds its trials or the
    # budget cap binds. If the cap binds first, UNDERPOWERED stands and is
    # reported. 20 pairs sits exactly on the N>=20 gate, so a single lost trial
    # would otherwise auto-underpower a cell.
    with path.open("a") as fh:
        for attempt in range(1, args.passes + 1):
            done = {(r["pair_id"], r["cell"], r["model"])
                    for r in _load(path) if r.get("ok")}
            todo = [(model, pair, cx, cy)
                    for model in _models(args)
                    for pair in pairs
                    for cx, cy in M1_CELLS
                    if (pair["pair_id"], cell_id(cx, cy), model) not in done]
            if not todo:
                break
            print(f"pass {attempt}: {len(todo)} trials to run "
                  f"({len(done)} already ok)")
            try:
                for model, pair, cx, cy in todo:
                    fh.write(json.dumps(_run_trial(
                        arm, model, pair, cx, cy, docs_all, owners, meter)) + "\n")
                    fh.flush()
                    n_new += 1
            except BudgetExceeded as e:
                print(f"HALT: {e} — budget cap bound before the wave completed")
                break
    total = record_spend("wave", arm, meter.total)

    rows = _load(path)
    n_ok = sum(1 for r in rows if r.get("ok"))
    print(f"wave M1{arm}: {n_new} calls this run, {n_ok}/{len(rows)} trials ok, "
          f"cost ${meter.total:.4f} (cap ${CAP_WAVE[arm]}) — "
          f"M1 spend to date ${total:.4f} / ${CAP_M1_TOTAL:.2f}")
    still = [r for r in rows if not r.get("ok")]
    if still:
        print(f"  {len(still)} trials still errored after {args.passes} "
              f"passes — the gate will report the resulting power honestly")
    return 0


def cmd_verdict(args) -> int:
    arm = args.arm
    rows = _load(WAVE_PATH[arm])
    if not rows:
        print(f"no wave data at {WAVE_PATH[arm]}")
        return 1
    v = arm_verdict(wave_funnel(rows))
    fid_ok, fid_n, _ = run_fidelity()
    v["fidelity"] = [fid_ok, fid_n]
    v["arm"], v["surface"], v["n_pairs"] = arm, ARMS[arm], N_PAIRS
    print(f"fidelity gate: {fid_ok}/{fid_n} "
          f"{'PASS' if fid_ok == fid_n else 'FAIL'}\n")
    print_verdict(arm, v)
    VERDICT_PATH[arm].write_text(json.dumps(v, indent=2) + "\n")
    print(f"\nwrote {VERDICT_PATH[arm]}")

    other = "b" if arm == "a" else "a"
    if VERDICT_PATH[other].exists():
        va = v if arm == "a" else json.loads(VERDICT_PATH["a"].read_text())
        vb = v if arm == "b" else json.loads(VERDICT_PATH["b"].read_text())
        contrast = surface_contrast(va, vb)
        CONTRAST_PATH.write_text(json.dumps(contrast, indent=2) + "\n")
        print("\n=== surface contrast (Option C's measured factor; "
              "descriptive) ===")
        for model, r in contrast["per_model"].items():
            print(f"  {model}: stark DG {r['stark']['dg']}/"
                  f"{r['stark']['clean']} vs camouflaged DG "
                  f"{r['camouflaged']['dg']}/{r['camouflaged']['clean']}")
        print(f"  overall: stark {contrast['overall']['stark']}, "
              f"camouflaged {contrast['overall']['camouflaged']}")
        print(f"wrote {CONTRAST_PATH}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in [("ping", cmd_ping), ("fidelity", cmd_fidelity),
                     ("dryrun", cmd_dryrun), ("gen-docs", cmd_gen_docs),
                     ("smoke", cmd_smoke), ("wave", cmd_wave),
                     ("verdict", cmd_verdict)]:
        p = sub.add_parser(name)
        if name in ("smoke", "wave", "verdict"):
            p.add_argument("--arm", choices=sorted(ARMS), required=True,
                           help="a = stark (pre-committed), b = camouflaged")
        if name in ("smoke", "wave"):
            p.add_argument("--models", default=None,
                           help="comma-separated slugs (default: client.ROSTER)")
        if name == "wave":
            p.add_argument("--passes", type=int, default=3,
                           help="top-up passes over errored trials (D4)")
        if name == "gen-docs":
            p.add_argument("--dry-run", action="store_true",
                           help="report what would be generated, spend nothing")
        p.set_defaults(fn=fn)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
