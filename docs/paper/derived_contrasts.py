"""derived_contrasts.py — re-derive the paper's prose-only statistics and ASSERT
them against the committed record, then emit one JSON for the paper and the
figures to cite.

Run:  uv run docs/paper/derived_contrasts.py        (from the repo root)

Why this file exists
--------------------
`/research-paper` may state only numbers that are already recorded. Two classes
of number in this paper are recorded as *prose* rather than as a machine-rendered
field:

  1. the engagement (non-refusal) share at the adversarial cell per stage —
     "stark 35% on p01-p20 vs 65% on p21-p80; camouflaged 35% vs 55%", written in
     `docs/M1C-BRIEF.md` ("Limitations, stated"), `Decisions.md` D25,
     `Wiki/Results.md` and `Wiki/Why-The-Null.md`;
  2. the D2 sizing table's "0/N Wilson upper" column in `docs/M1C-BRIEF.md`
     (16.1% / 13.8% / 6.0% / 4.6% / 3.1%).

Rather than re-doing that arithmetic inline in the paper, this script recomputes
each one from counts parsed out of the committed verdict files — through the
repo's own `stats.py`, the same module the verdict scripts used — and asserts it
equals the prose-recorded value at the recorded precision. A mismatch is a
finding, not something to paper over: if ANY assertion fails the script raises
and writes nothing at all.

It also re-derives, and asserts against the committed record, every Wilson
interval and both Newcombe deltas the paper quotes. Those are already recorded
verbatim in `data/m1c_verdict.json`; re-deriving them is a check that the
paper's numeric spine and the repo's own statistics module still agree.

READS (all committed, read-only):
  data/m1c_verdict.json, data/m1a_verdict.json, data/m1b_verdict.json,
  data/m0_verdict.json
WRITES:
  docs/paper/derived_contrasts.json   (only if every assertion passes)

What this script computes
-------------------------
  * Wilson intervals, via stats.wilson, from recorded (k, n)          [asserted]
  * Newcombe deltas, via stats.newcombe_diff, from recorded counts    [asserted]
  * wilson(0, N) upper bounds for the D2 sizing table                 [asserted]
  * engagement share = (n - correct-refusal) / n, per surface/scope   [asserted]

What this script deliberately does NOT compute
----------------------------------------------
  * DG rates conditioned on engagement ("opportunity denominators", e.g. the
    0/7 -> 3/39 form raised as a nice-to-have follow-up in PR #12's review) and
    any Fisher/chi-square test between the two stages. Neither is recorded in
    any committed file in this repo, so neither is a number this paper may
    state. The engagement SHARE is recorded prose and is verified above; the
    conditioned rate is not, and is not manufactured here.
  * Any p-value, test statistic, or point comparison against a cell of
    arXiv 2607.09349. Forbidden by `Decisions.md` D21 and `docs/M1C-BRIEF.md` D4.
  * Any cross-surface test. M1C pre-registered none and none was performed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from stats import newcombe_diff, wilson  # noqa: E402  (after sys.path fix)

DATA = ROOT / "data"
OUT = Path(__file__).resolve().parent / "derived_contrasts.json"

ARM = "absentxcompleting"      # the adversarial (gated) cell
CTRL = "absentxnull_control"   # the paired control cell

# Prose-recorded engagement (non-refusal) share at the adversarial cell, in
# percent, keyed (surface, scope). Source: docs/M1C-BRIEF.md "Limitations,
# stated"; Decisions.md D25; Wiki/Results.md; Wiki/Why-The-Null.md. All four
# state the same four numbers.
RECORDED_ENGAGEMENT_PCT = {
    ("a", "original"): 35.0,        # stark, p01-p20
    ("a", "extension_only"): 65.0,  # stark, p21-p80
    ("b", "original"): 35.0,        # camouflaged, p01-p20
    ("b", "extension_only"): 55.0,  # camouflaged, p21-p80
}

# The "0/N Wilson upper" column of docs/M1C-BRIEF.md D2's sizing table, in
# percent. Also pinned by test_m1c_sizing.py::test_zero_k_uppers.
RECORDED_SIZING_UPPER_PCT = {20: 16.1, 24: 13.8, 60: 6.0, 80: 4.6, 120: 3.1}

SURFACE_NAME = {"a": "stark", "b": "camouflaged"}
SCOPES = ["original", "extension_only", "combined"]


def load(name: str) -> dict:
    with open(DATA / name) as fh:
        return json.load(fh)


def close(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def main() -> int:
    m1c = load("m1c_verdict.json")
    m1a = load("m1a_verdict.json")
    m1b = load("m1b_verdict.json")
    m0 = load("m0_verdict.json")

    out: dict = {
        "_provenance": {
            "generated_by": "docs/paper/derived_contrasts.py",
            "reads": ["data/m1c_verdict.json", "data/m1a_verdict.json",
                      "data/m1b_verdict.json", "data/m0_verdict.json"],
            "recomputed_through": "stats.py (wilson, newcombe_diff)",
            "every_value_below_is_asserted_equal_to_the_committed_record": True,
        },
        "primary": {},
        "secondary_newcombe": {},
        "engagement": {},
        "sizing_zero_k_upper_pct": {},
        "blindness": {},
        "m1_reference": {},
    }

    # --- 1. Primary estimand: Wilson intervals, all three scopes, both surfaces
    for s, sdat in m1c["surfaces"].items():
        for scope in SCOPES:
            row = sdat["rows"][scope]
            k, n = row["primary"]["k"], row["primary"]["n"]
            rec_lo = row["primary"]["wilson"]["lo"]
            rec_hi = row["primary"]["wilson"]["hi"]
            lo, hi = wilson(k, n)
            assert close(lo, rec_lo, 1e-12), (s, scope, "wilson lo", lo, rec_lo)
            assert close(hi, rec_hi, 1e-12), (s, scope, "wilson hi", hi, rec_hi)
            # the recorded k/n must match the recorded label counts for that cell
            assert row["dg"][ARM] == k, (s, scope, "dg != primary.k")
            assert row["clean"][ARM] == n, (s, scope, "clean != primary.n")
            out["primary"][f"{s}:{scope}"] = {
                "surface": SURFACE_NAME[s], "scope": scope,
                "k": k, "n": n,
                "rate_pct": round(100 * k / n, 1),
                "wilson_lo_pct": round(100 * lo, 1),
                "wilson_hi_pct": round(100 * hi, 1),
                "band": row["band"],
            }

    # --- 2. Secondary paired gate: Newcombe deltas at combined N
    for s, sdat in m1c["surfaces"].items():
        comb = sdat["rows"]["combined"]
        rec = sdat["newcombe_delta_combined"]
        d, lo, hi = newcombe_diff(comb["dg"][CTRL], comb["clean"][CTRL],
                                  comb["dg"][ARM], comb["clean"][ARM])
        assert close(d, rec["d"], 1e-12), (s, "newcombe d", d, rec["d"])
        assert close(lo, rec["lo"], 1e-12), (s, "newcombe lo", lo, rec["lo"])
        assert close(hi, rec["hi"], 1e-12), (s, "newcombe hi", hi, rec["hi"])
        assert (lo > 0 or hi < 0) == rec["excludes_zero"], (s, "excludes_zero")
        out["secondary_newcombe"][s] = {
            "surface": SURFACE_NAME[s],
            "d": round(d, 3), "lo": round(lo, 3), "hi": round(hi, 3),
            "excludes_zero": rec["excludes_zero"], "gate": sdat["verdict"],
        }

    # --- 3. Engagement (non-refusal) share -- the D25 prose statistic
    for (s, scope), recorded_pct in RECORDED_ENGAGEMENT_PCT.items():
        row = m1c["surfaces"][s]["rows"][scope]
        labels = row["labels"][ARM]
        n = row["clean"][ARM]
        assert sum(labels.values()) == n, (s, scope, "labels do not sum to n")
        pct = 100 * (n - labels.get("correct-refusal", 0)) / n
        assert close(pct, recorded_pct, 0.5), (s, scope, pct, recorded_pct)
        out["engagement"][f"{s}:{scope}"] = {
            "surface": SURFACE_NAME[s], "scope": scope,
            "engagement_pct": recorded_pct,   # the RECORDED value, now verified
        }
    # combined rows carry no prose-recorded engagement figure, so none is
    # emitted for them: the paper reports engagement per STAGE, which is what
    # D25 compares, and never invents a pooled figure the record does not hold.

    # --- 4. Label composition at the adversarial cell (counts, lifted verbatim)
    for s, sdat in m1c["surfaces"].items():
        for scope in SCOPES:
            row = sdat["rows"][scope]
            out.setdefault("labels", {})[f"{s}:{scope}"] = {
                "surface": SURFACE_NAME[s], "scope": scope,
                "n": row["clean"][ARM], "counts": row["labels"][ARM],
                "control_counts": row["labels"][CTRL],
            }

    # --- 5. D2 sizing table, "0/N Wilson upper" column
    for n, recorded_pct in RECORDED_SIZING_UPPER_PCT.items():
        pct = 100 * wilson(0, n)[1]
        assert close(pct, recorded_pct, 0.05), (n, pct, recorded_pct)
        out["sizing_zero_k_upper_pct"][str(n)] = recorded_pct
    # the floor the templates key on, lifted from the verdict file
    out["floor_pct"] = round(100 * m1c["floor"], 1)
    # D22/M1C-BRIEF D2: 24 is the smallest N whose 0/N upper clears the floor
    assert wilson(0, 23)[1] >= m1c["floor"] > wilson(0, 24)[1]
    out["smallest_n_clearing_floor"] = 24

    # --- 6. Blindness contrast: every DG answer passed both standard proxies
    total_dg = total_faith = total_cit = 0
    for s, sdat in m1c["surfaces"].items():
        bc = sdat["rows"]["combined"]["blindness_contrast"]
        assert bc["n_dg"] == bc["faithfulness_pass"] == bc["citation_pass"], s
        assert bc["n_dg"] == sdat["rows"]["combined"]["primary"]["k"], s
        out["blindness"][s] = {"surface": SURFACE_NAME[s], **bc}
        total_dg += bc["n_dg"]
        total_faith += bc["faithfulness_pass"]
        total_cit += bc["citation_pass"]
    out["blindness"]["total"] = {"n_dg": total_dg,
                                 "faithfulness_pass": total_faith,
                                 "citation_pass": total_cit}

    # --- 7. M1 / M0 reference values the paper quotes
    for name, v in (("m1a", m1a), ("m1b", m1b)):
        per_model = {}
        for model, md in v["models"].items():
            k = md["dg"][ARM]
            n = md["clean"][ARM]
            lo, hi = wilson(k, n)
            assert close(lo, md["dg_wilson_completing"]["lo"], 1e-12), (name, model)
            assert close(hi, md["dg_wilson_completing"]["hi"], 1e-12), (name, model)
            per_model[model] = {"k": k, "n": n,
                                "wilson_lo_pct": round(100 * lo, 1),
                                "wilson_hi_pct": round(100 * hi, 1),
                                "verdict": md["verdict"]}
        out["m1_reference"][name] = {"surface": v["surface"],
                                     "overall": v["overall"],
                                     "fidelity": v["fidelity"],
                                     "per_model": per_model}
    out["m0_reference"] = {"fit": m0["fit"], "fidelity": m0["fidelity"],
                           "generator_rejection_rate": m0["generator_rejection_rate"],
                           "pairs_needed": m0["m1_sizing"]["pairs_needed"]}

    # --- 8. Run quality + spend, lifted from the verdict/ledger files
    out["run_quality"] = {
        "fidelity": m1c["fidelity"],
        "n_clean_required": m1c["n_clean_required"],
        "spend_total": m1c["spend"]["total"],
        "spend_cap": m1c["spend"]["cap_total"],
    }

    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print(f"all assertions passed -> {OUT.relative_to(ROOT)}")
    print("\nengagement (non-refusal) share at absent x completing, per stage:")
    for key, v in out["engagement"].items():
        print(f"  {v['surface']:<12} {v['scope']:<15} {v['engagement_pct']:.0f}%")
    print("\nprimary estimand (DG-Y at absent x completing):")
    for key, v in out["primary"].items():
        print(f"  {v['surface']:<12} {v['scope']:<15} {v['k']}/{v['n']} = "
              f"{v['rate_pct']:.1f}%  Wilson [{v['wilson_lo_pct']:.1f}%, "
              f"{v['wilson_hi_pct']:.1f}%]  {v['band']}")
    print("\nsecondary paired Newcombe delta (completing - null_control), combined N:")
    for key, v in out["secondary_newcombe"].items():
        print(f"  {v['surface']:<12} d={v['d']:+.3f} [{v['lo']:+.3f}, {v['hi']:+.3f}]"
              f"  excludes_zero={v['excludes_zero']}  gate={v['gate']}")
    print("\n0/N Wilson upper (D2 sizing table), floor = "
          f"{out['floor_pct']:.0f}%:")
    for n, pct in out["sizing_zero_k_upper_pct"].items():
        print(f"  N={n:<4} {pct:.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
