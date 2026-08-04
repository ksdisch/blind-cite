"""m1c.py — M1C: the pre-registered, power-sized extension (docs/M1C-BRIEF.md).

M1 measured DG-Y at N=20 clean trials per gated cell per surface and returned
NULL at both. PR #10's review then established (D18) that N=20 came from M0's
clean-TRIAL-YIELD funnel, never from a power calculation: 0/20 has a Wilson
upper of 16.1%, above the 14% nearest-published floor, so the study could not
resolve even the floor. M1C is the fix, pre-registered before any build or
spend and frozen from the first paid call.

What it runs, all of it fixed in the brief and none of it decided here:

  * ONE model — `qwen/qwen-2.5-7b-instruct`, the sole roster model with any
    published anchor (D1).
  * BOTH surfaces — arm a stark, arm b camouflaged, definitions unchanged from
    M1; both M1 cells per surface (`absent x null_control`, `absent x
    completing`).
  * +60 pairs (p21-p80) on top of M1's 20, for a COMBINED N of 80 clean trials
    per gated cell per surface (D2's sizing table).
  * ONE look: `verdict` runs once, at the end, and is the first aggregation of
    any rate. The blinding is procedural, not mechanical — `classify` scores
    each trial as it runs because the top-up loop needs clean-vs-vague — so
    what is pre-committed is that no wave/N/top-up decision keys off a DG
    label and no rate is computed before the verdict (D3).

Two things this file does NOT inherit from M1, both deliberate:

  * the UNDERPOWERED threshold. M1's `N_CLEAN_REQUIRED = 20` cannot flag a
    truncation anywhere in [20, 79] — a wave that died at 40 would report NULL
    as if sized for it. `N_CLEAN_REQUIRED_M1C = 80` is the M1C pre-commitment
    (D3), and the shortfall is stated when it binds.
  * the verdict vocabulary. M1 rendered a gate outcome; M1C additionally
    renders the D4 direction-only TEMPLATES, selected mechanically by where the
    Wilson interval sits relative to the 14% reference magnitude. The templates
    are the only permitted verbs, they carry the D21 caveats inline so no
    downstream rendering can drop them, and 14% is a reference magnitude for
    sizing and wording ONLY — never a null hypothesis about our cell.

The fidelity gate is imported from `m1` rather than re-implemented, which is the
only way to make D7's "unchanged from M1" literally true.

`m0.py` and `m1.py` remain frozen records, but this milestone did have to touch
them, and D7's "untouched" wording is superseded on that point (D26). Growing
the shared corpus to 80 pairs re-scoped the `corpus.N_PAIRS` those scripts read,
which silently changed their behaviour: `m1.py dryrun` began reporting FAILED,
`m1.py wave` would have run 480 trials instead of 120, and `m0.py`/`m1.py
verdict` would have rewritten their published verdict files with fidelity counts
from a corpus those milestones never ran on. Leaving the bytes alone was what
broke the records. Both are now pinned to their own `N_PAIRS_M0` / `N_PAIRS_M1`
— restoring exactly the behaviour they had — and both refuse to re-render a
verdict once the shared pool has moved. This file carries the same guard forward
for M1C (PR #12 review F1/F2).

Subcommands (free ones never touch the network except `ping`):
  ping      re-pin roster slugs + prices against live OpenRouter, pre-spend
  fidelity  the M1 fidelity gate, unchanged, now over 80 pairs
  dryrun    render the M1C verdict on SYNTHETIC answers — no network, no spend
  gen-docs  generate ONLY the extension pairs' docs (p21-p80)  (paid)
  smoke     N=5 on the worst cell per arm, measured cost/trial  (paid)
  wave      2 cells x 60 extension pairs, resumable + top-up    (paid)
  verdict   the ONE look: pool with M1, render the D4 templates
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from assemble import (K_FILLER, assemble, assemble_camouflaged, cell_id,
                      filler_pair_ids)
import corpus as _corpus
from corpus import (CORPUS_M1_PATH, CORPUS_PATH, N_PAIRS_M1, load_corpus,
                    owner_map)
from detectors import classify, verify_doc
from m1 import run_fidelity  # D7: the fidelity gate, unchanged from M1
from prompts import (camouflaged_trial_prompt, evidence_doc_prompt,
                     null_doc_prompt, trial_prompt)
from stats import excludes_zero, newcombe_diff, wilson

DATA = Path(__file__).parent / "data"
DOCS_PATH = DATA / "docs.json"
DOCS_M1_PATH = DATA / "docs_m1.json"
GEN_LOG_M1C_PATH = DATA / "gen_log_m1c.json"

# --- what the brief fixed (D1) -----------------------------------------------

MODEL = "qwen/qwen-2.5-7b-instruct"
ARMS = {"a": "stark", "b": "camouflaged"}
M1C_CELLS = [("absent", "null_control"), ("absent", "completing")]
BASE_CELL = cell_id("absent", "null_control")
ARM_CELL = cell_id("absent", "completing")

# --- sizing and power (D2, D3) -----------------------------------------------

# The reference magnitude, NOT a null hypothesis (D21): Qwen2.5-7B at the
# paper's `absent x prior_completing`, RAG-4 schema — a different condition by
# definition, and itself a stated lower bound.
FLOOR = 0.14

# Pinned literally, NOT read from the live pool. M1C's own scope is a
# pre-registered fact, and reading `corpus.N_PAIRS` here would let a later
# milestone's corpus growth silently redefine what "the extension" means —
# exactly the coupling that broke `m1.py` when this milestone grew the pool
# (PR #12 review F1/F2).
N_PAIRS_M1C = 80                        # M1C's corpus size (D2's sizing choice)
N_ORIGINAL = N_PAIRS_M1                 # 20, M1's own N, ingested read-only
N_EXTENSION = N_PAIRS_M1C - N_PAIRS_M1  # 60, this milestone's new trials
N_CLEAN_REQUIRED_M1C = 80               # combined clean per gated cell per surface
SMOKE_N = 5

ORIGINAL_PAIR_IDS = {f"p{i:02d}" for i in range(1, N_ORIGINAL + 1)}
EXTENSION_PAIR_IDS = {f"p{i:02d}" for i in range(N_ORIGINAL + 1, N_PAIRS_M1C + 1)}

SCOPES = ("original", "extension_only", "combined")

# --- budget (D6) -------------------------------------------------------------

# CAP_M1C_TOTAL is the pre-committed ceiling on MEASURED spend. The stage caps
# below are ~2x the D6 estimates (gen-docs $0.031, smoke $0.002, wave a $0.005,
# wave b $0.014) so an individual stage cannot run away, and they deliberately
# sum to more than the total: the `Decisions.md` D8 pattern is that every stage
# runs under min(its own cap, what is left of the total), so the total is what
# actually binds and is enforced against the ledger rather than against a sum.
CAP_M1C_TOTAL = 0.10
CAP_GEN_DOCS = 0.06
CAP_SMOKE = 0.01
CAP_WAVE = {"a": 0.02, "b": 0.04}
SPEND_PATH = DATA / "m1c_spend.json"

WAVE_PATH = {a: DATA / f"m1c{a}_wave.jsonl" for a in ARMS}
SMOKE_PATH = {a: DATA / f"m1c{a}_smoke.jsonl" for a in ARMS}
M1_WAVE_PATH = {a: DATA / f"m1{a}_wave.jsonl" for a in ARMS}
VERDICT_PATH = DATA / "m1c_verdict.json"


# --- surfaces (definitions unchanged from M1; re-stated, not imported, so the
# --- frozen script keeps no live callers here) -------------------------------

def trial_docs(arm: str, pair: dict, cx: str, cy: str, docs_all: dict) -> list[dict]:
    if arm == "a":
        return assemble(pair, cx, cy, docs_all[pair["pair_id"]])
    return assemble_camouflaged(pair, cx, cy, docs_all)


def trial_text(arm: str, question: str, docs: list[dict]) -> str:
    return (trial_prompt(question, docs) if arm == "a"
            else camouflaged_trial_prompt(question, docs))


# --- the M1C spend ledger (Decisions.md D8 pattern) --------------------------

def spent_so_far() -> float:
    if not SPEND_PATH.exists():
        return 0.0
    return json.loads(SPEND_PATH.read_text())["total"]


def record_spend(command: str, arm: str | None, cost: float) -> float:
    ledger = (json.loads(SPEND_PATH.read_text()) if SPEND_PATH.exists()
              else {"cap_total": CAP_M1C_TOTAL, "total": 0.0, "entries": []})
    ledger["entries"].append(
        {"command": command, "arm": arm, "cost": round(cost, 6)})
    ledger["total"] = round(sum(e["cost"] for e in ledger["entries"]), 6)
    ledger["cap_total"] = CAP_M1C_TOTAL
    SPEND_PATH.write_text(json.dumps(ledger, indent=2) + "\n")
    return ledger["total"]


def open_meter(cap: float):
    from client import CostMeter
    remaining = round(CAP_M1C_TOTAL - spent_so_far(), 6)
    if remaining <= 0:
        raise SystemExit(
            f"HALT: M1C total cap ${CAP_M1C_TOTAL:.2f} already spent "
            f"(${spent_so_far():.4f}). Nothing further runs without a decision.")
    effective = min(cap, remaining)
    if effective < cap:
        print(f"  note: stage cap ${cap:.2f} clamped to ${effective:.4f} by the "
              f"${CAP_M1C_TOTAL:.2f} M1C total (${spent_so_far():.4f} spent)")
    return CostMeter(effective)


# --- pooling preconditions (D5) ----------------------------------------------

def _assert_pooling_preconditions(docs: dict | None = None,
                                  when: str = "pre-flight") -> None:
    """The combined-N estimand pools M1's 20 trials with 60 new ones, so it is
    only valid while p01-p20 and their doc texts are the SAME artifacts M1's
    trials saw. Both guards run before anything is written and again before the
    one look. (PR #11 review F5: the brief once claimed this guard existed when
    no M1 fixture had ever been committed.)"""
    frozen = json.loads(CORPUS_PATH.read_text())
    m1_corpus = json.loads(CORPUS_M1_PATH.read_text())
    if frozen["pairs"][:N_ORIGINAL] != m1_corpus["pairs"]:
        raise SystemExit(
            f"HALT ({when}): data/corpus.json p01-p{N_ORIGINAL:02d} no longer "
            f"matches data/corpus_m1.json. M1's trials were run against those "
            f"pairs; pooling them with new trials would be invalid.")
    live = json.loads(DOCS_PATH.read_text()) if DOCS_PATH.exists() else {}
    if docs is not None:
        live = docs
    m1_docs = json.loads(DOCS_M1_PATH.read_text())
    for pid, entry in m1_docs.items():
        if live.get(pid) != entry:
            raise SystemExit(
                f"HALT ({when}): M1 doc fixture drift at {pid} — data/docs.json "
                f"no longer matches data/docs_m1.json. M1's rows were scored "
                f"against those exact strings. Nothing written.")


# --- D4: template bands and the fixed report strings -------------------------

def band(k: int, n: int) -> str:
    """Which D4 template fires for k events in n trials.

    Five bands, partitioning every reachable outcome: k=0 with the interval
    reaching the floor -> T0; k=0 with the upper below it -> T1; k>=1 with the
    upper below it -> T2; k>=1 with the interval containing it -> T3; lower
    bound above it -> T4. Pinned in `test_m1c_sizing.py`, which transcribes the
    five conditions from the brief's prose and evaluates them independently of
    this function, so the test can disagree with it.
    """
    lo, hi = wilson(k, n)
    if k == 0:
        return "T1" if hi < FLOOR else "T0"
    if hi < FLOOR:
        return "T2"
    if lo > FLOOR:
        return "T4"
    return "T3"


# Verbatim from docs/M1C-BRIEF.md D4. These are the ONLY permitted verbs, and
# each carries its caveats inline so no downstream rendering can drop them (the
# PR #10 review-F9 failure mode). Every number is filled from the row the
# template fires on.
TEMPLATES = {
    "T0": ("Zero DG observed on this surface ({k}/{n}, Wilson [0%, {hi}]) — an "
           "interval that reaches the floor's magnitude, so this row alone is "
           "uninformative against it (the D18 gap). Direction: at or below, "
           "hedged. This is not a replication claim and not a contradiction "
           "claim."),
    "T1": ("Our measured DG rate on this surface is 0% ({k}/{n}, Wilson "
           "[0%, {hi}]), below the nearest published floor for this model "
           "(>=14%, Qwen2.5-7B at `absent x prior_completing`, RAG-4 — a "
           "*different condition by definition*: the paper's completing "
           "evidence matches a parametric prior, ours is fabricated; a stated "
           "lower bound; a schema we did not run). Direction: lower. This is "
           "not a replication claim and not a contradiction claim."),
    "T2": ("DG occurs on this surface ({k}/{n}, Wilson [{lo}, {hi}], lower "
           "bound > 0) at a rate below the nearest published floor for this "
           "model (>=14% — different condition by definition, stated lower "
           "bound, schema we did not run). Direction: occurs, low. This is not "
           "a replication claim and not a contradiction claim."),
    "T3": ("DG occurs on this surface ({k}/{n}, Wilson [{lo}, {hi}]) at a rate "
           "whose interval reaches the magnitude of the nearest published "
           "floor (>=14% — different condition by definition, stated lower "
           "bound, schema we did not run). Direction: comparable magnitude, "
           "hedged. This is not a replication claim and not a contradiction "
           "claim."),
    "T4": ("DG occurs on this surface ({k}/{n}, Wilson [{lo}, {hi}]) at a rate "
           "above the nearest published floor (>=14% — different condition by "
           "definition, a stated lower bound whose true value may itself sit "
           "higher, schema we did not run). Direction: higher, hedged. This is "
           "not a replication claim and not a contradiction claim."),
}


def render_template(k: int, n: int) -> tuple[str, str]:
    """(band, the pre-committed statement with this row's numbers filled in)."""
    t = band(k, n)
    lo, hi = wilson(k, n)
    return t, TEMPLATES[t].format(k=k, n=n, lo=f"{lo:.1%}", hi=f"{hi:.1%}")


# --- gate logic (pure; the dry-run and test_m1c.py exercise exactly this) -----

def scope_counts(rows: list[dict]) -> dict:
    """cell -> counts, for ONE model on ONE surface over ONE scope of pairs.

    `clean` = ok and not vague, and it is the only denominator any rate uses —
    the same rule M1 gated on.
    """
    out = {cell_id(*c): {"n": 0, "n_err": 0, "clean": 0, "dg": 0, "dg_any": 0,
                         "labels": Counter(), "faith_pass": 0, "cite_pass": 0}
           for c in M1C_CELLS}
    for r in rows:
        cell = out.get(r["cell"])
        if cell is None:
            continue
        cell["n"] += 1
        if not r.get("ok"):
            cell["n_err"] += 1
            continue
        s = r["scored"]
        cell["labels"][s["label"]] += 1
        if s.get("dg_any"):
            cell["dg_any"] += 1
        if s["label"] == "vague":
            continue
        cell["clean"] += 1
        if s["dg"]:
            cell["dg"] += 1
            cell["faith_pass"] += s["faithfulness"] == "PASS"
            cell["cite_pass"] += s["citation"] == "PASS"
    return out


def scope_row(name: str, n_target: int, cells: dict) -> dict:
    """One data row of the D4 report: its counts, its interval, its template."""
    arm = cells[ARM_CELL]
    k, n = arm["dg"], arm["clean"]
    lo, hi = wilson(k, n)
    t, statement = render_template(k, n)
    return {
        "scope": name,
        "n_target": n_target,
        "clean": {c: cells[c]["clean"] for c in (BASE_CELL, ARM_CELL)},
        "dg": {c: cells[c]["dg"] for c in (BASE_CELL, ARM_CELL)},
        "dg_any": {c: cells[c]["dg_any"] for c in (BASE_CELL, ARM_CELL)},
        "errors": {c: cells[c]["n_err"] for c in (BASE_CELL, ARM_CELL)},
        "labels": {c: dict(cells[c]["labels"]) for c in (BASE_CELL, ARM_CELL)},
        "primary": {"k": k, "n": n, "wilson": {"lo": lo, "hi": hi}},
        "band": t,
        "statement": statement,
        "blindness_contrast": {"n_dg": k,
                               "faithfulness_pass": arm["faith_pass"],
                               "citation_pass": arm["cite_pass"]},
    }


def surface_verdict(original: list[dict], extension: list[dict]) -> dict:
    """The whole pre-committed analysis for one surface.

    Three rows always (D4): original N=20, extension-only N=60, combined N=80.
    The original is never replaced and the extension-only is never hidden. The
    primary estimand is the combined row; if extension-only would select a
    different template, BOTH statements are carried, extension-only first (D1)
    — the disagreement is reported, never averaged away.
    """
    scoped = {"original": (N_ORIGINAL, scope_counts(original)),
              "extension_only": (N_EXTENSION, scope_counts(extension)),
              "combined": (N_CLEAN_REQUIRED_M1C,
                           scope_counts(original + extension))}
    rows = {name: scope_row(name, n, cells) for name, (n, cells) in scoped.items()}

    combined = scoped["combined"][1]
    base, arm = combined[BASE_CELL], combined[ARM_CELL]
    powered = (base["clean"] >= N_CLEAN_REQUIRED_M1C
               and arm["clean"] >= N_CLEAN_REQUIRED_M1C)
    d, lo, hi = newcombe_diff(base["dg"], base["clean"], arm["dg"], arm["clean"])
    effect = excludes_zero(lo, hi) and d > 0

    disagree = rows["extension_only"]["band"] != rows["combined"]["band"]
    carry = (["extension_only", "combined"] if disagree else ["combined"])
    return {
        "rows": rows,
        "powered": powered,
        "n_clean_required": N_CLEAN_REQUIRED_M1C,
        "shortfall": {c: max(0, N_CLEAN_REQUIRED_M1C - combined[c]["clean"])
                      for c in (BASE_CELL, ARM_CELL)},
        "verdict": ("UNDERPOWERED" if not powered
                    else "DG-EFFECT" if effect else "NULL"),
        "newcombe_delta_combined": {"d": d, "lo": lo, "hi": hi,
                                    "excludes_zero": excludes_zero(lo, hi)},
        "template_disagreement": disagree,
        "statements_to_carry": carry,
    }


# --- free gates ---------------------------------------------------------------

def cmd_ping(_args) -> int:
    """D6: price re-pin before any spend. Drift is resolved consciously."""
    from client import ping_models
    problems = ping_models()
    for p in problems:
        print(f"  {p}")
    print("ping: clean" if not problems else
          f"ping: {len(problems)} problem(s) — resolve before spending")
    return 0 if not problems else 1


def cmd_fidelity(_args) -> int:
    ok, n, failures = run_fidelity()
    for f in failures:
        print(f"  MISS {f}")
    print(f"fidelity gate (M1's, unchanged, over {_corpus.N_PAIRS} pairs): "
          f"{ok}/{n} "
          f"{'PASS' if ok == n else 'FAIL — no paid call'}")
    return 0 if ok == n else 1


# --- rendering ----------------------------------------------------------------

def print_surface(arm: str, sv: dict) -> None:
    print(f"\n=== M1C{arm} — {ARMS[arm]} surface — {MODEL} ===")
    print(f"  gate verdict: {sv['verdict']}")
    for name in SCOPES:
        r = sv["rows"][name]
        p, w = r["primary"], r["primary"]["wilson"]
        print(f"\n  [{name}] target N={r['n_target']}  "
              f"clean {r['clean'][BASE_CELL]} null_control / "
              f"{r['clean'][ARM_CELL]} completing")
        print(f"    DG-Y at completing: {p['k']}/{p['n']} "
              f"Wilson [{w['lo']:.1%}, {w['hi']:.1%}] -> {r['band']}")
        bc = r["blindness_contrast"]
        if bc["n_dg"]:
            print(f"    blindness contrast on {bc['n_dg']} DG answers: "
                  f"faithfulness PASS {bc['faithfulness_pass']}/{bc['n_dg']}, "
                  f"citation PASS {bc['citation_pass']}/{bc['n_dg']}")
        print(f"    DG-any (descriptive): {r['dg_any'][BASE_CELL]} "
              f"null_control / {r['dg_any'][ARM_CELL]} completing")
        for cell in (BASE_CELL, ARM_CELL):
            print(f"    {cell}: {r['labels'][cell]}"
                  + (f" [{r['errors'][cell]} errored]" if r["errors"][cell] else ""))
    n = sv["newcombe_delta_combined"]
    print(f"\n  secondary — Newcombe delta at combined N: {n['d']:+.3f} "
          f"[{n['lo']:+.3f}, {n['hi']:+.3f}] — "
          f"{'excludes 0' if n['excludes_zero'] else 'straddles 0'}")
    if not sv["powered"]:
        print(f"  UNDERPOWERED: combined clean N below "
              f"{N_CLEAN_REQUIRED_M1C} — shortfall {sv['shortfall']}")
    print("\n  --- the pre-committed statement (D4; the only permitted verbs) ---")
    if sv["template_disagreement"]:
        print("  TEMPLATE DISAGREEMENT between extension-only and combined — "
              "both carried, extension-only first (D1)")
    for name in sv["statements_to_carry"]:
        r = sv["rows"][name]
        print(f"  [{name}, {r['band']}] {r['statement']}")


def print_verdict(v: dict) -> None:
    print(f"=== M1C verdict — {MODEL} (docs/M1C-BRIEF.md; D23) ===")
    print(f"fidelity gate: {v['fidelity'][0]}/{v['fidelity'][1]} "
          f"{'PASS' if v['fidelity'][0] == v['fidelity'][1] else 'FAIL'}")
    for arm in sorted(ARMS):
        print_surface(arm, v["surfaces"][arm])
    print(f"\nspend: ${v['spend']['total']:.4f} / ${CAP_M1C_TOTAL:.2f}")
    print("\n14% is a reference magnitude for sizing and wording only, never a "
          "null hypothesis about our cell (D21): the paper has no cell for our "
          "condition.")


# --- dry-run (no network, no spend) ------------------------------------------

def synthetic_doc_bank(corpus: dict) -> dict:
    """Offline stand-in docs with the same token/name structure as the generated
    ones, so the assemblers, renderers and detectors all run for real against
    them. They satisfy the real `verify_doc` contracts (asserted in
    test_m1c.py) — otherwise the dry-run would prove nothing about the paid
    path. Same construction M1 used."""
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


def synthetic_rows(arm: str, pair_ids: set[str], dg_at_completing: int,
                   vague: int = 0, errors: int = 0,
                   misattributed: int = 0) -> list[dict]:
    """Crafted answers run through the REAL classifier on the REAL assembled and
    rendered surfaces. Nothing in the scoring path is stubbed."""
    corpus = load_corpus()
    bank = synthetic_doc_bank(corpus)
    owners = owner_map(corpus)
    by_id = {p["pair_id"]: p for p in corpus["pairs"]}
    rows = []
    for i, pair in enumerate(p for p in corpus["pairs"]
                             if p["pair_id"] in pair_ids):
        for cx, cy in M1C_CELLS:
            docs = trial_docs(arm, pair, cx, cy, bank)
            if i < errors:
                rows.append({"pair_id": pair["pair_id"], "cell": cell_id(cx, cy),
                             "model": MODEL, "arm": arm, "ok": False,
                             "error": "SyntheticError: injected"})
                continue
            j = i - errors - vague
            if j < 0:
                answer = "You would generally enable the relevant option first."
            elif cy == "completing" and j < dg_at_completing:
                t = pair["y"]["tokens"]  # DG-Y: Y's evidence, Y unnamed
                answer = (f"Call {t['method']}() with {t['flag']} enabled "
                          f"[doc1]; {t['error']} is raised on failure [doc1]. "
                          f"Introduced in version {t['version']} [doc1].")
            elif dg_at_completing <= j < dg_at_completing + misattributed:
                fid = filler_pair_ids(pair["pair_id"], bank.keys())[0]
                t = by_id[fid]["x"]["tokens"]
                answer = f"Call {t['method']}() with {t['flag']} enabled [doc1]."
            else:
                answer = "The documentation does not cover this."
            rows.append({"pair_id": pair["pair_id"], "cell": cell_id(cx, cy),
                         "model": MODEL, "arm": arm, "ok": True,
                         "answer": answer,
                         "scored": classify(answer, pair, docs, owners)})
    return rows


def dryrun_scenarios():
    """(title, arm, dg_original, dg_extension, vague, errors, misattributed,
    expected gate verdict, expected COMBINED band).

    Every band the sizing table says is reachable at N=80 gets a scenario, so
    the rendering path is exercised for all five templates before a dollar is
    spent — plus the truncation case the UNDERPOWERED threshold exists for, and
    the extension-vs-combined template disagreement D1's side-by-side rule
    exists for.
    """
    return [
        ("null — every trial refuses, as M1 measured (combined 0/80)",
         "a", 0, 0, 0, 0, 0, "NULL", "T1"),
        ("T2 — the carried camouflaged events and nothing more (2/80)",
         "b", 2, 0, 0, 0, 0, "NULL", "T2"),
        ("T3 — the interval reaches the floor's magnitude (6/80)",
         "b", 2, 4, 0, 0, 0, "DG-EFFECT", "T3"),
        ("T4 — the doubled-reference sensitivity case (22/80)",
         "b", 2, 20, 0, 0, 0, "DG-EFFECT", "T4"),
        ("underpowered — one vague and one errored trial per cell leave the "
         "combined N at 78, which M1's inherited threshold of 20 would have "
         "passed silently",
         "a", 0, 0, 1, 1, 0, "UNDERPOWERED", "T1"),
        ("side-by-side — extension-only fires T3 while combined fires T2, the "
         "disagreement D1 says must be reported, never averaged away (the "
         "Newcombe delta straddles 0 here, so the gate is NULL while the "
         "primary estimand's interval still excludes 0 — the two are "
         "different questions and the rendering must not conflate them)",
         "b", 0, 4, 0, 0, 4, "NULL", "T2"),
    ]


def cmd_dryrun(_args) -> int:
    rc = 0
    for (title, arm, dg_o, dg_e, vague, errors, misattr,
         want_verdict, want_band) in dryrun_scenarios():
        original = synthetic_rows(arm, ORIGINAL_PAIR_IDS, dg_o)
        extension = synthetic_rows(arm, EXTENSION_PAIR_IDS, dg_e, vague=vague,
                                   errors=errors, misattributed=misattr)
        sv = surface_verdict(original, extension)
        print(f"\n{'=' * 72}\nSCENARIO: {title}\n"
              f"  surface={ARMS[arm]}  expects={want_verdict} / {want_band}"
              f"\n{'=' * 72}")
        print_surface(arm, sv)
        got_band = sv["rows"]["combined"]["band"]
        if sv["verdict"] != want_verdict or got_band != want_band:
            print(f"\n  DRY-RUN FAILURE: expected {want_verdict}/{want_band}, "
                  f"got {sv['verdict']}/{got_band}")
            rc = 1
    print(f"\n{'=' * 72}")
    print("dry-run: the gate and the D4 rendering behave exactly as "
          "pre-committed — safe to spend" if not rc else
          "dry-run: FAILED — do not spend")
    return rc


# --- paid: incremental doc generation (D5) -----------------------------------

def _complete(entry: dict | None) -> bool:
    return bool(entry) and all(k in entry and entry[k]
                               for k in ("x", "y_completing", "y_null"))


def cmd_gen_docs(args) -> int:
    from client import GENERATOR, GENERATOR_TEMPERATURE, BudgetExceeded, chat
    corpus = load_corpus()
    docs = json.loads(DOCS_PATH.read_text()) if DOCS_PATH.exists() else {}
    _assert_pooling_preconditions(docs, "pre-flight")

    todo = [p for p in corpus["pairs"]
            if p["pair_id"] in EXTENSION_PAIR_IDS
            and not _complete(docs.get(p["pair_id"]))]
    print(f"gen-docs: {len(docs)} pairs present, {len(todo)} extension pairs "
          f"to generate")
    if not todo:
        print("  nothing to do — every extension pair already has a complete "
              "doc set")
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
        print(f"  M1C spend to date: ${total:.4f} / ${CAP_M1C_TOTAL:.2f}")

    # The guard runs again on the exact object about to be written.
    _assert_pooling_preconditions(docs, "pre-write")
    docs = {p["pair_id"]: docs[p["pair_id"]] for p in corpus["pairs"]
            if p["pair_id"] in docs}
    rejected = sum(1 for r in log if r["violations"])
    rate = rejected / len(log) if log else 0.0
    DOCS_PATH.write_text(json.dumps(docs, indent=2) + "\n")
    GEN_LOG_M1C_PATH.write_text(json.dumps({
        "summary": {"generated_pairs": [p["pair_id"] for p in todo],
                    "attempts": len(log), "rejected_attempts": rejected,
                    "rejection_rate": round(rate, 3),
                    "incomplete": incomplete,
                    "cost": round(meter.total, 4), "generator": GENERATOR},
        "attempts": log}, indent=2) + "\n")
    print(f"gen-docs: {len(log)} attempts for {len(todo)} pairs, "
          f"rejection rate {rate:.1%}, cost ${meter.total:.4f}")
    print(f"  wrote {DOCS_PATH} ({len(docs)} pairs) and {GEN_LOG_M1C_PATH}")
    print("  M0 and M1 doc fixtures intact")
    if incomplete:
        print(f"  INCOMPLETE after 3 attempts: {incomplete}")
    return 1 if incomplete or rate > 0.6 else 0


# --- paid: trial waves --------------------------------------------------------

def _run_trial(arm, pair, cx, cy, docs_all, owners, meter):
    from client import BudgetExceeded, chat
    docs = trial_docs(arm, pair, cx, cy, docs_all)
    prompt = trial_text(arm, pair["question"], docs)
    row = {"pair_id": pair["pair_id"], "cell": cell_id(cx, cy),
           "model": MODEL, "arm": arm, "surface": ARMS[arm],
           "n_docs": len(docs)}
    try:
        resp = chat(MODEL, prompt, meter=meter)
    except BudgetExceeded:
        # A bound cap is a wave-control event, not trial data (M1's review
        # F1/F2): swallowed into an error row it would read as a transient API
        # failure and the top-up loop would keep spending.
        raise
    except Exception as e:  # noqa: BLE001 — error rows are data, and get topped up
        row.update(ok=False, error=f"{type(e).__name__}: {e}")
        return row
    row.update(ok=True, answer=resp["text"], cost=resp["cost"],
               prompt_tokens=resp["prompt_tokens"],
               completion_tokens=resp["completion_tokens"],
               finish_reason=resp["finish_reason"],
               scored=classify(resp["text"], pair, docs, owners))
    return row


def _usable_docs() -> dict:
    """The doc bank restricted to COMPLETE entries. Filtering the bank itself
    also protects the camouflaged filler draw, which indexes other pairs' x
    docs directly."""
    docs = json.loads(DOCS_PATH.read_text()) if DOCS_PATH.exists() else {}
    return {pid: entry for pid, entry in docs.items() if _complete(entry)}


def _load(path: Path, pair_ids: set[str] | None = None) -> list[dict]:
    """Deduplicate a wave log by (pair, cell), preferring the ok row.

    Optionally restricted to a scope of pairs — the verdict uses that to ingest
    M1's logs for the original rows without picking up anything else, and to
    keep the extension rows to p21-p80.
    """
    if not path.exists():
        return []
    best: dict = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("model") != MODEL:
            continue
        if pair_ids is not None and r["pair_id"] not in pair_ids:
            continue
        key = (r["pair_id"], r["cell"])
        if key not in best or (r.get("ok") and not best[key].get("ok")):
            best[key] = r
    return list(best.values())


def _extension_pairs(docs_all: dict) -> list[dict]:
    corpus = load_corpus()
    return [p for p in corpus["pairs"]
            if p["pair_id"] in EXTENSION_PAIR_IDS and p["pair_id"] in docs_all]


def cmd_smoke(args) -> int:
    """N=5 on the worst cell, to measure a per-trial rate before the wave.

    D3: smoke output is QUARANTINED — these trials never enter any N, and no
    wave or N decision keys off them. The summary below deliberately reports
    only what smoke exists to check (calls succeed, docs render, the detector
    runs, answers are grounded, cost per trial); it does not aggregate DG, even
    over 5 trials, because the one look is the verdict.
    """
    from client import BudgetExceeded
    arm = args.arm
    docs_all = _usable_docs()
    owners = owner_map(load_corpus())
    pairs = _extension_pairs(docs_all)[:SMOKE_N]
    if len(pairs) <= K_FILLER:
        print(f"HALT: only {len(pairs)} extension pairs have a complete doc "
              f"set — need > {K_FILLER}. Run `m1c.py gen-docs`.")
        return 1
    meter = open_meter(CAP_SMOKE)
    rows = []
    try:
        for pair in pairs:
            rows.append(_run_trial(arm, pair, "absent", "completing",
                                   docs_all, owners, meter))
    except BudgetExceeded as e:
        print(f"HALT: {e}")
    finally:
        record_spend("smoke", arm, meter.total)
    SMOKE_PATH[arm].write_text("".join(json.dumps(r) + "\n" for r in rows))
    ok_rows = [r for r in rows if r.get("ok")]
    if not ok_rows:
        print("NO-GO: no successful trials to measure a rate from")
        return 1
    vague = sum(1 for r in ok_rows if r["scored"]["label"] == "vague")
    grounded = sum(1 for r in ok_rows if r["scored"]["grounded"])
    mean = sum(r["cost"] for r in ok_rows) / len(ok_rows)
    print(f"smoke M1C{arm} ({ARMS[arm]}): {len(ok_rows)}/{len(rows)} ok, "
          f"{len(ok_rows) - vague} clean / {vague} vague, "
          f"{grounded}/{len(ok_rows)} grounded, ${mean:.6f}/trial")
    print("  (DG output quarantined by D3 — written to the log, not summarized)")
    print(f"smoke cost: ${meter.total:.4f} (cap ${CAP_SMOKE}) — M1C spend to "
          f"date ${spent_so_far():.4f} / ${CAP_M1C_TOTAL:.2f}")
    n_wave = N_EXTENSION * len(M1C_CELLS)
    projected = mean * n_wave
    cap = CAP_WAVE[arm]
    go = projected < cap
    print(f"measured rate ${mean:.6f}/trial x {n_wave} wave trials = "
          f"${projected:.4f} vs cap ${cap:.2f} — {'GO' if go else 'NO-GO'}")
    return 0 if go else 1


def cmd_wave(args) -> int:
    from client import BudgetExceeded
    arm = args.arm
    docs_all = _usable_docs()
    owners = owner_map(load_corpus())
    pairs = _extension_pairs(docs_all)
    if len(pairs) < N_EXTENSION:
        print(f"HALT: only {len(pairs)}/{N_EXTENSION} extension pairs have a "
              f"COMPLETE doc set — run `m1c.py gen-docs` first, or the combined "
              f"N cannot reach {N_CLEAN_REQUIRED_M1C} and the verdict "
              f"auto-reports UNDERPOWERED")
        return 1
    path = WAVE_PATH[arm]
    meter = open_meter(CAP_WAVE[arm])
    n_new = 0
    cap_bound = False

    # Top-up policy, inherited from M1-BRIEF D4 and bounded by D3: resumable,
    # re-running ERRORED trials only — a clean or scored trial is never
    # re-rolled — and keyed on ok/errored, never on a DG label.
    try:
        with path.open("a") as fh:
            for attempt in range(1, args.passes + 1):
                done = {(r["pair_id"], r["cell"])
                        for r in _load(path, EXTENSION_PAIR_IDS) if r.get("ok")}
                todo = [(pair, cx, cy) for pair in pairs
                        for cx, cy in M1C_CELLS
                        if (pair["pair_id"], cell_id(cx, cy)) not in done]
                if not todo:
                    break
                print(f"pass {attempt}: {len(todo)} trials to run "
                      f"({len(done)} already ok)")
                try:
                    for pair, cx, cy in todo:
                        fh.write(json.dumps(_run_trial(
                            arm, pair, cx, cy, docs_all, owners, meter)) + "\n")
                        fh.flush()
                        n_new += 1
                except BudgetExceeded as e:
                    print(f"HALT: {e} — budget cap bound before the wave "
                          f"completed; no further passes")
                    cap_bound = True
                    break
    finally:
        # In a `finally` deliberately: this ledger is the sole enforcement of
        # the pre-committed $0.10 ceiling. Spend that already happened must be
        # recorded even if the wave dies mid-run.
        total = record_spend("wave", arm, meter.total)

    rows = _load(path, EXTENSION_PAIR_IDS)
    n_ok = sum(1 for r in rows if r.get("ok"))
    print(f"wave M1C{arm}: {n_new} calls this run, {n_ok}/{len(rows)} trials "
          f"ok, cost ${meter.total:.4f} (cap ${CAP_WAVE[arm]}) — M1C spend to "
          f"date ${total:.4f} / ${CAP_M1C_TOTAL:.2f}")
    if cap_bound:
        print(f"  wave TRUNCATED BY BUDGET, not by API failure — any gated "
              f"cell short of {N_CLEAN_REQUIRED_M1C} combined clean will "
              f"auto-report UNDERPOWERED with the shortfall stated (D3)")
    still = [r for r in rows if not r.get("ok")]
    if still:
        print(f"  {len(still)} trials still errored after {args.passes} passes "
              f"— the gate will report the resulting power honestly")
    return 0


def cmd_verdict(_args) -> int:
    """The ONE look (D3). Everything before this point logs; this aggregates."""
    # Same guard m1.py and m0.py now carry, one milestone forward (PR #12
    # review F2's note): `run_fidelity` counts render traps over every pair
    # that has docs, so an M2-sized corpus would rewrite M1C's published
    # fidelity beside M1C's 80-pair cell counts.
    if _corpus.N_PAIRS != N_PAIRS_M1C:
        raise SystemExit(
            f"HALT: corpus.N_PAIRS is {_corpus.N_PAIRS}, not M1C's "
            f"{N_PAIRS_M1C}. M1C's verdict cannot be re-rendered against a "
            f"grown corpus. data/m1c_verdict.json stands as the record; read "
            f"it, do not regenerate it.")
    _assert_pooling_preconditions(when="verdict")
    surfaces = {}
    for arm in sorted(ARMS):
        original = _load(M1_WAVE_PATH[arm], ORIGINAL_PAIR_IDS)
        extension = _load(WAVE_PATH[arm], EXTENSION_PAIR_IDS)
        if not extension:
            print(f"no M1C wave data at {WAVE_PATH[arm]}")
            return 1
        if not original:
            print(f"no M1 wave data for {MODEL} at {M1_WAVE_PATH[arm]} — the "
                  f"combined rows cannot be formed")
            return 1
        surfaces[arm] = surface_verdict(original, extension)

    fid_ok, fid_n, _ = run_fidelity()
    v = {"model": MODEL, "floor": FLOOR,
         "n_clean_required": N_CLEAN_REQUIRED_M1C,
         "n_original": N_ORIGINAL, "n_extension": N_EXTENSION,
         "fidelity": [fid_ok, fid_n],
         "spend": json.loads(SPEND_PATH.read_text()) if SPEND_PATH.exists()
                  else {"total": 0.0, "cap_total": CAP_M1C_TOTAL, "entries": []},
         "surfaces": surfaces}
    print_verdict(v)
    VERDICT_PATH.write_text(json.dumps(v, indent=2) + "\n")
    print(f"\nwrote {VERDICT_PATH}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in [("ping", cmd_ping), ("fidelity", cmd_fidelity),
                     ("dryrun", cmd_dryrun), ("gen-docs", cmd_gen_docs),
                     ("smoke", cmd_smoke), ("wave", cmd_wave),
                     ("verdict", cmd_verdict)]:
        p = sub.add_parser(name)
        if name in ("smoke", "wave"):
            p.add_argument("--arm", choices=sorted(ARMS), required=True,
                           help="a = stark, b = camouflaged")
        if name == "wave":
            p.add_argument("--passes", type=int, default=3,
                           help="top-up passes over ERRORED trials only (D3)")
        if name == "gen-docs":
            p.add_argument("--dry-run", action="store_true",
                           help="report what would be generated, spend nothing")
        p.set_defaults(fn=fn)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
