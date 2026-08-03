# Paper-Mapping

## Purpose
Which cell of arXiv 2607.09349 our factorial actually corresponds to, and what the paper's stated mechanism implies about our null. Written 2026-08-03 after a direct re-read of the paper's §4, §5.3, Table 1, Table 2 and Appendix A, prompted by a suspected overclaim in the M1 write-up. It corrects a comparison that was wrong, and supplies a better explanation for the null than the one the M1 brief reached for.

## Key understanding

### The correction: our headline comparison was not cell-matched

**Fact** (paper Table 2, caption: *"Cross-model deceptive grounding rates. Peak DG rate (absent Cx × synthetic_Y), 10-tool schema"*): the **66.3%** figure for Qwen2.5-7B — carried since KICKOFF as our roster's directional anchor — is that model's **peak cell only**, `absent × synthetic_Y`. The paper publishes no per-cell breakdown for any non-calibration model.

**Fact** (paper Table 1, caption: *"Deceptive grounding rate by retrieval condition. L1-16B-A3B, 10-tool schema, n=264 triples per cell"*), at `Cx = absent`:

| Cy condition | DG |
|---|---|
| null_control | 26.5% |
| class_proximate | 49.2% |
| context_adjacent | 32.6% |
| prior_completing | **67.0%** |
| synthetic_Y | **73.1%** |

That breakdown is for **L1-16B-A3B**, the calibration model from which the completing-information targets were elicited — not for any model on our roster.

**Contradiction (resolved by withdrawal):** `Wiki/Results.md` and `README.md` compared our `0/20` against `66.3%` as if they were the same condition. They are not, and the intermediate claim "paper-contradicting for cheap models" was withdrawn on 2026-08-03. Note also that the paper's `null_control` shows **26.5%** DG, whereas ours is 0 *by construction* (the Y-null doc contains no token-shaped strings) — the two control cells are not the same instrument either.

### The deeper finding: our corpus removes the mechanism the paper's effect runs on

**Fact** (paper §4 / §5, quoted): the mechanism is prior-driven — *"Stage 1 opens when disease-context overlap activates a parametric attribution prior"*, and DG occurs because *"retrieved Y-documents are consistent with model expectations about X in context C, differing only at the entity level."* Domain fine-tuning amplifies it: *"Domain-specific fine-tuning loads stronger pharmacological class representations… increasing both Stage 1 susceptibility and Stage 2 risk."*

**Fact** (paper, on why `synthetic_Y` beats `prior_completing`): *"The model attributes evidence based on information content, not Y's entity-label recognition."* Recognizing a real alternate drug lets the model disambiguate; fabricating the name removes that check.

**Fact** (paper limitations): *"CITs were elicited from L1-16B-A3B by design, meaning absolute failure rates are anchored to that model's pharmacological prior."* The paper never tests entities absent from training data.

**Inference (high confidence).** Our design fabricates **both** entities *and* all their evidence, deliberately — it is KICKOFF bar entry 4, the property that makes the detector judge-free and contamination-proof ("a token can only enter an answer from a retrieved doc"). Mapped onto the paper's axes:

| axis | paper `prior_completing` | paper `synthetic_Y` | **ours** |
|---|---|---|---|
| alternate entity recognizable? | yes (real drug) | **no** (fabricated name) | **no** (fabricated) |
| evidence matches a prior about X? | **yes** (elicited from the model) | **yes** (identical content) | **no** (fabricated tokens) |
| DG (paper's calibration model) | 67.0% | 73.1% | — |

We are **past** `synthetic_Y` on the recognition axis and **off** the paper's grid entirely on the prior axis. There is no parametric attribution prior about `Vexurak` for disease-context overlap to activate, so by the paper's own account Stage 1 cannot open. Our null is therefore not a failed replication — it is a **boundary condition the paper's stated mechanism predicts**.

**Inference.** This also explains the M1b texture that the camouflage hypothesis did not: under heavier camouflage the models moved into `correct-refusal` (30→43 of 60) rather than into DG. With nothing in the retrieved evidence that the model already believes about X, the cheapest correct continuation is to decline — exactly what was observed.

**Inference.** The tension is structural, not a design flaw to fix: **the property that makes our detector judge-free is the property that removes the paper's mechanism.** Testing the prior axis needs entities the model knows, which reintroduces training contamination and forfeits exact token ownership — the one thing KICKOFF's honesty contract will not trade (bar entry 2: never an LLM judge). Within this project's contract, the prior axis is not reachable.

## Sources
- arXiv 2607.09349 (Caruzzo, Yoo, Kim), v1 2026-07-10 — §4 (factorial + Cy definitions), §5.3 + Appendix D (noticing does not prevent DG), Table 1 (per-cell, calibration model), Table 2 (cross-model peak), Appendix A (synthetic_Y construction), limitations. Re-read 2026-08-03; still v1, no code released.
- [`docs/M0-BRIEF.md`](../docs/M0-BRIEF.md) D1 — the original mapping (`completing ↔ prior_completing`), now known to be partial
- [`docs/KICKOFF.md`](../docs/KICKOFF.md) — bar entry 4 (fabricated corpus, zero contamination), the honesty contract
- [Results](Results.md), [Why-The-Null](Why-The-Null.md) — the artifacts this correction propagates into

## Uncertainties & contradictions
- **Unresolved:** the paper gives no `prior_completing` rate for Qwen2.5-7B or any other cross-model entry, so no cell-matched cheap-model anchor exists in the published tables. Our result cannot be compared like-for-like against any number the paper reports.
- **Unresolved:** whether DG would appear on our corpus if the *evidence* matched a prior while the entities stayed fabricated. Not reachable judge-free (see above), so untested and likely untestable within this contract.
- **Inference, not Fact:** that the absent parametric prior *causes* our null. It is consistent with the paper's mechanism, our two nulls, and the refusal shift — but we did not manipulate the prior, so this is an explanation, not a measurement.
- **Fact:** M0-BRIEF D1's mapping line (`completing ↔ prior_completing`) is a frozen pre-commitment and is **not** rewritten. This page records the correction; the historical brief stands as written.

## Related pages
- [Results](Results.md) — the measured record
- [Why-The-Null](Why-The-Null.md) — what the nulls mean
- [Detector-Design](Detector-Design.md) — why judge-free scoring requires fabricated entities

## Relevance to current work
This is the reframing the v1 write-up should be built on: not "the paper fails to replicate on cheap models" (unsupported at the cell level) but "**DG is prior-dependent; strip the parametric prior and it disappears — measured judge-free, well-powered, across two presentation surfaces and three models.**" It also retires the proposed `synthetic_Y` positive-control arm as redundant: our design already sits past that cell on the axis it manipulates.

_Last reviewed: 2026-08-03_
