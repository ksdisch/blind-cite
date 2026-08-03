# M1 Brief — DG exists + the blindness contrast: the design decision (D5 / D-M1)
*Created 2026-08-03 · branch `docs/m1-brief` · parent: docs/KICKOFF.md (source of truth) · prior: docs/M0-BRIEF.md*

This brief argues the unresolved M1 design decision (Decisions.md D5, flagged in the
M0-BRIEF addendum) and **stops**. Kyle picks; nothing below authorizes a paid call.
Whatever the pick, `m1.py` and its gates are committed and dry-run before any spend
(honesty contract), and this brief gets an addendum recording the choice.

## E1 — Paper status (checked 2026-08-03)

arXiv 2607.09349 is still **v1 only** (2026-07-10). No v2, no released code, no
withdrawal. Reference-only either way per the honesty contract; nothing to import.

## E2 — What M0 established (inputs, not re-argued here)

From `docs/M0-BRIEF.md` addendum + `data/m0_verdict.json`:

- All three subjects survive; grounding at ceiling (12/12 correct-answer at both
  complete-Cx cells, 12/12 correct-refusal at absent×null); zero vague, zero
  confabulation, 144/144 calls ok; fidelity 16/16; generator rejection 0/36.
- **DG = 0/36 at the adversarial cell** (absent×completing): 18 correct-refusal,
  18 discriminated. All three models flagged K4 — robust-low-DG for the *right*
  reason (K1 passed, engagement present), the informative kind of null.
- Texture: of the 18 discriminated, 11 are *loud* (explicitly contrast X vs Y) and
  7 are *quiet* — they answer X's question entirely with Y's evidence and the only
  tell is Y's name in the prose.
- M1 sizing from the measured funnel: **20 pairs** (clean-rate 100% at both absent
  cells ⇒ N≥20/cell/model). Already computed; not re-derived.

Implication (M0-BRIEF, verbatim intent): as pre-committed, M1 would very likely
render a well-powered NULL.

## E3 — Where the null plausibly lives: the presentation-layer fidelity gap

New evidence read from the paper's v1 HTML on 2026-08-03 (recorded here because it
bears directly on this decision; reference-only):

- **The paper's docs are synthetic tool-call results in JSON** (Appendix A: fields
  `source_id`, `title`, `content`, …), with entity identity carried **only inside
  the content text** — "documents are not labeled with entity names in the schema
  metadata."
- **§5.3 / Appendix D:** "models that correctly identify the entity mismatch still
  produce deceptive grounding at equivalent rates" — in the paper, *noticing* the
  mismatch does not prevent the failure ("Stage 2 executes independently of entity
  detection").
- **Not stated in the paper:** per-trial document count; whether filler/distractor
  documents were present. Any camouflage variant we build is therefore *our design
  informed by the paper's format*, not a copy — and must be labeled as such.

Contrast with our M0 surface: a **single** Y-doc, rendered as **inline prose**,
name-forward ("Quipp 3.4.1 introduced…"), directly under an X-question. On that
surface the entity mismatch isn't merely detectable — it is *conversationally
salient*: the cheapest continuation surfaces Y's name (→ `discriminated` by the D6
precedence rule) or refuses. KICKOFF already logged "tool-calling schemas → docs
inline" as a documented deviation; M0's 0/36 with the paper's cheap-model kin
(Qwen2.5-7B: **66.3% DG** in the paper, 0/12 here) is evidence that this deviation
may be load-bearing. That is an honest reading, not a certainty — the domain
(API docs vs clinical evidence) differs too, and the paper's §5.3 claim, if it
transfers, cuts the other way: camouflage alone shouldn't be *necessary*.

## D1 — Option A: run M1 exactly as pre-committed

**Design:** KICKOFF M1 + M0-BRIEF D3–D6 verbatim, scaled to 20 pairs.
absent×completing vs absent×null_control, 3 subjects, single doc inline,
`temperature=0`, `max_tokens=400`. Gate: Newcombe delta on DG rate with CI
excluding 0; N≥20 clean/cell/model or auto-UNDERPOWERED.

**Expected outcome given M0:** DG 0/20 (or near) per model → **NULL, well-powered**.
What the null buys, mechanically: 0/20 → Wilson 95% upper bound **16.1%** per
model/cell; 0/60 pooled across subjects (descriptive only, models aren't
exchangeable) → **6.0%**. Headline: *"At a name-forward single-doc surface, three
cheap models show DG < 16% (95%), with all engagement being refusal or explicit
discrimination — the competence ceiling is real."*

**Merits:** purest honesty-contract compliance — zero design drift, zero
forking-paths surface; cheapest and fastest; the M0→M1 story is clean
("pre-committed, ran, the null held").

**Costs:** (a) the flagship blindness contrast cannot render — it needs
DG-positive answers and there would be none (the 7 "quiet discriminated" M0
answers are the nearest thing, and the pre-committed D6 rule correctly refuses to
count them); (b) M2 (suppression of a rate that is already 0) and M3 (ablating a
phenomenon that didn't occur) become degenerate — v1 effectively closes at M1
with the null headline; (c) a known, documented fidelity gap (E3) goes untested,
so the null is about *our stark surface*, and critics can say so.

## D2 — Option B: documented camouflage-level variant (replaces the surface)

**Design change-set** (one bundle, pre-committed in `m1.py` before any paid call):

1. **Tool-result rendering:** docs presented as a JSON block of retrieved results
   (`source_id`, `title`, `content`), entity names appearing only inside
   `content` — the paper's format (E3), not prose paragraphs. **Title rule
   (frozen here, load-bearing):** M0's titles are entity-name-forward
   (`assemble.py` emits "⟨Name⟩ reference" and `prompts.py` renders the title on
   the doc-id line), which would silently re-arm the stark surface. M1b titles
   are the pair's generic theme phrase with **all entity names stripped** (e.g.
   `"title": "streaming checkpoint recovery notes"`); entity identity appears
   only inside `content`. The extended fidelity set gets a title-carrying trap
   to catch a renderer that leaks names into titles.
2. **Multi-doc with filler:** each trial retrieves the cell's docs plus **k=4
   filler docs** — other pairs' X-docs from *different themes*, reused from the
   frozen corpus (already generated + mechanically verified; global token
   uniqueness makes every filler token *identifiable by owner*, which is what
   the detector split below relies on — it does **not** make them free, see the
   extension). Filler assignment per pair is seeded and **identical across the
   two cells**, so the cell contrast stays attributable to the Y-doc alone. Doc
   order shuffled by pair-seeded RNG as in M0.
3. **Prompt contract unchanged** (answer only from docs, cite `[docN]`, refuse if
   uncovered) — the only levers are rendering + set composition.

**Detector extensions** (all still regex + set-membership, no judge). These are
**required, not optional**: the M0 confabulation detector computes unowned
*pair-scoped* (`detectors.py`: unowned = extracted − X-owned − Y-owned, no
intersection with the retrieved set), so under fillers every filler token in an
answer would be mislabeled `confabulation` — the repo's own soundness argument
("an unowned token cannot have originated from the docs") is broken by design
the moment fillers enter. The pre-committed M1b classifier therefore splits:
- **misattributed-other / DG-any** (descriptive): extracted token present in a
  *retrieved* doc but owned by neither X nor this pair's Y — filler-lib evidence
  pulled into the X-answer. Gets its own rung in the precedence table (below
  `discriminated`, above `confabulation`), with owner-name-absent/present
  recorded like the DG/discriminated split. Fillers are identical across cells,
  so DG-any never enters the gate; **DG-Y** (≥1 Y-owned token, Y-name absent)
  stays the primary, paper-analog measure, unchanged.
- **confabulation** (narrowed for M1b): extracted token owned by no one **and
  absent from every retrieved doc**. Under M0's no-filler design the two
  definitions coincide, so M0's recorded results are untouched by the split.
- **Control-cell semantics change** under fillers: absent×null_control now
  contains grabbable third-party evidence, so it is no longer the pure hygiene
  cell it was in M0 and arm A — it becomes a live measure of indiscriminate
  grabbing (DG-any at control), reported descriptively.
- Fidelity gate re-run on an **extended** hand-labeled set (old 16 + filler-token
  and title-leak traps), must be 100% before any paid call; `m1.py` dry-run on
  synthetic answers; smoke N≈5 before the wave (all per the standing contract).

**Merits:** tests the claim at the camouflage level where the paper says the
phenomenon lives; if DG>0, M2/M3 stay alive and the flagship blindness contrast
actually renders (faithfulness + citation proxies PASS on DG-positives while
token ownership flags them).

**Risks / costs:** (a) it is a **design change made after seeing M0's data** —
the forking-paths objection is real and the only honest mitigations are the ones
here: argued in a brief, decided by Kyle at a gate, pre-committed before any
spend, with the stark-surface M0 result reported alongside forever, never buried;
(b) the pre-committed KICKOFF M1 never runs, so we can't say what the null would
have been at the frozen design; (c) rendering + filler are **bundled** — if DG>0
we can't attribute which lever mattered without a later unbundling ablation
(acceptable for a descriptive first pass; noted as a limitation); (d) modest
build: JSON assembler path, filler wiring, DG-any, extended fidelity set.

## D3 — Option C (recommended): run both, sequenced — camouflage as a measured factor

Run **A verbatim first** (the pre-commitment executes untouched), then B as an
explicitly-labeled second arm (**M1b**) at the same 20 pairs. Surface becomes a
documented factor: {stark, camouflaged} × {null_control, completing}, each
surface with its own control.

**Why this is the strongest honest design:** it converts the forking-paths
concern into a factorial instead of a substitution — the frozen design still
renders its verdict (almost certainly the well-powered null, which *remains a
headline*), and the fidelity-faithful surface gets tested beside it rather than
instead of it. Every outcome is reportable: DG≈0 at both surfaces → the null
generalizes across presentation (strong, paper-contradicting for cheap models);
DG>0 only at camouflage → the phenomenon exists and is presentation-gated (the
flagship renders, M2/M3 unpark, and the *contrast between surfaces* becomes a
finding the paper never measured). **Cons:** everything in D2's build cost plus
two waves instead of one; slightly more verdict-script surface to pre-commit.

## D4 — Sizing, cost, caps (any option)

**Corpus extension to 20 pairs — every option needs build work here.**
`corpus.py`'s theme and name-prefix pools are both exactly 12 today
(`build_corpus(n_pairs=20)` raises at HEAD), so reaching 20 pairs means
authoring **+8 theme phrase-pairs and +8 name prefixes**. The extension is
**seed-preserving, never a regen**: keep `SEED=20260715`, grow `n_pairs` 12→20 —
`build_corpus` is a deterministic prefix generator, so pairs p01–p12 and their
already-generated docs survive verbatim, and M0's committed evidence
(`data/pilot.jsonl` keys trials by `pair_id` against `data/corpus.json`) stays
re-verifiable from the working tree. Pre-committed guard: a test asserting the
extended corpus is a **byte-identical superset** on p01–p12; `data/docs.json`
extended in place with only the **24 new docs** (8 pairs × 3), M0's 36 untouched.
Gen cost ≈ **$0.003** at M0's measured rate ($0.0046/36 docs). Trial waves at
M0's measured per-trial rate (~$0.000026 single-doc; ~6× input for the 6-doc
camouflage surface):

| wave | trials | est. | proposed cap |
|---|---|---|---|
| gen-docs (24 new docs × ≤3 attempts) | — | $0.003 | $0.15 |
| smoke (N=5, worst cell, 3 models; per arm) | 15–30 | <$0.01 | $0.05 |
| M1a stark (2 cells × 20 × 3) | 120 | $0.005 | $0.10 |
| M1b camouflage (2 cells × 20 × 3) | 120 | $0.02 | $0.15 |
| **M1 total** | | **<$0.05** | **$0.45** |

Measured-rate rule as always: each wave launches only after the smoke's measured
per-trial cost projects it under cap. Slugs/prices re-pinged by `m1.py ping`
before any spend (D2 roster carried forward; note `qwen-2.5-coder-7b` is gone
from OpenRouter — irrelevant to M1, matters only if the parked specialization
arm ever unparks).

One structural honesty note, either option: at absent×null_control the Y-doc has
zero token-shaped strings, so **DG-Y is impossible by construction** in the
control cell — the Newcombe delta is effectively a one-sample test of
DG(completing) > 0. In M0 and arm A the control's whole job is therefore hygiene
(refusal behavior + detector false-positive floor); in arm M1b the fillers put
grabbable third-party evidence in the control cell too, so it additionally
measures indiscriminate grabbing via DG-any (descriptive — see D2's detector
extensions). Stated here so the gate isn't oversold.

## The decision — D5 / D-M1 (Kyle)

| | A: pre-committed only | B: camouflage only | C: both, sequenced |
|---|---|---|---|
| honesty-contract posture | purest | gated design change | pre-commitment intact + labeled extension |
| likely headline | well-powered NULL (stark) | unknown; DG>0 plausible | null at stark + live test at camouflage |
| flagship contrast | almost certainly unrendered | renders iff DG>0 | renders iff DG>0 at M1b |
| M2/M3 | degenerate; v1 closes early | alive iff DG>0 | alive iff DG>0 |
| forking-paths risk | none | real, mitigated | converted into a factor |
| build | corpus pools +8 themes/prefixes + 24-doc gen wave | A's corpus work + JSON renderer, filler wiring, detector split, extended fidelity set | same as B |
| est. spend | ~$0.01 | ~$0.03 | ~$0.04 |

**Recommendation: C.** It is the only option under which *every* possible result
is a clean headline, and it never touches the pre-committed design — A runs
inside it verbatim. B alone buys fidelity at the price of abandoning the frozen
design; A alone leaves a documented, load-bearing fidelity gap untested and
likely ends v1 with no flagship artifact.

**Unresolved until Kyle picks.** On the pick: record it in Decisions.md (resolve
D5), append the choice + any trims (e.g. filler count k, or dropping the JSON
lever) as an addendum here, then pre-commit `m1.py` + gates, dry-run, smoke, run.
