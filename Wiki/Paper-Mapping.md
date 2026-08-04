# Paper-Mapping

## Purpose
Which cell of arXiv 2607.09349 our factorial corresponds to, what the paper's own published rate is for that cell **on our exact model**, and what our measurements do and do not establish against it. Rewritten 2026-08-04 after adversarial review caught a false premise in the first version of this page; the correction is recorded below rather than hidden.

## Key understanding

### The anchor: 14%, published, for our exact model at our exact cell

**Fact** (paper Appendix C, *"Full Cross-Model DG Rate Matrices and Profile Taxonomy"*; Figure 6, *"Complete cross-model DG rate matrices for 13 models (4-tool schema)"*; figure asset read directly at `2607.09349v1/figures/fig9_supp_matrices.png`, titled *"Cross-Model Failure Rate Matrices — RAG-4 Schema, 15 Conditions, n=3,960 per model (13 models)"*). At `Cx = absent`:

| model (paper) | null_ctrl | class_prox | ctx_adj | **prior_completing** | synthetic_Y |
|---|---|---|---|---|---|
| **Qwen2.5-7B** | 2% | 4% | 6% | **14%** | 61% |
| Llama-3.1-70B | 4% | 5% | 2% | 14% | 42% |
| Gemma4-27B-A4B | 0% | 0% | 1% | 6% | 21% |
| Gemma4-31B | 0% | 0% | 1% | 4% | 11% |
| L1-16B-A3B (calibration) | 5% | 15% | 17% | 34% | 77% |

**Fact:** our gated cell is `absent × completing`, mapped to `prior_completing` at `docs/M0-BRIEF.md` D1. **Fact:** of our three subjects, only `qwen/qwen-2.5-7b-instruct` is an exact match for a model in that figure. `meta-llama/llama-3.1-8b-instruct` is not Llama-3.1-**70B**; `google/gemma-3-12b-it` is not Gemma4-27B or Gemma4-31B. So exactly one cell-matched anchor exists for this project: **14%**.

### What our data actually says against that anchor

**Fact** (`data/m1a_verdict.json`, `data/m1b_verdict.json`, intervals from the repo's own `stats.wilson`; exact binomial computed alongside):

| our arm, `qwen-2.5-7b` at `absent × completing` | measured | Wilson 95% | contains 14%? | P(X≤k \| p=0.14, n=20) |
|---|---|---|---|---|
| M1a stark | 0/20 = 0.0% | [0.0%, 16.1%] | **yes** | 0.049 |
| M1b camouflaged | 2/20 = 10.0% | [2.8%, 30.1%] | **yes** | 0.455 |

**Inference (high confidence).** The camouflaged result is *consistent with the paper's published rate for the same model at the same cell* — 10% observed against 14% expected, p = 0.455. This is not a refutation. The stark result is marginally lower (p = 0.049) but its interval still contains 14%. **At N = 20 per cell this study cannot resolve 14% from 0**, and 0/25 would have been the minimum needed to exclude it (Wilson upper 13.3%).

**Inference — the methodological lesson.** The pre-committed N ≥ 20 was computed from M0's *clean-trial yield* (`m0.py m1_sizing`: clean-rate 100% ⇒ 20 pairs), never from a power calculation against a target effect size. That is a real gap in the pre-registration: it sized the wave for *usable trials*, not for *detectable difference*. Against a 14% rate it is underpowered, and the gate's NULL verdict — correct as a mechanical gate outcome, since the Newcombe delta straddles 0 — must not be read as "the phenomenon is absent."

### What survives about prior-dependence

**Fact** (paper §4, Appendix A): `synthetic_Y` fabricates Y's **name** while holding the completing information constant. **Fact** (paper §5.1 R3): *"absent × synthetic_Y DG exceeds absent × prior_completing in 13/13 models (Wilcoxon signed-rank, W=91, p<0.001; median delta: 37.8 pp, range: 6.5–54.9 pp)"* — for Qwen2.5-7B specifically, 14% → 61%. Removing entity-label recognition **quadruples** DG for our kin model.

**Inference (moderate confidence, cross-study and confounded).** Our corpus fabricates Y's name — matching `synthetic_Y` on the recognition axis — *and* fabricates all the evidence, which neither paper cell does. If the name axis alone drove the effect we would expect something near 61%; we observe 0–10%, close to `prior_completing`'s 14% and far below `synthetic_Y`'s 61%. That pattern is **consistent with** completing information (the parametric prior) being the load-bearing factor, which is what the paper itself says: *"The model attributes evidence based on information content, not Y's entity-label recognition."*

**This is an explanation, not a measurement.** It is a cross-study comparison across different domains (clinical vs API docs), different corpora, different detectors (LLM judge vs token ownership) and different schemas, at N far too small to separate 14% from 0. It is offered as the most parsimonious reading, explicitly labelled **Inference**, and it is **not** the project's headline claim.

### The axis map, corrected

| axis | paper `prior_completing` | paper `synthetic_Y` | **ours** |
|---|---|---|---|
| alternate entity recognizable? | yes (real drug) | **no** (fabricated name) | **no** (fabricated) — *equal to* synthetic_Y, not past it |
| evidence matches a prior about X? | **yes** (elicited from the model) | **yes** (identical content) | **no** (fabricated tokens) — off the paper's grid |
| queried entity X real? | yes | yes | **no** (fabricated) — the paper never varies X |
| Qwen2.5-7B rate (paper) | 14% | 61% | 0/20 stark, 2/20 camouflaged |

**Fact:** the paper *does* test fabricated entities — `synthetic_Y` by definition, plus the anonymous-label substitution (§5.3 / Table 11, *"XC-9941"*) and Appendix F's `ENTITY_XYZZY_42`. What it never varies is the **queried** entity X, which is always a real drug.

**Inference.** The structural tension stands and is the honest methodological finding: **the property that makes our detector judge-free — fabricating both entities and all evidence — is the property that moves us off the paper's grid on the completing-information axis.** Reaching that axis needs evidence a model already believes, which forfeits exact token ownership (KICKOFF bar entry 4). Within this project's contract that axis is unreachable.

### Correction history (kept, not hidden)

**Fact.** The first version of this page (2026-08-03, commit `e550652`) asserted *"the paper publishes no per-cell breakdown for any non-calibration model"* and built a headline on it. That is **false** — Appendix C publishes complete per-cell matrices for all 13 models, and the re-read that produced the page stopped one appendix short of it. Caught by adversarial review on PR #10 (F1/F2), verified first-hand by reading the figure. Consequences: the "no cell-matched anchor exists" claim is withdrawn; the "remove the prior and it disappears — well-powered" headline is withdrawn; D12 and D13 are superseded by D16/D17.

**Fact.** An earlier error in the same lineage: the 66.3% figure carried since KICKOFF is Qwen2.5-7B's **peak** cell (`absent × synthetic_Y`, Table 2, 10-tool), not our gated cell. That withdrawal stands — it was correct, just incomplete, because the right anchor (14%) existed and was missed.

## Sources
- arXiv 2607.09349 (Caruzzo, Yoo, Kim), v1 2026-07-10 — §4 (Cy definitions), §5.1 R3/R4, §5.3 + Table 11 (anonymous label), §6, Table 1 (calibration model per-cell), Table 2 (cross-model **peak**), **Appendix C + Figure 6 (per-cell, all 13 models)**, Appendix A, Appendix F, limitations. Re-read 2026-08-03; Appendix C read 2026-08-04; still v1, no code.
- [`data/m1a_verdict.json`](../data/m1a_verdict.json), [`data/m1b_verdict.json`](../data/m1b_verdict.json), [`stats.py`](../stats.py) — our side of every comparison above
- [`docs/M0-BRIEF.md`](../docs/M0-BRIEF.md) D1 (the `completing ↔ prior_completing` mapping), D7 (sizing); [`docs/KICKOFF.md`](../docs/KICKOFF.md) (bar entry 4, honesty contract)

## Uncertainties & contradictions
- **Unresolved — the live one:** whether our kin-model rate differs from the paper's 14%. At N=20 we cannot tell; the camouflaged interval contains it outright. Resolving it needs a power-sized extension (~N=100/cell), which would be an N-extension after seeing data and must be pre-registered as such or not done at all.
- **Unresolved:** no cell-matched anchor exists for `llama-3.1-8b-instruct` or `gemma-3-12b-it` — the paper's Llama and Gemma entries are different models. Their 0/20 results have nothing published to compare against.
- **Contradiction (schema):** Figure 6 is RAG-4; Table 1/Table 2 are 10-tool. The paper claims *"DG changes by less than 2 pp at completing-Cy conditions"* between schemas, yet L1-16B-A3B reads 34% (Fig. 6) vs 67.0% (Table 1) at `absent × prior_completing`. Flagged, not resolved; the 14% Qwen anchor is RAG-4 and the 10-tool value for that cell is not tabulated.
- **Inference, not Fact:** that the absent parametric prior explains our low rate. We did not manipulate the prior.

## Related pages
- [Results](Results.md) — the measured record
- [Why-The-Null](Why-The-Null.md) — what the results mean and what they do not rule out
- [Detector-Design](Detector-Design.md) — why judge-free scoring requires fabricated entities

## Relevance to current work
This page is the evidence base for the open call in `PROJECT.md`: whether to close v1 on an honestly-underpowered result, or run a pre-registered power-sized extension on the one cell-matched model. It also fixes what a `/research-paper` session must not repeat — the write-up's comparison is to **14%**, not 66.3%, and the supported verb is *"consistent with"*, not *"disappears"*.

_Last reviewed: 2026-08-04_
