# Results

## Purpose
Every milestone's headline numbers in one place, with the pre-registered prediction beside the observed outcome. Synthesizes across `docs/M0-BRIEF.md`, `docs/M1-BRIEF.md`, `docs/M1C-BRIEF.md` and the four machine-rendered verdict files, none of which hold the whole picture on their own. For anyone who needs the project's measured record without reading three briefs and four JSON files.

## Key understanding

### M1C — the pre-registered extension, and the headline it produced

**Fact** (`data/m1c_verdict.json`, rendered once by `m1c.py verdict` per the D3 one-look guard): combined **N=80** clean trials per gated cell per surface on `qwen-2.5-7b`, the one roster model with any published anchor. All three pre-committed rows, per surface:

| surface | original (N=20) | extension-only (N=60) | **combined (N=80)** | template |
|---|---|---|---|---|
| stark | 0/20 [0.0%, 16.1%] → T0 | 3/60 [1.7%, 13.7%] → T2 | **3/80 [1.3%, 10.5%]** | **T2** — occurs, low |
| camouflaged | 2/20 [2.8%, 30.1%] → T3 | 5/60 [3.6%, 18.1%] → T3 | **7/80 [4.3%, 17.0%]** | **T3** — comparable magnitude, hedged |

Extension-only and combined selected the **same** template on each surface, so D1's side-by-side clause did not fire; the combined statement is carried alone and all three rows are recorded regardless.

**Fact** (same file): 240/240 M1C calls ok on the first pass; zero errored, zero vague, zero confabulation; doc generation 180 attempts / 0 rejections; fidelity gate **1068/1068**; **DG-any 0/160**; spend $0.0446 / $0.10. Both surfaces met `N_CLEAN_REQUIRED_M1C = 80` exactly, so neither reports UNDERPOWERED. The original rows re-derive `data/m1{a,b}_verdict.json` exactly, which is the ingestion check the combined estimand depends on.

**Fact — the headline.** The stark surface, where M1 measured **0/20** and reported a null, reads **3/80 with a Wilson lower bound of 1.3%** — above zero. **Inference:** M1's stark null did not survive the pre-registered extension. This is D18's self-diagnosis (the pre-committed N came from clean-trial yield, not a power calculation) bearing out on the project's own data — but **not on N alone**: the extension's pairs also elicited materially more engagement (D25), and this study separates neither effect from the other. M1's measurement is not withdrawn; the inference "DG ≈ 0 on this surface" drawn from it is (D24).

**Fact — the secondary gate, which disagrees with the primary on the stark arm.** Newcombe delta (completing − null_control) at combined N: stark **+0.037 [−0.015, +0.105]**, straddles 0 → gate NULL; camouflaged **+0.087 [+0.024, +0.170]**, excludes 0 → gate DG-EFFECT. **Inference:** these are two different questions and neither is presented as the other. DG-Y is impossible by construction at `absent × null_control` (the Y-null doc carries zero token-shaped strings), yet the Newcombe interval still carries the control cell's own Wilson width (0/80 → upper 4.6%) into the difference — wider, at k=3, than the arm cell's distance from zero. The paired test is therefore strictly the more conservative of the two here, and its stark NULL is not evidence against occurrence. `m1c.py dryrun` carried a scenario for exactly this case before any spend.

### The measured record

**Fact** (`data/m0_verdict.json`, `data/m1a_verdict.json`, `data/m1b_verdict.json` — all rendered mechanically by the verdict scripts):

| | M0 fit-pilot | M1a — stark | M1b — camouflaged |
|---|---|---|---|
| pairs × cells × models | 12 × 4 × 3 = 144 | 20 × 2 × 3 = 120 | 20 × 2 × 3 = 120 |
| calls ok | 144/144 | 120/120 | 120/120 |
| clean per gated cell | — (pilot, ungated) | 20/20 all models | 20/20 all models |
| **DG-Y at absent×completing** | **0/36** | **0/60** | **2/60** |
| DG-Y at absent×null_control | 0/36 | 0/60 | 0/60 |
| discriminated at absent×completing | 18/36 | 30/60 (7/8/15) | 15/60 (5/1/9) |
| correct-refusal at absent×completing | 18/36 | 30/60 | 43/60 |
| vague / confabulation | 0 / 0 | 0 / 0 | 0 / 0 |
| DG-any (fillers) | n/a (no fillers) | 0/120 | 0/120 |
| fidelity gate | 16/16 | 288/288 | 288/288 |
| gate verdict | **FIT** | **NULL** | **NULL** |
| vs. nearest published floor, 14% (qwen only; **not our cell**) | n/a | 0/20 — CI [0.0%, 16.1%] spans it | 2/20 — CI [2.8%, 30.1%] spans it |
| spend | ≈$0.009 | — | — (M1 total $0.0177) |

The M1C column is deliberately absent from this table: it covers **one model** at **three scopes per surface**, which does not fit a per-milestone column. Its full record is the [M1C section above](#m1c--the-pre-registered-extension-and-the-headline-it-produced), and it supersedes the M1 columns' *interpretation* — not their numbers, which stand as measured.

**Fact** (`data/m1a_verdict.json`, `data/m1b_verdict.json`): per-model Wilson 95% intervals on DG at the adversarial cell are [0.0%, 16.1%] for every model/arm except `qwen-2.5-7b` camouflaged, which is [2.8%, 30.1%] on 2/20. Pooled M1a 0/60 → [0.0%, 6.0%] (descriptive only; models are not exchangeable).

### Prediction vs. outcome

**Fact** (`docs/M0-BRIEF.md` Pilot outcome addendum, written 2026-07-15 — *before* M1 ran): "as designed, M1 would very likely render a well-powered NULL." **Observed:** a NULL gate outcome on all three subjects at both surfaces. **But the "well-powered" half did not hold** (D18): the N was derived from clean-trial yield, not from power against a target effect size, and against the nearest published 14% floor it is underpowered. The prediction was right about the verdict and wrong about what the verdict would license.

**Fact** (`docs/M1-BRIEF.md` D1): Option A's stated expected outcome was "DG 0/20 (or near) per model → NULL, well-powered", with the headline bound "DG ≤ 16.1% (95% Wilson upper)". **Observed:** 0/20 per model, bound 16.1%. The number written in the brief before the run is the number the run produced — but that bound was chosen when the assumed target was 66.3%, and it does not exclude the nearest published 14% floor (D18).

**Inference — *superseded by M1C (D24)*.** As written at M1, from D3 and the M1b result: "Option C's stated payoff was that *every* outcome would be a clean headline. The realized branch is DG≈0 at both surfaces." The payoff clause stands. The realized branch does not: at the pre-registered N=80 it is **DG occurs at both surfaces** on `qwen-2.5-7b`, the one model M1C extended (D23) — stark 3/80 [1.3%, 10.5%], camouflaged 7/80 [4.3%, 17.0%] (the table above). "DG≈0 at both surfaces" was a statement about N, not about the phenomenon.

**Contradiction — three framings withdrawn; [Paper-Mapping](Paper-Mapping.md) carries the full history.** (1) Comparing our 0/20 to "66.3% for Qwen2.5-7B" — that is the model's *peak* cell. (2) Claiming no per-cell breakdown exists — Appendix C publishes one for all 13 models. (3) Claiming 14% is "our exact cell" and our result "consistent with the paper" — it is **not our cell**.

**Fact.** The paper has **no cell for the condition we ran**: §4 and Appendix A define `prior_completing` as evidence elicited to match a model's parametric prior for X, and ours is fabricated tokens matching no prior. The nearest published cell — `Qwen2.5-7B, absent × prior_completing` = 14% (Fig. 6, **RAG-4** schema) — is additionally labelled a **lower bound for non-L1 models** (paper §5.2 body; Appendix C Table 8), and this project ran neither of the paper's schemas.

**What is reportable:** direction only, and after M1C only through the pre-committed D4 templates — **stark fired T2**, "occurs, low" (3/80 [1.3%, 10.5%], upper below the floor); **camouflaged fired T3**, "comparable magnitude, hedged" (7/80 [4.3%, 17.0%], interval reaching the floor). The pre-M1C wording here — "our rates (0/20 stark, 2/20 camouflaged) sit at or below the nearest published floor" — is **superseded by M1C (D24)**: it quotes the N=20 rates, and "at or below" is no longer true of the camouflaged surface, whose interval reaches ≥14%. The paper's completing-Cy regime for that model spans 14% → 61%. No point comparison, no p-value on one, no verb claiming agreement or disagreement (D21). `llama-3.1-8b-instruct` and `gemma-3-12b-it` are not the paper's Llama/Gemma models and have no anchor at all.

### The flagship artifact

**Fact** (`data/m1b_wave.jsonl`, pairs p14 and p18, model `qwen/qwen-2.5-7b-instruct`): two answers score `DG` — every one of the four evidence slots filled with Y's tokens, attributed to X *by name*, Y never mentioned, a genuinely retrieved doc cited. On both, the mechanical **faithfulness proxy PASSES and the citation proxy PASSES**. This is the blindness contrast the project exists to render: standard checks see nothing; token ownership sees everything.

**Fact** (`data/m1c_verdict.json`): at M1C's N=80 per surface the same contrast rests on **ten** answers — 3 stark and 7 camouflaged — with **faithfulness PASS 10/10 and citation PASS 10/10**. Not one DG answer on either surface was caught by either standard proxy.

**Inference:** at M1 n=2 was an existence proof, not a rate, and was reported as such. At M1C the artifact carries a rate interval on both surfaces (stark [1.3%, 10.5%], camouflaged [4.3%, 17.0%]) and the blindness is no longer a two-instance observation — it is 10/10 on every DG answer the study produced. The mechanism claim and the rate claim stay separate: the ten answers demonstrate the mechanism, the intervals bound the frequency.

### The surface factor

**Fact** (`data/m1_surface_contrast.json`): stark 0/20 vs camouflaged 2/20 for `qwen-2.5-7b`; 0/20 vs 0/20 for both others.

**Inference — *superseded by M1C (D24)*.** As written at M1: "every DG in the project appeared only at the camouflage surface and only on the paper's kin model — consistent with the M1-BRIEF E3 fidelity-gap reading, and far too small to support it. The cross-surface delta straddles 0." The hedge was right and the claim was not: at N=80 DG occurs at **both** surfaces — stark **3/80 [1.3%, 10.5%]**, camouflaged **7/80 [4.3%, 17.0%]** (the table at the top of this page). "Only at the camouflage surface" was a statement about N, not about surface. What survives is descriptive direction only: the camouflaged point rate remains the higher of the two. It is **not** established that the surfaces differ — the two intervals overlap, and M1C pre-registered **no** cross-surface test, so none was performed (`docs/M1C-BRIEF.md`; see Uncertainties below). The per-surface paired gates are not that test either: one excluding 0 while the other does not is a difference of significance, not a significant difference. The M1-era reading that the stark surface produces no DG is withdrawn. The `qwen-2.5-7b`-only half is untested at N=80: M1C extended that model alone (D23), so the other two remain at 0/20 with a 16.1% upper bound.

### Why DG-any reads zero and the split was still required

**Fact** (`data/m1b_verdict.json`): under k=4 off-theme fillers, DG-any is 0/120 — no model at either cell pulled a single third-party token. **Inference:** the detector split (see [Detector-Design](Detector-Design.md)) therefore never had to separate anything in practice, but was not optional: without it those trials could only have been scored `confabulation`, and the claim "no model grabbed filler evidence" would have been unavailable to make.

## Sources
- [`data/m0_verdict.json`](../data/m0_verdict.json), [`data/m1a_verdict.json`](../data/m1a_verdict.json), [`data/m1b_verdict.json`](../data/m1b_verdict.json), [`data/m1_surface_contrast.json`](../data/m1_surface_contrast.json), [`data/m1c_verdict.json`](../data/m1c_verdict.json) — machine-rendered verdicts, the primary record
- [`data/m1b_wave.jsonl`](../data/m1b_wave.jsonl), [`data/m1ca_wave.jsonl`](../data/m1ca_wave.jsonl), [`data/m1cb_wave.jsonl`](../data/m1cb_wave.jsonl) — the DG answer texts behind the flagship contrast
- [`docs/M0-BRIEF.md`](../docs/M0-BRIEF.md) — D7/D8 pre-commitments, Pilot outcome addendum (the M1 prediction)
- [`docs/M1-BRIEF.md`](../docs/M1-BRIEF.md) — D1–D4 pre-commitments, "The pick", "M1 outcome" addendum
- [`docs/M1C-BRIEF.md`](../docs/M1C-BRIEF.md) — the pre-registration (D1–D7: scope, sizing, one-look guard, the five report templates, corpus mechanics, budget, gates) and the "M1C outcome" addendum
- [`Decisions.md`](../Decisions.md) — D3 (FIT), D6 (Option C), D7–D11 (M1 run and verdict), D12–D22 (paper-mapping corrections, the withdrawn headlines, the pre-registration gap, and D19's approved extension), D23 (the M1C pre-registration), D24 (the M1C verdict), D25 (stage heterogeneity)

## Uncertainties & contradictions
- **Unresolved — the largest one, recorded as D25: stage heterogeneity.** Engagement (non-refusal) at the adversarial cell differs materially between M1's pairs and M1C's: stark **35% on p01–p20 vs 65% on p21–p80**; camouflaged **35% vs 55%**. The two stages are not behaviourally exchangeable and the combined row pools them. No mechanism is established, and there are **two** live sources of variation, not one: the pairs differ in hand-authored themes and generated prose, **and** repeat draws of the same prompt are not stable (D27). The claim that they "differ only in" theme and prose was wrong and is corrected (PR #12 review F3). The extension-only rows are reported beside the combined ones precisely so this is visible; the pre-registration forbids adjusting for it after the fact, and nothing was adjusted.
- **Resolved by M1C, recorded here because the older row below states it:** whether the 2 DG answers at M1 reflected a real effect or sampling noise. At N=80 the camouflaged interval is [4.3%, 17.0%] with the paired gate excluding 0, and the stark surface — 0/20 at M1 — reads 3/80 with a lower bound above zero. The phenomenon is present at both surfaces; what remains open is its magnitude relative to any published cell, which no comparison here can settle (D21).
- **Unresolved — repeat draws are not stable at `temperature = 0.0` (D27).** Of the 10 duplicate smoke-vs-wave trials M1C committed, **3 differ in answer text, 2 change label**, and **2 report different `prompt_tokens` for a byte-identical prompt** — provider routing is unpinned (`client.py` sends no `provider` preference and no seed). Visible in M1's data too (30 duplicates: 8 text differences, 2 label flips), so pre-existing. Consequence: **no committed rate in this repo is exactly reproducible by re-running its wave**, and repeat-draw noise is a second source of stage-to-stage variation alongside theme composition.
- **Unresolved:** the stark-vs-camouflaged difference (3/80 [1.3%, 10.5%] vs 7/80 [4.3%, 17.0%]) has overlapping intervals, and M1C pre-registered **no** cross-surface test, so none was performed. The surface factor stays descriptive.
- **Unresolved:** an M1b null cannot be distinguished from M0's on the constant-title axis — five byte-identical titles are themselves a synthetic-benchmark tell that may reinforce the refusal ceiling. Stated in `docs/M1-BRIEF.md` D2 *before* the run, not discovered after.
- **Unresolved:** the camouflage levers (JSON rendering, fillers, constant title) were bundled; no attribution among them is possible from this data.
- **Unresolved:** DG-Y is impossible by construction at absent×null_control (the Y-null doc has zero tokens), so the Newcombe delta is effectively a one-sample test of DG(completing) > 0. Stated in the brief so the gate is not oversold.

## Related pages
- [Why-The-Null](Why-The-Null.md) — what the nulls mean and what they do not rule out
- [Detector-Design](Detector-Design.md) — how each number above is produced mechanically
- [History](History.md) — the chronology these results sit in

## Relevance to current work
This is the table a write-up (`/research-paper`) is built from, and the measurement phase is now closed (D3's stopping rule binds after M1C). Every number here is traceable to a committed file. Four constraints carry into the write-up: report the paper relationship **only** through the M1C-BRIEF D4 templates — directional against a 14% floor at a non-matching cell and a schema we did not run, no point estimate, no verb claiming agreement or disagreement (D21); show **all three rows per surface**; keep the primary estimand and the secondary paired gate distinct; and carry **D25's stage heterogeneity in the body**, not a footnote.

_Last reviewed: 2026-08-04_
