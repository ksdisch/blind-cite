# Why-The-Null

## Purpose
Explains what the M0 DG = 0/36 result actually means: what was measured, why the null is informative rather than a failure, what it does not rule out, and what M1 must change (or not) to be a valid next step. For anyone resuming the project who needs to understand the experimental state before writing `docs/M1-BRIEF.md`.

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

**Decision** (D5, **Unresolved** — `Decisions.md`): Whether M1 runs pre-committed (likely well-powered NULL headline, legitimate per the honesty contract) or with the camouflage variant is Kyle's call at the M1 brief.

### What M1 would need to change
**Fact** (`docs/M0-BRIEF.md` Pilot outcome, `Decisions.md` D3): M1 sizing is already computed from the M0 funnel: 20 pairs (clean-rate 100% at both absent cells; N≥20/cell/model). The `m1.py` script is pre-committed in structure (same subcommand pattern: `ping|gen-docs|smoke|pilot|verdict`).

**Inference** (from the discriminated-texture finding and the paper's design space, `docs/M0-BRIEF.md` D1): The paper's DG effect peaks at `absent × synthetic_Y` (73.1%), where the Y-doc is written to look as if it answers an X-question — the maximum camouflage condition. The M0 design uses `absent × completing` (Y's doc is honestly about Y) — a weaker camouflage. A M1 variant that introduces filler docs (making the Y-doc one of several, reducing name-salience) or uses a more X-framed Y-doc would move the design toward the paper's high-DG cells.

**Unresolved** (from D5 and `HANDOFF.md`): The camouflage-variant path requires a documented design change in `docs/M1-BRIEF.md`. The pre-committed path runs as-is and would likely confirm the null with power. Both are valid outcomes per the honesty contract ("nulls are headlines").

### The grounding precondition (why K1 matters)
**Fact** (`docs/M0-BRIEF.md` D7, Pilot outcome): K1 (capability cliff kill trigger) requires grounding ≥6/12 at `complete × null_control`. All three models grounded at 12/12. This is the load-bearing precondition: without K1 passing, a low-DG result is uninterpretable — the model might just be incapable of RAG. K1 passing at ceiling means the DG null is interpretable as "capable models chose not to deceive" rather than "models cannot do RAG."

## Sources
- [`docs/M0-BRIEF.md`](../docs/M0-BRIEF.md) — D1 (paper DG definition), D3 (corpus design), D4 (retrieval design), D6 (detector taxonomy), D7 (K4 flag definition), Pilot outcome addendum
- [`Decisions.md`](../Decisions.md) — D3 (FIT verdict), D5 (M1 design, Unresolved)
- [`PROJECT.md`](../PROJECT.md) — Current status, Next actions
- [`HANDOFF.md`](../HANDOFF.md) — Immediate next move, Open questions
- [`detectors.py`](../detectors.py) — `classify()` label precedence (lines 127–136)

## Uncertainties & contradictions
- **Unresolved** (D5): M1 design path not chosen — pre-committed NULL vs. camouflage variant. This is the central open question for the project resume.
- **Unresolved**: The 18 discriminated answers include 7 "quiet" cases where Y's name appears incidentally. If M1 uses a design where Y's name is harder to notice (filler docs, shorter Y-doc), some quiet-discriminated cases might flip to DG. The M0 data does not predict the M1 flip rate.
- **Unresolved**: Whether an arXiv v2 of 2607.09349 ships code or appendices — reference-only either way per the honesty contract, but would inform the camouflage-variant design.

## Related pages
- [Detector-Design](Detector-Design.md)

## Relevance to current work
This project is parked at M0. The M1 design decision (D5) is the first action on resume. This page is the primary reference for understanding *why* M0's null result does not close the question, and what the two M1 paths would each yield. A returning reader should read this page before writing `docs/M1-BRIEF.md`.

_Last reviewed: 2026-07-26_
