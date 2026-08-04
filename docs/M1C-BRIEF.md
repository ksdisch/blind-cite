# M1C brief — pre-registered, power-sized extension on `qwen-2.5-7b`

**Status: COMMITTED pre-registration (D23, 2026-08-04).** The three argued
design points were ruled by Kyle in-session (see "The argument, ruled" below);
this document is the pre-registration D19 called for. **Nothing is built and
no dollar is spent until Kyle green-lights the build on this committed brief**
— the pre-registration is the deliverable (D19); the wave is a separate,
later act. Frozen from the moment the first paid call runs.

## Why this document exists, stated against ourselves

M1's pre-committed N≥20 came from M0's clean-**trial-yield** funnel
(`m1_sizing()` in `m0.py`), never from a power calculation against a target
effect size (D18). At N=20, 0/20 has a Wilson upper of 16.1% — above the 14%
nearest-published floor — so the study could not resolve even the floor. That
is the project's main methodological finding about itself.

This extension is therefore an **N-extension decided after seeing the data.**
The decision post-dates the M1 results and is documented as such: it was
triggered by the discovery of the Appendix C anchor (D16) and the power audit
(D18), not by the observed rate — but no reader is asked to take that on
faith, which is why the reporting rules below always show the extension-only
rows. The three guards that make an after-the-fact extension legitimate:

1. **Argued in advance** — this brief, approved before any build or spend.
2. **Fixed in advance, one look** — N, cells, analysis, and report templates
   are frozen here; the verdict script runs once, at the end.
3. **Reported alongside, never replacing** — the original N=20 result stands
   as published; every rendering shows original / extension-only / combined.

The D21 constraint governs everything below: **14% is a reference magnitude
for sizing and wording only — never a null hypothesis about our cell.** The
paper has no cell for our condition (fabricated evidence matches no parametric
prior; neither of its schemas is ours; the 14% is itself a stated lower
bound). No template below attaches a p-value to any comparison with the paper.

## D1 — Scope and estimand

- **Model:** `qwen/qwen-2.5-7b-instruct` only — the sole roster model with any
  published anchor (the paper's Llama/Gemma entries are different models).
- **Surfaces:** both — M1a stark (plain document list) and M1b camouflaged
  (JSON tool-results, constant titles, k=4 off-theme fillers). Unchanged from
  their pre-committed definitions; no design drift.
- **Cells:** both M1 cells per surface — `absent × completing` (gated) and
  `absent × null_control` (contamination guard + Newcombe base).
- **Primary estimand:** DG-Y rate at `absent × completing`, per surface, at
  the **combined** N, with Wilson 95% CI.
- **Secondary:** Newcombe delta (completing − null_control) per surface at
  combined N — the original M1 gate structure, kept intact.
- **Robustness rows (always shown):** the same quantities on extension-only
  data. If the combined and extension-only rows would select different
  templates under D4, the rendering carries **both** templates side by side,
  extension-only first — the disagreement is reported, never averaged away.
- **Everything else is out of scope.** No new models, no new cells, no schema
  changes, no detector changes.

## D2 — Sizing (the power calculation D18 said never happened)

Computed with the repo's own `stats.wilson`, and pinned: `test_m1c_sizing.py`
(committed alongside this brief) asserts every cell of the table below — the
`0/N` uppers, both endpoints of each T2 band, each "T3 starts at" k, and every
parenthesized point estimate — plus the power identities, so the table cannot
drift from the function that defines it. (PR #11 review round 1 caught one
hand-built row wrong — its F1 — which is exactly why the pin exists; the
parenthesized point estimates are asserted per its F13, and the T2 bands' lower
endpoints per its F13 residual.)

**Sizing question:** what combined N makes the *directional* statement
decisive — meaning every reachable outcome k maps to exactly one
pre-committed template, with no outcome left saying "cannot tell"?

| combined N | 0/N Wilson upper | T2 band (occurs, below floor) | T3 starts at |
|---|---|---|---|
| 20 (status quo) | 16.1% — **above the floor; the D18 gap** | none (empty band) | k=1 (5.0%) |
| 24 | 13.8% — bare exclusion only | none (empty band) | k=1 (4.2%) |
| 60 (+40 pairs) | 6.0% | k=1–3 | k=4 (6.7%) |
| **80 (+60 pairs)** | **4.6%** | **k=1–5** | **k=6 (7.5%)** |
| 120 (+100 pairs) | 3.1% | k=1–9 | k=10 (8.3%) |

Parenthesized percentages are point estimates k/N. "T3 starts at" marks the
first k whose interval reaches the floor; the T4 band (interval entirely above
the floor, D4) begins higher and is asserted in `test_m1c_sizing.py`.

- At **N=80**: k=0 → [0, 4.6%]; k=2 (the carried camouflaged events alone) →
  [0.7%, 8.7%]; k=5 → [2.7%, 13.8%]; k=6 → [3.5%, 15.4%]; k=8 (the 10% point
  estimate holding) → [5.2%, 18.5%]. Every k lands in exactly one template.
- **Sensitivity to the floor being a floor:** the paper's own calibration
  model reads 34% (Fig. 6, RAG-4) vs 67.0% (Table 1, 10-tool) at the same
  cell — a ~2× schema discrepancy. Sized against a doubled reference (~28%):
  if the true rate is at that magnitude, expected k ≈ 22/80 → CI ≈ [19%, 38%],
  decisively T4 (the whole interval above the floor). The sizing does not
  depend on 14% being exact.
- **Why not 24** (the bare-exclusion minimum): 0/24 clears the floor only if
  the extension observes zero events; the camouflaged cell already carries 2.
  The interesting deliverable is a **tight estimate**, not a bare exclusion.
- **Why not 120:** $0.034 more for template-band shifts that change no verb;
  and 100 new hand-authored themes materially raises corpus-quality risk.

**Pre-committed choice: combined N = 80 per cell per surface (E = +60 pairs).**

Power against the "does DG occur at all" direction: the Wilson lower bound is
> 0 iff k ≥ 1, so P(lo > 0) = 1 − (1−p)^N exactly — no simulation needed. At
N=80 that is 0.9998 if the true camouflaged rate is 10%, and 0.9835 if 5%
(both asserted in `test_m1c_sizing.py`). The carried k=2 makes the combined
lower bound > 0 certain for the camouflaged cell; the question N=80 answers
is *where the upper bound lands*.

## D3 — One-look guard (the optional-stopping pre-commitment)

- **N is fixed here.** E = 60 new pairs; target 80 clean trials per gated
  cell per surface, combined.
- **One look.** `m1c.py verdict` runs once, after the full wave. Per-trial
  detector labels are logged as each trial runs — the top-up loop needs
  clean-vs-vague, and the M1 pipeline scores in-trial (`classify` per row,
  D7) — so the blinding is **procedural, not mechanical**: no rate is
  aggregated before the verdict, no wave/N/top-up decision keys off a DG
  label (clean-vs-vague only), and the verdict run is the first aggregation.
  (Smoke checks pipeline mechanics — call success, doc fidelity, detector
  run — and its N≈5 DG output is quarantined: smoke trials never enter any N,
  and no wave/N decision keys off a smoke DG count.)
- **Clean-trial top-up, bounded and blind:** if clean yield < 100% (M1 ran
  240/240), top-up waves run only to reach the fixed N-clean target, still
  without aggregating DG. Top-up is capped by budget (D6); if the cap binds
  first, the verdict runs at the achieved N and auto-reports **UNDERPOWERED
  whenever combined clean N < 80 per gated cell per surface** — the
  M1C-specific threshold this brief pre-commits (`N_CLEAN_REQUIRED_M1C = 80`
  in `m1c.py`), with the shortfall stated. M1's inherited threshold of 20
  cannot flag a truncation anywhere in [20, 79], so it is explicitly **not**
  reused for this gate (the KICKOFF N≥20 floor remains as the outer bound).
- **No further extension, regardless of outcome.** Whatever M1C shows, any
  subsequent wave is a new pre-registered study with its own brief — never an
  M1C top-up. This clause is the stopping rule.

## D4 — Reporting: templates fixed verbatim, direction only

Every rendering of the M1C result shows **three rows** per surface per cell:
original (N=20), extension-only (N=60), combined (N=80) — the original is
never replaced, the extension-only is never hidden.

The directional statement is selected by where the Wilson CI on the primary
estimand lands. Exactly one template fires **per data row** (original /
extension-only / combined, per surface) — D1's side-by-side rule governs
which rows a rendering must show. The templates are the only permitted verbs,
and each carries its caveats inline so no downstream rendering can drop them
(the PR #10 review-F9 failure mode):

- **T0 — k=0 with CI reaching 14%:** "Zero DG observed on this surface (0/N,
  Wilson [0%, hi]) — an interval that reaches the floor's magnitude, so this
  row alone is uninformative against it (the D18 gap). Direction: at or below,
  hedged. This is not a replication claim and not a contradiction claim."
- **T1 — k=0 with CI upper below 14%:** "Our measured DG rate on this surface
  is 0% (0/N, Wilson [0%, hi]), below the nearest published floor for this
  model (≥14%, Qwen2.5-7B at `absent × prior_completing`, RAG-4 — a
  *different condition by definition*: the paper's completing evidence
  matches a parametric prior, ours is fabricated; a stated lower bound; a
  schema we did not run). Direction: lower. This is not a replication claim
  and not a contradiction claim."
- **T2 — CI excludes 0 and upper < 14%:** "DG occurs on this surface (k/N,
  Wilson [lo, hi], lower bound > 0) at a rate below the nearest published
  floor for this model (≥14% — different condition by definition, stated
  lower bound, schema we did not run). Direction: occurs, low. This is not a
  replication claim and not a contradiction claim."
- **T3 — CI contains 14%:** "DG occurs on this surface (k/N, Wilson [lo, hi])
  at a rate whose interval reaches the magnitude of the nearest published
  floor (≥14% — different condition by definition, stated lower bound, schema
  we did not run). Direction: comparable magnitude, hedged. This is not a
  replication claim and not a contradiction claim."
- **T4 — CI lower bound > 14%:** "DG occurs on this surface (k/N, Wilson
  [lo, hi]) at a rate above the nearest published floor (≥14% — different
  condition by definition, a stated lower bound whose true value may itself
  sit higher, schema we did not run). Direction: higher, hedged. This is not
  a replication claim and not a contradiction claim."

The five bands partition every reachable outcome: k=0 with the interval
reaching 14% → T0; k=0 with upper < 14% → T1; k≥1 with upper < 14% → T2;
k≥1 with the interval containing 14% → T3; lower bound > 14% → T4. All numbers
in a rendered template are filled from the row it fires on. Asserted in
`test_m1c_sizing.py`, which evaluates the five conditions independently of the
band function and requires exactly one to hold.

Which rows can produce T0 is a fact about the data, not part of any template's
text (PR #11 review F15): at the planned Ns only the original N=20 rows can,
since `wilson(0, 24)` upper is already 13.8% — but the D3 budget-truncation
path can produce a row at N ≤ 23, and `wilson(0, 23)` upper is 14.3%, so such a
row fires T0 too. The template therefore states only what its own numbers show.

Forbidden everywhere, restating D21: p-values against any paper cell;
"consistent with" / "contradicts" / "replicates" verbs; any point comparison.
The Newcombe delta (secondary) keeps its own M1 gate language (effect iff CI
excludes zero) — that is a *within-our-study* contrast and is exempt from
none of the honesty contract, just from the paper-comparison prohibition.

## D5 — Corpus extension p21–p80, seed-preserving, append-only

- Temperature is 0.0 by pre-commitment (D2 of M0: deterministic-as-available
  subjects), so new trials require new pairs. There is no re-sampling
  alternative that isn't a design change to the frozen subject contract.
- **Mechanics (the 12→20 pattern, verbatim):** append 60 entries to `THEMES`
  and 60 to `NAME_PREFIXES` — nothing else. `NAME_SUFFIXES` / `VERBS` /
  `NOUNS` / `FLAG_*` / `STEM_LETTERS` stay frozen (touching any re-rolls
  p01–p12 silently; the committed M0 guards are `data/corpus_m0.json` /
  `docs_m0.json` / `gen_log_m0.json` and must remain bit-identical).
  `build_corpus` consumes the RNG in pair order, so appending leaves p01–p20
  untouched.
- **No M1 fixture exists yet — the combined-N pooling depends on p01–p20
  staying byte-identical, so pinning them is the build's first step, before
  any pool is touched:** commit `data/corpus.json` → `data/corpus_m1.json`
  and `data/docs.json` → `data/docs_m1.json` as fixtures; extend
  `test_corpus.py` to pin `pairs[:20]` against them (today it pins only
  `pairs[:12]`); and mirror M1-BRIEF D4's gen-docs contract in `m1c.py
  gen-docs` — assert p01–p20 corpus entries and doc texts byte-unchanged
  before writing anything.
- Incremental `gen-docs` for p21–p80 only (3 docs/pair: x, y_completing,
  y_null), generator `gpt-4o-mini`, existing generator+verifier contract,
  30% retry margin priced in (last extension: 0% rejections).
- **Filler-population note, stated in advance:** `filler_pair_ids` samples
  from the full pair list, so extension trials draw fillers from the 80-pair
  population while the original M1b trials drew from 20. The original trials
  are never re-assembled — the M1b record stands on its logs — and per-trial
  mechanical verification of the manipulation applies to every new trial as
  ever. Listed as a stage-heterogeneity limitation in D1's robustness rows.

## D6 — Budget (measured-rate model, from the M1 ledgers)

Measured rates: qwen stark $0.0000388/trial, qwen camouflaged
$0.0001206/trial (`data/m1{a,b}_wave.jsonl`), $0.000133/doc → $0.0004/pair
(`data/gen_log_m1.json`).

| item | calc | est. |
|---|---|---|
| corpus gen-docs p21–p80 | 60 pairs × $0.0004 × 1.3 retry margin | $0.031 |
| smoke, both arms | ~5 × ($0.0000388 + $0.0001206) × 2 | $0.002 |
| wave, stark (2 cells × 60) | 120 × $0.0000388 | $0.005 |
| wave, camouflaged (2 cells × 60) | 120 × $0.0001206 | $0.014 |
| **total** | | **≈$0.052** |

- **`CAP_M1C_TOTAL = $0.10`** — hard ceiling on *measured* spend, ledger
  `data/m1c_spend.json`, each stage under min(own cap, remainder) — the
  `Decisions.md` D8 pattern. The ~2× headroom absorbs price drift and
  top-ups.
- Price re-pin at `m1c.py ping` before any spend (the `Decisions.md` D7
  pattern — M1's pre-spend price re-pin); drift is resolved consciously,
  never silently. (Cross-references to numbered points name their document —
  this brief's own sections are also numbered D1–D7.)
- Project total after M1C: ≈$0.08 spent of the <$5 KICKOFF target.

## D7 — Gates as code, dry-run before paid

- New flat script `m1c.py` (`ping|gen-docs|smoke|wave|verdict` per the
  M0-BRIEF D9 conventions), sharing `corpus.py` / `assemble.py` / `detectors.py` /
  `prompts.py` / `client.py` / `stats.py`. `m0.py`/`m1.py` are untouched
  frozen records.
- `verdict` re-derives from wave logs (M1's zero-rescore-mismatch property),
  ingests the M1 logs read-only for the original and combined rows, renders
  the D4 template selection mechanically, and emits
  `data/m1c_verdict.json`.
- Detectors, fidelity gate, and per-trial manipulation verification:
  unchanged from M1 (`classify` scores each trial as it runs — the D3
  blinding is procedural, not mechanical). The UNDERPOWERED threshold is
  **not** inherited: `m1c.py verdict` pins `N_CLEAN_REQUIRED_M1C = 80`
  (combined clean per gated cell per surface) and auto-reports UNDERPOWERED
  below it with the achieved N stated — M1's fixed 20 would pass a truncated
  wave silently (D3).
- Full dry-run on synthetic responses before any paid call; smoke N≈5 per arm
  before each paid wave.

## The argument, ruled (Kyle, 2026-08-04)

Three design points were open when this brief was drafted; Kyle ruled on all
three at the argue stage, each per the drafted recommendation:

1. **Primary analysis: combined N=80.** Combined maximizes precision; the
   one-look + no-further-extension guards bound the selection concern; the
   extension-only rows are always shown as the unconditioned check, and a
   template disagreement between them is reported side-by-side (D1), so
   nothing hides. (The alternative — extension-only primary, statistically
   purer at the cost of 25% of the data — was presented and declined.)
2. **Null-control extension at full E.** Keeps the paired Newcombe structure
   and the contamination guard at matching precision for ~$0.020 of the
   $0.052 — trial calls $0.010 plus the 60 `y_null` docs' generation $0.010,
   which a frozen null would also have skipped. (The ruling was presented
   with the ~$0.010 trial-side figure only; corrected here per PR #11 review
   F9 — the decision is unaffected, everything stays far under the cap. Freezing
   null at 20 would have left the secondary contrast base-limited: 0/20's
   16.1% upper would dominate the delta interval.)
3. **Combined N = 80 (+60 pairs).** $0.017 over the N=60 fallback buys the
   wider decisive bands in D2's table and headroom against the
   floor-is-a-floor caveat.

With those ruled, D1–D7 are the pre-registration. Build follows in D7's
order — dry-run, smoke, wave, verdict — and the brief is frozen from the
moment the first paid call runs. Nothing is built or spent until Kyle
green-lights the build on this committed brief.

---

## M1C outcome (2026-08-04) — the wave ran; the brief above is frozen

Rendered mechanically by `m1c.py verdict`, run **once**, per D3. The addendum
is appended; nothing above this line was edited after the first paid call.

### What ran

240 new trials (60 extension pairs × 2 gated cells × 2 surfaces) on
`qwen/qwen-2.5-7b-instruct`, pooled with M1's 20 per gated cell per surface.
**240/240 calls ok on the first pass** — no top-up needed, zero errored, zero
vague, zero confabulation. Fidelity gate **1068/1068 PASS** over the 80-pair
corpus. Doc generation: 180 attempts, **0 rejections**. Both surfaces hold
**80/80 clean per gated cell**, so `N_CLEAN_REQUIRED_M1C = 80` is met exactly
and neither surface reports UNDERPOWERED. Measured spend **$0.0446 / $0.10**
(estimate was $0.052; the 30% retry margin went unused).

The original rows re-derive M1's published verdicts exactly — stark
{refusal 13, discriminated 7}, DG 0/20; camouflaged {refusal 13,
discriminated 5, DG 2}, DG 2/20, blindness 2/2 and 2/2 — which is the
ingestion check the combined estimand depends on.

### The result, in the pre-committed rows

| surface | scope | DG-Y at `absent × completing` | Wilson 95% | template |
|---|---|---|---|---|
| stark | original (N=20) | 0/20 | [0.0%, 16.1%] | T0 |
| stark | extension-only (N=60) | 3/60 | [1.7%, 13.7%] | **T2** |
| **stark** | **combined (N=80)** | **3/80** | **[1.3%, 10.5%]** | **T2** |
| camouflaged | original (N=20) | 2/20 | [2.8%, 30.1%] | T3 |
| camouflaged | extension-only (N=60) | 5/60 | [3.6%, 18.1%] | **T3** |
| **camouflaged** | **combined (N=80)** | **7/80** | **[4.3%, 17.0%]** | **T3** |

Extension-only and combined selected the **same** template on each surface, so
D1's side-by-side clause did not fire and the combined statement is carried
alone. All three rows are recorded either way; the extension-only row is the
unconditioned check and is never hidden.

**The pre-committed statements, verbatim as rendered:**

- **Stark (T2):** "DG occurs on this surface (3/80, Wilson [1.3%, 10.5%],
  lower bound > 0) at a rate below the nearest published floor for this model
  (≥14% — different condition by definition, stated lower bound, schema we did
  not run). Direction: occurs, low. This is not a replication claim and not a
  contradiction claim."
- **Camouflaged (T3):** "DG occurs on this surface (7/80, Wilson [4.3%,
  17.0%]) at a rate whose interval reaches the magnitude of the nearest
  published floor (≥14% — different condition by definition, stated lower
  bound, schema we did not run). Direction: comparable magnitude, hedged. This
  is not a replication claim and not a contradiction claim."

### The secondary gate, and why it disagrees with the primary on the stark arm

| surface | Newcombe delta (completing − null_control), combined N | gate |
|---|---|---|
| stark | +0.037 [−0.015, +0.105] — straddles 0 | **NULL** |
| camouflaged | +0.087 [+0.024, +0.170] — excludes 0 | **DG-EFFECT** |

On the stark arm the primary estimand's interval excludes 0 (3/80 → lower
bound 1.3%) while the secondary paired interval does not. These are two
different questions and the rendering does not conflate them — the dry-run
carried a scenario for exactly this case before any spend. The structural
reason is the one M1 already stated against itself: at `absent ×
null_control` the Y-null doc contains **zero** token-shaped strings, so DG-Y
is impossible there by construction. The Newcombe interval nevertheless
carries the control cell's own Wilson width (0/80 → upper 4.6%) into the
difference, which is wider than the arm cell's distance from zero at k=3. The
paired test is therefore strictly more conservative than the one-sample
interval here, and its NULL is not evidence against occurrence.

### The flagship artifact, at ten answers instead of two

**Ten** DG answers across the two surfaces (3 stark, 7 camouflaged). On every
single one the mechanical **faithfulness proxy PASSES and the citation proxy
PASSES**: 3/3 and 3/3 on stark, 7/7 and 7/7 on camouflaged. Y's evidence
attributed to X, Y never named, a genuinely retrieved doc cited, every
standard check blind. M1 rendered this contrast on 2 answers and could only
call it an existence proof; at N=80 per surface it is rendered on ten, at both
surfaces, with a rate interval attached.

**DG-any is 0/160** — across all 160 camouflaged trials not one third-party
filler token entered an answer. The contamination guard reads clean.

### What M1C changes about M1

M1's headline was a NULL at both surfaces at N=20. The stark surface — where
M1 measured **0/20** — reads **3/80** at the pre-registered N, with a lower
bound above zero. D18 recorded that M1's N came from clean-trial yield rather
than a power calculation and could not resolve the floor; M1C is that
prediction bearing out on the project's own data. The M1 result is not
withdrawn — 0/20 was correctly measured and correctly reported, and its row
stands unchanged above — but the inference "DG ≈ 0 on this surface" was a
power artifact.

### Limitations, stated

- **Stage heterogeneity, and it is large.** Engagement (non-refusal) at the
  adversarial cell differs materially between the two stages: stark 35% on
  p01–p20 vs 65% on p21–p80; camouflaged 35% vs 55%. The two stages are not
  behaviourally exchangeable, and the combined row pools them. Both scopes
  fired the same template on each surface, and the extension-only rows are
  reported beside the combined ones precisely so this is visible rather than
  averaged away — but the DG rates themselves rest on pairs that elicit more
  engagement than M1's did. No mechanism for the difference is established
  here; the pairs differ in their hand-authored themes and generated prose —
  and, per D27 below, repeat draws of the same prompt are not stable either, so
  "only" would be wrong.
- **The filler population changed**, as D5 stated in advance: extension trials
  draw fillers from 80 pairs, the original M1b trials drew from 20. The
  original trials were never re-assembled.
- **The camouflage levers stay bundled** (JSON rendering, constant titles,
  k=4 fillers), so the stark-vs-camouflaged difference — 3/80 [1.3%, 10.5%] vs
  7/80 [4.3%, 17.0%], overlapping intervals — is not attributable to any one
  of them. M1C pre-registered no cross-surface test and none is performed.
- **One model.** Nothing here transfers to `llama-3.1-8b-instruct` or
  `gemma-3-12b-it`, which have no published anchor of any kind (D1).
- **14% remains a reference magnitude for sizing and wording only** (D21),
  never a null hypothesis about our cell. No p-value is attached to any
  comparison with the paper, and the templates above are the only permitted
  verbs.
- **D7's "`m0.py`/`m1.py` are untouched frozen records" is false as written,
  and is superseded by D26.** This milestone had to modify both. Growing the
  shared corpus re-scoped the `corpus.N_PAIRS` those scripts read, so leaving
  their bytes alone is what changed their behaviour: `m1.py dryrun` began
  reporting FAILED, `m1.py wave` would have run 480 trials instead of M1's 120
  under M1's caps, and `m0.py`/`m1.py verdict` would have rewritten their
  published verdict files with fidelity counts from a corpus those milestones
  never ran on. Both are now pinned to their own `N_PAIRS_M0` / `N_PAIRS_M1` —
  restoring the behaviour each had when it ran — and every verdict writer, plus
  `m0.py gen-docs`, refuses to run once the shared pool has moved. The D7
  section stands as written because it is frozen; this is where it is
  corrected. Frozen means the recorded behaviour is preserved, not that the
  bytes are inviolable while the behaviour drifts.
- **Repeat draws are not stable at `temperature = 0.0` (D27), and D5's premise
  above is wrong because of it.** Smoke and wave both ran `absent × completing`
  on p21–p25, so this milestone committed 10 duplicate trials of byte-identical
  prompts. **3 differ in answer text, 2 change label** (`m1ca` p25 and `m1cb`
  p22, both `correct-refusal` → `discriminated`), and **2 report different
  `prompt_tokens` for the same prompt** — which prompt construction cannot
  produce, so those calls reached different backends. `client.py` sends no
  `provider` preference and no seed. Three consequences, stated rather than
  smoothed over:
  1. **D5's frozen rationale is false as written.** It says *"Temperature is 0.0
     by pre-commitment … so new trials require new pairs. There is no
     re-sampling alternative that isn't a design change to the frozen subject
     contract."* Re-sampling the same 20 pairs would in fact have produced new
     information — and would have avoided the stage heterogeneity that is now
     this study's principal limitation. The frozen section stands as written
     because it is frozen; this addendum is where it is corrected.
  2. **The "only" in the heterogeneity note above is corrected.** Repeat-draw
     instability is a second live source of variation between stages, alongside
     theme and prose composition.
  3. **No committed rate in this repo is exactly reproducible by re-running its
     wave.** That is a fair property for a study to have; it is not a fair
     property to leave unstated in a repo whose contract is per-trial
     mechanical verification.

  The condition is **pre-existing, not introduced here** — M1's own logs show it
  (30 duplicates: 8 text differences, 2 label flips). Pinning provider routing
  is the durable fix, is a design change, and belongs in a future brief rather
  than a retrofit into this one.

### The stopping rule holds

D3's "no further extension, regardless of outcome" is binding. Whatever these
numbers invite, any subsequent wave is a new pre-registered study with its own
brief — never an M1C top-up.
