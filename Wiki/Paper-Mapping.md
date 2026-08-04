# Paper-Mapping

## Purpose
How this project's factorial relates to arXiv 2607.09349's — and why **no cell of that paper matches the condition we ran**, so only directional statements are legitimate. Rewritten twice on 2026-08-04 after adversarial review caught first a false premise and then an over-correction; both are recorded below rather than hidden.

## Key understanding

### There is no cell-matched anchor. There is a nearest published cell, and it is a floor.

**Fact** (paper Appendix C, *"Full Cross-Model DG Rate Matrices and Profile Taxonomy"*; Figure 6, *"Complete cross-model DG rate matrices for 13 models (4-tool schema)"*; asset `2607.09349v1/figures/fig9_supp_matrices.png` read directly). At `Cx = absent`:

| model (paper) | null_ctrl | class_prox | ctx_adj | prior_completing | synthetic_Y |
|---|---|---|---|---|---|
| **Qwen2.5-7B** | 2% | 4% | 6% | **14%** | 61% |
| Llama-3.1-70B | 4% | 5% | 2% | 14% | 42% |
| Gemma4-27B-A4B | 0% | 0% | 1% | 6% | 21% |
| Gemma4-31B | 0% | 0% | 1% | 4% | 11% |
| L1-16B-A3B (calibration) | 5% | 15% | 17% | 34% | 77% |

**Three reasons that 14% is *not* "our cell", each verified, each pushing the comparison the same way — toward direction only, never a point estimate:**

1. **Our condition is off the paper's grid by definition.** Paper §4 defines *"prior_completing (clinical evidence **matching the baseline model's parametric prior for X**)"*, and Appendix A builds that block by eliciting from L1-16B-A3B: *"List the specific clinical evidence for [X] in [C]: trial names, NCT numbers…"*, keeping entities *"appearing in ≥3/8 samples"*. Our completing evidence is **fabricated tokens matching no prior whatsoever**. The paper has no cell for what we ran.
2. **The number is explicitly a lower bound.** Paper Table 2 caption: *"Absolute DG rates at completing-Cy conditions are **lower bounds for non-L1 models** (CITs calibrated to L1-16B-A3B's prior)"*, repeated in Appendix C Table 8 and Appendix F. So Qwen2.5-7B's true completing-Cy rate under its *own* calibrated stimuli is ≥ 14%, not 14%.
3. **Schema mismatch, in both directions.** Figure 6 is RAG-4; Tables 1–2 are 10-tool; **this project ran neither** (M1a is a plain document list, M1b is JSON tool-results with k=4 fillers). The paper claims *"DG changes by less than 2 pp at completing-Cy conditions"* across schemas, yet its own calibration model reads **34%** (Fig. 6) against **67.0%** (Table 1) at this very cell — a ~2× discrepancy at the exact point of comparison.

**Fact.** Sensitivity to (3) alone, computed with the repo's own tools: at p = 0.14, P(X≤2 | n=20) = 0.455; at p = 0.28, it is **0.053**. Any verb resting on that p-value is not robust to a caveat the paper's own numbers make live.

### What our data can and cannot say

**Fact** (`data/m1a_verdict.json`, `data/m1b_verdict.json`):

| `qwen-2.5-7b` at `absent × completing` | measured | Wilson 95% | vs. the 14% floor |
|---|---|---|---|
| M1a stark | 0/20 = 0.0% | [0.0%, 16.1%] | contains it |
| M1b camouflaged | 2/20 = 10.0% | [2.8%, 30.1%] | contains it |

**Can say (direction, hedged):** our measured rates sit at or below the nearest published floor for this model, while the paper's completing-Cy regime for it spans 14% → 61% depending on entity recognizability. **Cannot say:** that we reproduced it, that we contradicted it, or that the phenomenon "disappears". No point comparison is legitimate — the conditions differ definitionally, the anchor is a bound not a value, and the schemas differ. This is precisely the case the honesty contract already covers: *"direction + structure, never point estimates."*

**Fact (D18) — the finding about ourselves.** At N=20/cell we cannot resolve even the floor: 0/20 has a Wilson upper of 16.1%, above 14%, and **0/24 is the smallest run that would clear it** (upper 13.80%). The pre-committed N≥20 came from M0's clean-**trial-yield** funnel (the `m1_sizing()` function in `m0.py`, called by `cmd_verdict` — not a subcommand), never from a power calculation against a target effect size. It sized the wave for usable trials, not for detectable difference. That is the project's main methodological finding about itself, and it is the reason the extension under D19 is worth running.

### What survives about prior-dependence

**Fact** (paper §4, Appendix A): `synthetic_Y` fabricates Y's **name** while holding the completing information constant. **Fact** (paper §5.3, "Label-substitution experiment"): *"This is corroborated at scale: absent × synthetic_Y DG exceeds absent × prior_completing in 13/13 models (Wilcoxon signed-rank, W=91, p<0.001; median delta: 37.8 pp)"* — for Qwen2.5-7B specifically, 14% → 61%. Removing entity-label recognition **quadruples** DG for our kin model.

**Inference (low-to-moderate confidence, cross-study and confounded, and NOT a headline).** Our corpus fabricates Y's name — matching `synthetic_Y` on the recognition axis — *and* fabricates all the evidence, which neither paper cell does. If the name axis alone drove the effect we would expect something near 61%; we observe 0–10%, close to `prior_completing`'s 14% and far below `synthetic_Y`'s 61%. That pattern is **consistent with** completing information (the parametric prior) being the load-bearing factor, which is what the paper itself says: *"The model attributes evidence based on information content, not Y's entity-label recognition."*

**This is an explanation, not a measurement.** It is a cross-study comparison across different domains (clinical vs API docs), different corpora, different detectors (LLM judge vs token ownership) and different schemas, at N far too small to separate 14% from 0. It is offered as the most parsimonious reading, explicitly labelled **Inference**, and it is **not** the project's headline claim.

### The axis map, corrected

| axis | paper `prior_completing` | paper `synthetic_Y` | **ours** |
|---|---|---|---|
| alternate entity recognizable? | yes (real drug) | **no** (fabricated name) | **no** (fabricated) — *level with* synthetic_Y |
| evidence matches a prior about X? | **yes** (elicited from L1) | **yes** (identical content) | **no** (fabricated tokens) — **this is what puts our condition off the paper's grid entirely** |
| queried entity X real? | yes | yes | **no** (fabricated) — the paper never varies X |
| Qwen2.5-7B rate (paper) | 14% | 61% | 0/20 stark, 2/20 camouflaged |

**Fact:** the paper *does* test fabricated entities — `synthetic_Y` by definition, plus the anonymous-label substitution (§5.3 / Table 11, *"XC-9941"*) and Appendix F's `ENTITY_XYZZY_42`. What it never varies is the **queried** entity X, which is always a real drug.

**Inference.** The structural tension stands and is the honest methodological finding: **the property that makes our detector judge-free — fabricating both entities and all evidence — is the property that moves us off the paper's grid on the completing-information axis.** Reaching that axis needs evidence a model already believes, which forfeits exact token ownership (KICKOFF bar entry 4). Within this project's contract that axis is unreachable.

### Correction history (kept, not hidden)

**Fact.** The first version of this page (2026-08-03, commit `e550652`) asserted *"the paper publishes no per-cell breakdown for any non-calibration model"* and built a headline on it. That is **false** — Appendix C publishes complete per-cell matrices for all 13 models, and the re-read that produced the page stopped one appendix short of it. Caught by adversarial review on PR #10 (F1/F2), verified first-hand by reading the figure. Consequences: the "no cell-matched anchor exists" claim is withdrawn; the "remove the prior and it disappears — well-powered" headline is withdrawn; D12 and D13 are superseded by D16/D17.

**Fact.** The *second* version (2026-08-04, `93d14e0`) then over-corrected: it called 14% "our exact model at our exact cell" and published "consistent with the paper". Adversarial review round 2 (F9/F10) showed the cell is not ours by the paper's own §4/Appendix A definition, that the paper labels the figure a lower bound for non-L1 models, and that neither schema is one we ran. Third strike on the same failure mode — comparing our rate to a paper cell that is not the one we ran — so the comparison is now stated as direction-only, with no verb claiming agreement or disagreement.

**Fact.** An earlier error in the same lineage: the 66.3% figure carried since KICKOFF is Qwen2.5-7B's **peak** cell (`absent × synthetic_Y`, Table 2, 10-tool), not our gated cell. That withdrawal stands — it was correct, just incomplete, because the right anchor (14%) existed and was missed.

## Sources
- arXiv 2607.09349 (Caruzzo, Yoo, Kim), v1 2026-07-10 — §4 (Cy definitions), §5.1 R3/R4, §5.3 + Table 11 (anonymous label), §6, Table 1 (calibration model per-cell), Table 2 (cross-model **peak**), **Appendix C + Figure 6 (per-cell, all 13 models)**, Appendix A, Appendix F, limitations. Re-read 2026-08-03; Appendix C read 2026-08-04; still v1, no code.
- [`data/m1a_verdict.json`](../data/m1a_verdict.json), [`data/m1b_verdict.json`](../data/m1b_verdict.json), [`stats.py`](../stats.py) — our side of every comparison above
- [`docs/M0-BRIEF.md`](../docs/M0-BRIEF.md) D1 (the `completing ↔ prior_completing` mapping), D7 (sizing); [`docs/KICKOFF.md`](../docs/KICKOFF.md) (bar entry 4, honesty contract)

## Uncertainties & contradictions
- **Unresolved — the live one:** what our kin-model rate actually is. At N=20 the interval spans the nearest published floor either way. Resolving it needs a power-sized extension (D19), which is an N-extension after seeing data and must be pre-registered as such.
- **Contradiction (the paper's own, unresolved by us):** Table 2's caption calls completing-Cy absolutes lower bounds for non-L1 models, and the calibration model reads 34% (Fig. 6, RAG-4) vs 67.0% (Table 1, 10-tool) at the same cell despite a claimed <2pp schema effect. Both cut against treating 14% as a point value.
- **Unresolved:** no anchor of any kind exists for `llama-3.1-8b-instruct` or `gemma-3-12b-it` — the paper's Llama and Gemma entries are different models (Llama-3.1-70B, Gemma4-27B/31B).
- **Inference, not Fact:** that the absent parametric prior explains our low rate. We did not manipulate the prior, and the comparison that motivates the idea is cross-study and confounded.
- **Structural, not fixable here:** our condition is off the paper's grid because our evidence is fabricated. Reaching the paper's grid requires evidence a model already believes, which forfeits exact token ownership.

## Related pages
- [Results](Results.md) — the measured record
- [Why-The-Null](Why-The-Null.md) — what the results mean and what they do not rule out
- [Detector-Design](Detector-Design.md) — why judge-free scoring requires fabricated entities

## Relevance to current work
This page exists to stop a fourth iteration of one specific mistake: **comparing this project's rate against a paper cell that is not the one it ran.** Three published framings have already failed that way ("paper-contradicting", "prior-dependence / well-powered", "consistent with the paper at our exact cell"). A `/research-paper` session must state the relationship as **directional and hedged**, name the schema, carry the lower-bound caveat, and never attach a p-value to a point comparison. It is also the evidence base for D19, the approved power-sized extension.

_Last reviewed: 2026-08-04_
