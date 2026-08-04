# HANDOFF.md

_Last updated: 2026-08-04_

## What was just done
- **M1 built and run end to end (Option C, both arms), reviewed, merged** — PR #9, squash `e057c6d`. Gate verdict **NULL at both surfaces**; the flagship blindness contrast rendered on 2 answers (faithfulness PASS 2/2, citation PASS 2/2). ("Well-powered" was claimed at the time and is now withdrawn — see below.)
- **The paper was re-read, and the first re-read got it wrong.** It established correctly that the 66.3% anchor is Qwen2.5-7B's **peak** cell (`absent × synthetic_Y`), not ours — but then claimed no cell-matched anchor existed at all, and built a "prior-dependence, well-powered" headline on that. **Adversarial review (PR #10, F1/F2) caught it.**
- **The nearest published cell, verified first-hand:** the paper's **Appendix C, Figure 6** publishes per-cell DG matrices for **all 13 models**. For our model at the nearest cell — **Qwen2.5-7B, `absent × prior_completing` — 14%** (61% at `synthetic_Y`), RAG-4 schema, and stated as a lower bound.
- **Three headlines withdrawn, the third by review round 2 (D16, D17, D21).** The last one claimed 14% was "our exact cell" and our result "consistent with the paper". It is **not our cell**: §4/Appendix A define `prior_completing` by evidence elicited to match a model's prior for X, ours is fabricated; the paper calls the figure a **lower bound** for non-L1 models; and we ran neither of its schemas. Only a hedged **directional** statement is legitimate.
- **The pre-registration gap, recorded as the project's main finding about itself (D18):** the pre-committed N≥20 came from M0's clean-**trial yield**, never from a power calculation against a target effect size. Against the 14% floor it is underpowered; **0/24** is the smallest run that would clear it (Wilson upper 13.80%).

## Where things stand
M0 FIT; M1's gate rendered NULL at both surfaces, but that verdict does **not** license "the phenomenon is absent" — the paper has no cell for the condition we ran, its nearest cell is a lower bound at a schema we did not run, and at N=20/cell we cannot resolve even that floor. Direction only. `main` carries M1 (PR #9). The corrections are on `docs/paper-cell-mapping-correction` (PR #10), mid-review: round 1 filed 2 critical + 3 should-fix + 3 nice-to-have; round 2 verified 6, reopened 2, and added 7 more (1 critical). All accepted and fixed; round 3 pending. Total spend ≈$0.027 of the <$5 budget.

## Immediate next move
**Plan the extension (D19 — approved: "extend once and make it decisive").** D15's premise no longer held once D16/D18 landed, so v1 does not close here. The next session's deliverable is the **pre-registration**, not the wave:
- Target N derived from a **power calculation** against the 14% floor (and against a plausible higher value, given the lower-bound caveat and the ~2× schema discrepancy) — not from clean-trial yield, which is the mistake D18 records.
- An explicit **optional-stopping guard**: N fixed in advance, analysis pre-committed, one look.
- How the extension is reported **alongside** the original N=20 result, never replacing it, since this is an N-extension after seeing data.
- Scope: `qwen-2.5-7b` only (the sole model with any published anchor), both surfaces, and whether the corpus extension it needs preserves the frozen seed the way the 12→20 extension did.

Only after that: `/research-paper`, which must state the relationship **directionally**, name the schema, carry the lower-bound caveat, and attach no p-value to a point comparison. Then `/seed-hunt` for repro #6.

## Open questions / blockers
- **D19 is approved; the pre-registration is the blocker.** Nothing is built or spent until that session lands.
- **The live scientific question:** does our kin-model rate actually differ from the paper's 14%? At N=20 we cannot tell. This is now the strongest remaining reason to spend anything.
- No cell-matched anchor exists for `llama-3.1-8b-instruct` or `gemma-3-12b-it` — the paper's Llama and Gemma entries are **different models** (Llama-3.1-70B, Gemma4-27B/31B). Their 0/20 results have nothing published to compare against.
- **Schema contradiction, flagged not resolved:** Figure 6 is RAG-4, Tables 1–2 are 10-tool. The paper claims <2pp difference at completing-Cy conditions, yet its calibration model reads 34% (Fig. 6) vs 67.0% (Table 1) at the same cell.
- Watch for an arXiv v2 (reference-only either way; re-read 2026-08-03/04, still v1, no code).
- Six nice-to-have follow-ups from PR #9's review; none blocks anything.

## Files touched recently
- `Wiki/Paper-Mapping.md` — **read this first.** Why no paper cell matches our condition, the nearest-cell table, all three withdrawn headlines, and what the data can and cannot say.
- `Decisions.md` — D16 (corrects D12), D17 (withdraws D13), D18 (pre-registration gap), D19 (**approved:** extend), D20 (corrects D14's rationale), D21 (withdraws D17 — no point comparison is legitimate), D22 (numeric/attribution corrections). D12/D13/D14/D15 marked Superseded.
- `Wiki/Results.md`, `Wiki/Why-The-Null.md` — corrected. Note "well-powered" still stands unannotated in frozen/append-only records (`Decisions.md` D10, `Wiki/History.md`'s PR #9 entry) by design; D17/D18/D22 withdraw it rather than rewriting history.
- `README.md`, `PROJECT.md`, `CLAUDE.md` — headline corrected to a hedged directional statement; no point comparison anywhere.
- `docs/M1-BRIEF.md` — a correction pointer added above the post-run addendum; the addendum text itself left as the record of what was concluded at the time.
- `Wiki/History.md` — append-only; the PR #9 entry stands as written, the 2026-08-03/04 entry records all three withdrawals.
