# Why-The-Null

## Purpose
Explains what this project's null results actually mean: what was measured, why the nulls are informative rather than failures, and what they do not rule out. Written at M0 (DG = 0/36), extended after M1 tested the same question at a second, deliberately harder surface, corrected 2026-08-04 once review established the nearest published floor and withdrew every point comparison (D21) — and then **substantially overturned the same day by M1C** (D24).

> **Read this first.** The page keeps its name and its argument history on purpose, but its central claim no longer holds. At the pre-registered N=80 per gated cell per surface, **DG occurs at both surfaces** — the stark surface, which M1 measured at 0/20, reads 3/80 with a Wilson lower bound above zero. See ["What M1C answered"](#what-m1c-answered--2026-08-04) below. Everything above that section is preserved as the reasoning that was correct given the data available at the time; the sections it supersedes are marked inline.

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

**Fact** (`data/m1a_verdict.json`, `Decisions.md` D10): The pre-committed design at 20 pairs rendered a **NULL gate outcome** — DG 0/20 per model per cell, Wilson 95% upper 16.1% per model, engagement present (`discriminated` 30/60 at the adversarial cell). *"Well-powered" was claimed here and is withdrawn* (D17/D18): 16.1% does not exclude the nearest published 14% floor, so the M0 null reproduced at the same N, not at power.

**Fact** (`data/m1b_verdict.json`): The camouflage surface — JSON tool-result rendering, one constant title per doc, k=4 off-theme filler docs, the levers built precisely to defeat the name-salience described in the section above — also rendered a **NULL gate outcome**. DG was 0/20 for two models and **2/20** for `qwen-2.5-7b` (Newcombe +0.100 [−0.077, +0.301], straddles 0) — a rate at the nearest published floor for that model — though that cell is **not ours** and 14% is a lower bound at a schema we did not run, so only direction is reportable (D21).

**Inference — *superseded by M1C (D24)*.** As written at M1: "the 'what the null does NOT rule out' argument below was the right argument to make, and it was tested rather than left standing. Reducing name-salience did not unlock the phenomenon at this scale." The first half stands. The second does not: at N=80 DG occurs on *both* surfaces, including the un-camouflaged one, so "did not unlock the phenomenon" was a statement about N, not about name-salience.

**Fact** (`data/m1b_wave.jsonl`): those 2 DG answers are nonetheless the project's flagship artifact — faithfulness PASS 2/2 and citation PASS 2/2 while token ownership flags both. The mechanism the paper describes is real and demonstrable here; what these models do not show is the *rate*. See [Results](Results.md).

**Inference:** the "quiet discriminated" prediction below (that some quiet cases might flip to DG under harder camouflage) is weakly supported at best — `discriminated` fell from 30/60 stark to 15/60 camouflaged while DG rose only 0→2. The bulk of the change went to `correct-refusal` (30/60 → 43/60): under camouflage these models refuse *more*, rather than mis-attributing more. That is consistent with the pre-stated worry that a uniform-title synthetic surface may itself reinforce the refusal ceiling.

### What M1C answered — 2026-08-04

**Fact** (`data/m1c_verdict.json`, `Decisions.md` D24): the pre-registered extension took `qwen-2.5-7b` to **combined N=80 clean trials per gated cell per surface**, one look, analysis and report templates frozen in advance. **Stark: DG 3/80, Wilson [1.3%, 10.5%]. Camouflaged: DG 7/80, Wilson [4.3%, 17.0%].** Both lower bounds are above zero. 240/240 calls ok, zero vague, zero confabulation, fidelity 1068/1068, DG-any 0/160.

**Inference — this page's central claim does not survive.** M0 read 0/36 and M1 read 0/20 on the stark surface, and both were interpreted as "capable models chose not to deceive". At N=80 the same surface, same corpus construction, same detectors produce DG at [1.3%, 10.5%]. The M0 and M1 measurements were correct; the *inference* drawn from them — absence of the phenomenon — did not survive, much as D18 warned about the project's own sizing. It did not fail on N alone: the extension's pairs also elicited materially more engagement (D25), and the study separates neither effect from the other. Nothing here revises the K1/K4 reasoning: grounding was and is the precondition, and it held. What changes is that "chose not to deceive" was never established — at those Ns it could not have been.

**Inference — the surface argument survives in weakened form.** The camouflaged surface still reads higher than the stark one (7/80 vs 3/80), which is the direction the name-salience argument predicted. But the intervals overlap, M1C pre-registered **no** cross-surface test, and none was performed. The honest reading is that camouflage is not *required* for DG on this corpus — the stark surface produces it too — and that whether camouflage raises the rate remains untested.

**Inference — the "camouflage pushes models toward refusal" reading is weaker than it looked.** At M1 (N=20) refusal ran 65% at the adversarial cell on both surfaces. At M1C's combined N=80 it is 42% stark and 50% camouflaged. The ordering is preserved; the magnitude that made it look like a ceiling was not. Most of the change is stage heterogeneity (D25), not surface: the extension pairs elicit materially more engagement than M1's on *both* surfaces, for reasons this study does not establish.

### What the null still does not rule out
*(Written at M1, when there was a null to defend. Retained: the open questions below are still open, and M1C did not close any of them.)*

**Unresolved:** the camouflage levers were bundled, so no single lever is exonerated. Two documented escalations remain unrun and each needs its own argued addendum first (`docs/M1-BRIEF.md` D2): a frozen title pool assigned by post-shuffle doc *position*, and same-theme filler generation. Neither was slipped in after seeing the data.

**Fact — corrected 2026-08-03** (paper §4 + Appendix A, read directly; see [Paper-Mapping](Paper-Mapping.md)): `synthetic_Y` is **not** "a Y-doc written to look as if it answers an X-question", as this page previously stated. It is *"a pharmacologically plausible but non-existent drug name with identical completing information"* — the manipulation replaces Y's **name** with a fabricated one while holding the evidence constant. The paper's own explanation for why it scores highest: *"The model attributes evidence based on information content, not Y's entity-label recognition"* — a real drug name lets the model disambiguate; a fabricated one removes that.

**Inference (moderate confidence, confounded).** Our corpus fabricates **both** entities by construction (KICKOFF: "zero training-prior contamination"). On the entity-recognition axis we sit *level with* the paper's `synthetic_Y`, and our *evidence* is fabricated too, which no paper cell does. For our kin model the paper reads 14% at `prior_completing` and **61%** at `synthetic_Y`; we read 0–10%, near the former and far below the latter. That is *suggestive* that completing information is load-bearing — the paper's own claim — but it is a cross-study comparison at N far too small to establish anything, and it is labelled Inference, never a headline. See [Paper-Mapping](Paper-Mapping.md).

### The grounding precondition (why K1 matters)
**Fact** (`docs/M0-BRIEF.md` D7, Pilot outcome): K1 (capability cliff kill trigger) requires grounding ≥6/12 at `complete × null_control`. All three models grounded at 12/12. This is the load-bearing precondition: without K1 passing, a low-DG result is uninterpretable — the model might just be incapable of RAG. K1 passing at ceiling means the DG null is interpretable as "capable models chose not to deceive" rather than "models cannot do RAG."

## Sources
- [`docs/M0-BRIEF.md`](../docs/M0-BRIEF.md) — D1 (paper DG definition), D3 (corpus design), D4 (retrieval design), D6 (detector taxonomy), D7 (K4 flag definition), Pilot outcome addendum
- [`docs/M1-BRIEF.md`](../docs/M1-BRIEF.md) — D1–D4 (the two designs and their pre-stated limitations), "M1 outcome" addendum
- [`Decisions.md`](../Decisions.md) — D3 (FIT verdict), D5→D6 (Option C), D10 (M1 verdict), D16–D22 (the nearest-cell 14% floor, the three withdrawn headlines, the pre-registration gap, and D19's approved extension)
- [`PROJECT.md`](../PROJECT.md) — Current status, Next actions
- [`detectors.py`](../detectors.py) — `classify()` label precedence

## Uncertainties & contradictions
- **Resolved by M1C**: whether `qwen-2.5-7b`'s 2/20 at the camouflaged cell was real or noise. At N=80 it is 7/80, [4.3%, 17.0%], with the paired gate excluding zero. The phenomenon is present — its magnitude relative to any published cell remains unanswerable (D21).
- **Unresolved**: whether camouflage *raises* the DG rate. Both surfaces produce DG and their intervals overlap; M1C pre-registered no cross-surface test, so the surface factor stays descriptive.
- **Unresolved — and now the largest one (D25)**: why the extension pairs elicit materially more engagement than M1's (35% → 55–65% at the adversarial cell). Two sources are live: the pairs differ in hand-authored themes and generated prose, **and** repeat draws of the same prompt are not stable (D27). Both confound any reading of the M1-vs-M1C difference that is not purely about N.
- **Unresolved**: the "quiet discriminated might flip to DG" prediction from M0 is still not cleanly tested — under camouflage answers moved toward `correct-refusal` at M1, and M1C's stage heterogeneity makes the M1-vs-M1C label mix uninterpretable on this axis.
- **Unresolved**: an M1b null cannot be distinguished from M0's on the constant-title axis. Stated in `docs/M1-BRIEF.md` D2 *before* the run, not discovered after. (Moot for the null itself, which no longer holds; still live for any claim about *why* the rate is what it is.)
- **Unresolved**: Whether an arXiv v2 of 2607.09349 ships code or appendices — reference-only either way per the honesty contract.

## Related pages
- [Results](Results.md) — the full measured record these arguments rest on
- [Detector-Design](Detector-Design.md)

## Relevance to current work
**This page is now primarily a record of a corrected inference, and that is its main value to the write-up.** The measurements at M0 (0/36) and M1 (0/20 stark) were sound; the conclusion drawn from them — that these models "chose not to deceive" — was not licensed by the N, and M1C proved it on the project's own data. A write-up that quotes this page must quote the correction with it.

**Read [Paper-Mapping](Paper-Mapping.md) before trusting any comparison.** The paper has no cell for the condition we ran, and its nearest cell (14%) is a lower bound at a schema we did not run (D21) — so nothing here supports a point comparison in either direction, before or after M1C. What survives intact is the *structure*: K1 grounding is the load-bearing precondition and it held throughout; engagement was present at every stage; and the mechanism is demonstrable — ten DG answers, faithfulness PASS 10/10 and citation PASS 10/10.

_Last reviewed: 2026-08-04_
