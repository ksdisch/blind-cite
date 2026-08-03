# Why-The-Null

## Purpose
Explains what this project's null results actually mean: what was measured, why the nulls are informative rather than failures, and what they do not rule out. Written at M0 (DG = 0/36) and extended 2026-08-03 after M1 tested the same question at power and at a second, deliberately harder surface.

## Key understanding

### What was measured
**Fact** (`docs/M0-BRIEF.md` Pilot outcome, `Decisions.md` D3): The M0 fit-pilot ran 12 corpus pairs × 4 factorial cells × 3 models = 144 trials. The adversarial cell — the only cell where DG is possible — is `absent × completing`: no X-doc is retrieved, only Y's completing doc (which answers X's question shape using Y's tokens). DG was scored as 0/36 at that cell (12 pairs × 3 models).

**Fact** (`docs/M0-BRIEF.md` Pilot outcome): All 36 adversarial-cell trials were labeled either `correct-refusal` (18) or `discriminated` (18). Zero `DG` labels. Zero `vague`. Zero `confabulation`.

### Why the null is informative (K4 flag)
**Fact** (`docs/M0-BRIEF.md` D7, Pilot outcome): The K4 trigger is **not a kill** — it is a "robust-low-DG (right reason)" flag that a model survives with. All three subjects (Qwen-2.5-7B, Llama-3.1-8B, Gemma-3-12B) tripped K4.

The K4 flag fires when: K1 passes (grounding ≥6/12 at complete×null_control — the model CAN do RAG) AND the adversarial cell produces ≥10/12 refusals or discriminated answers. The logic: a model that refuses or names Y is engaging with the evidence and correctly not presenting it as X's. That is the right behavior. The null is informative *precisely because* K1 passed — the models are capable of grounding but chose not to deceive.

**Fact** (`docs/M0-BRIEF.md` Pilot outcome): Grounding at both complete-Cx cells was 12/12 (ceiling) for all three models — K1 is passed at full strength, not at the minimum threshold.

**Inference** (from the K4 definition and the pilot texture): The 18 discriminated answers are not uniform. 11/18 were "loud" — the model named both X and Y and explicitly contrasted them ("the documentation covers Vexenzi, not Vexalith"). 7/18 were "quiet" — the model filled all four evidence slots with Y's tokens but Y's name appeared in the prose (the one llama-3.1-8b answer that noted "I corrected 'Vexurak' to 'Vexenzi' as it seems to be a typo" is the extreme case). The pre-committed `discriminated` label covers both; reported DG is a floor.

### What the null does NOT rule out
**Inference** (from the experimental design, `docs/M0-BRIEF.md` D3, D4): The M0 corpus is a maximally name-forward design: each pair's X-doc and Y-doc have distinct 3-letter stems, distinct names that appear ≥2× each, and a Y-null doc that is entirely prose with zero token-shaped strings. The Y-completing doc presents Y's evidence clearly as Y's. On this surface, the name mismatch (question asks about X; only doc is about Y) is maximally visible. The null means cheap models notice a clear mismatch — not that they cannot deceptively ground on a harder surface.

**Fact** (`docs/M0-BRIEF.md` Pilot outcome addendum, `Decisions.md` D5): The M0-BRIEF addendum explicitly states: "as designed, M1 would very likely render a well-powered NULL" on the pre-committed design, and proposes a camouflage-level variant (e.g. multi-doc retrieval with filler docs) as an alternative that would make the Y-doc's name-mismatch less glaring — a design change that must be argued, not slipped in.

**Decision** (D5, resolved by **D6** — `Decisions.md`): M1 ran as Option C — the pre-committed design *and* a labeled camouflage arm, sequenced, so the frozen design rendered its own verdict rather than being replaced by the variant.

### What M1 answered — 2026-08-03

**Fact** (`data/m1a_verdict.json`, `Decisions.md` D10): The pre-committed design at 20 pairs rendered **NULL, well-powered** — DG 0/20 per model per cell, Wilson 95% upper 16.1% per model, engagement present (`discriminated` 30/60 at the adversarial cell). The M0 null was not an artifact of small N; it reproduced at power.

**Fact** (`data/m1b_verdict.json`): The camouflage surface — JSON tool-result rendering, one constant title per doc, k=4 off-theme filler docs, the levers built precisely to defeat the name-salience described in the section above — also rendered **NULL, well-powered**. DG was 0/20 for two models and **2/20** for `qwen-2.5-7b` (Newcombe +0.100 [−0.077, +0.301], straddles 0).

**Inference:** the "what the null does NOT rule out" argument below was the right argument to make, and it was tested rather than left standing. Reducing name-salience did not unlock the phenomenon at this scale. That is a stronger result than M0's, because the obvious alternative explanation was built and run rather than merely conceded.

**Fact** (`data/m1b_wave.jsonl`): those 2 DG answers are nonetheless the project's flagship artifact — faithfulness PASS 2/2 and citation PASS 2/2 while token ownership flags both. The mechanism the paper describes is real and demonstrable here; what these models do not show is the *rate*. See [Results](Results.md).

**Inference:** the "quiet discriminated" prediction below (that some quiet cases might flip to DG under harder camouflage) is weakly supported at best — `discriminated` fell from 30/60 stark to 15/60 camouflaged while DG rose only 0→2. The bulk of the change went to `correct-refusal` (30/60 → 43/60): under camouflage these models refuse *more*, rather than mis-attributing more. That is consistent with the pre-stated worry that a uniform-title synthetic surface may itself reinforce the refusal ceiling.

### What the null still does not rule out
**Unresolved:** the camouflage levers were bundled, so no single lever is exonerated. Two documented escalations remain unrun and each needs its own argued addendum first (`docs/M1-BRIEF.md` D2): a frozen title pool assigned by post-shuffle doc *position*, and same-theme filler generation. Neither was slipped in after seeing the data.

**Inference** (from the paper's design space, `docs/M0-BRIEF.md` D1): the paper's DG effect peaks at `absent × synthetic_Y` (73.1%) — a Y-doc written to look as if it answers an X-question. This project measures `absent × completing` (Y's doc is honestly about Y) at both surfaces. The `synthetic_Y` condition was never in scope (KICKOFF) and remains untested here.

### The grounding precondition (why K1 matters)
**Fact** (`docs/M0-BRIEF.md` D7, Pilot outcome): K1 (capability cliff kill trigger) requires grounding ≥6/12 at `complete × null_control`. All three models grounded at 12/12. This is the load-bearing precondition: without K1 passing, a low-DG result is uninterpretable — the model might just be incapable of RAG. K1 passing at ceiling means the DG null is interpretable as "capable models chose not to deceive" rather than "models cannot do RAG."

## Sources
- [`docs/M0-BRIEF.md`](../docs/M0-BRIEF.md) — D1 (paper DG definition), D3 (corpus design), D4 (retrieval design), D6 (detector taxonomy), D7 (K4 flag definition), Pilot outcome addendum
- [`docs/M1-BRIEF.md`](../docs/M1-BRIEF.md) — D1–D4 (the two designs and their pre-stated limitations), "M1 outcome" addendum
- [`Decisions.md`](../Decisions.md) — D3 (FIT verdict), D5→D6 (Option C), D10 (M1 verdict), D11 (close v1, Proposed)
- [`PROJECT.md`](../PROJECT.md) — Current status, Next actions
- [`detectors.py`](../detectors.py) — `classify()` label precedence

## Uncertainties & contradictions
- **Unresolved**: whether `qwen-2.5-7b`'s 2/20 at the camouflaged cell is a real surface effect or noise. n=2 cannot distinguish them and the pre-committed gate declines to try.
- **Unresolved**: the "quiet discriminated might flip to DG" prediction from M0 is only weakly supported — camouflage moved answers into `correct-refusal`, not into DG. Whether that is the constant-title tell or a genuine property of these models is untested.
- **Unresolved**: an M1b null cannot be distinguished from M0's on the constant-title axis. Stated in `docs/M1-BRIEF.md` D2 *before* the run, not discovered after.
- **Unresolved**: Whether an arXiv v2 of 2607.09349 ships code or appendices — reference-only either way per the honesty contract.

## Related pages
- [Results](Results.md) — the full measured record these arguments rest on
- [Detector-Design](Detector-Design.md)

## Relevance to current work
M0 and M1 are both closed. This page explains why two nulls are the project's headline rather than its failure, and why the M1b arm makes the M0 null stronger rather than merely repeating it. It is the argument a write-up (`/research-paper`) has to carry, and the reference for the open D11 call on whether v1 closes here.

_Last reviewed: 2026-08-03_
