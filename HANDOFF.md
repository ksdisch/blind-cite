# HANDOFF.md

_Last updated: 2026-08-04_

## What was just done
- **M1 built and run end to end (Option C, both arms), reviewed, merged** — PR #9, squash `e057c6d`. Gate verdict **NULL at both surfaces**; the flagship blindness contrast rendered on 2 answers (faithfulness PASS 2/2, citation PASS 2/2). ("Well-powered" was claimed at the time and is now withdrawn — see below.)
- **The paper was re-read, and the first re-read got it wrong.** It established correctly that the 66.3% anchor is Qwen2.5-7B's **peak** cell (`absent × synthetic_Y`), not ours — but then claimed no cell-matched anchor existed at all, and built a "prior-dependence, well-powered" headline on that. **Adversarial review (PR #10, F1/F2) caught it.**
- **The real anchor, verified first-hand:** the paper's **Appendix C, Figure 6** publishes per-cell DG matrices for **all 13 models**. For our exact model at our exact cell — **Qwen2.5-7B, `absent × prior_completing` — it is 14%** (and 61% at `synthetic_Y`).
- **Both headlines withdrawn (D16, D17).** Against 14%, *both* kin-model intervals contain it: stark 0/20 → [0.0%, 16.1%]; camouflaged 2/20 → [2.8%, 30.1%], exact binomial p = 0.455. **Our camouflaged result is consistent with the paper, not a refutation.**
- **The pre-registration gap, recorded as the project's main finding about itself (D18):** the pre-committed N≥20 came from M0's clean-**trial yield**, never from a power calculation against a target effect size. Against 14% it is underpowered; 0/25 would have been the minimum to exclude it.

## Where things stand
M0 FIT; M1's gate rendered NULL at both surfaces, but that verdict does **not** license "the phenomenon is absent" — at N=20/cell the study cannot resolve 14% from 0, and the one model with a published cell-matched anchor read a rate consistent with the paper. `main` carries M1 (PR #9). The corrections are on `docs/paper-cell-mapping-correction` (PR #10), mid-review: round 1 filed 2 critical + 3 should-fix + 3 nice-to-have, all accepted and fixed, awaiting re-verification. Total spend ≈$0.027 of the <$5 budget.

## Immediate next move
**Kyle's open call (D19).** D15 closed v1 on the premise that nothing informative remained to run; D16/D18 change that premise. Two paths:
1. **Close v1 on the honestly-underpowered result** — report the gate NULL, the 14% anchor, the consistency of the camouflaged result with the paper, and the sizing gap as the methodological finding.
2. **Run a pre-registered, power-sized extension** on `qwen-2.5-7b` (the only model with a published cell-matched anchor) to resolve 14% vs ~0. ≈$0.02 at measured rates, well inside the remaining $0.43 M1 ceiling. This is an **N-extension after seeing data** and is legitimate only if argued in an addendum, fixed in advance, and reported alongside the original N=20 result — never as a replacement for it.

Either way, `/research-paper` must compare to **14%**, not 66.3%, and use *"consistent with"*, never *"disappears"*. Then `/seed-hunt` for repro #6.

## Open questions / blockers
- **D19 is open and blocking the close.** Nothing else blocks.
- **The live scientific question:** does our kin-model rate actually differ from the paper's 14%? At N=20 we cannot tell. This is now the strongest remaining reason to spend anything.
- No cell-matched anchor exists for `llama-3.1-8b-instruct` or `gemma-3-12b-it` — the paper's Llama and Gemma entries are **different models** (Llama-3.1-70B, Gemma4-27B/31B). Their 0/20 results have nothing published to compare against.
- **Schema contradiction, flagged not resolved:** Figure 6 is RAG-4, Tables 1–2 are 10-tool. The paper claims <2pp difference at completing-Cy conditions, yet its calibration model reads 34% (Fig. 6) vs 67.0% (Table 1) at the same cell.
- Watch for an arXiv v2 (reference-only either way; re-read 2026-08-03/04, still v1, no code).
- Six nice-to-have follow-ups from PR #9's review; none blocks anything.

## Files touched recently
- `Wiki/Paper-Mapping.md` — **read this first.** The anchor table, both withdrawn headlines, the correction history, and what the data actually supports.
- `Decisions.md` — D16 (corrects D12), D17 (withdraws D13's headline), D18 (pre-registration gap), D19 (v1 closure back with Kyle); D12/D13 marked Superseded.
- `Wiki/Results.md`, `Wiki/Why-The-Null.md` — corrected; "well-powered" withdrawn throughout.
- `README.md`, `PROJECT.md`, `CLAUDE.md` — headline corrected to the 14% comparison.
- `docs/M1-BRIEF.md` — a correction pointer added above the post-run addendum; the addendum text itself left as the record of what was concluded at the time.
- `Wiki/History.md` — append-only; the PR #9 entry stands as written, the 2026-08-04 entry records both withdrawals.
