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

Computed with the repo's own `stats.wilson` (script: this brief's numbers
re-derive with `python3 - <<'EOF' ... stats.wilson ... EOF` against HEAD).

**Sizing question:** what combined N makes the *directional* statement
decisive — meaning every reachable outcome k maps to exactly one
pre-committed template, with no outcome left saying "cannot tell"?

| combined N | 0/N Wilson upper | T2 band (occurs, below floor) | T3 starts at |
|---|---|---|---|
| 20 (status quo) | 16.1% — **above the floor; the D18 gap** | — | — |
| 24 | 13.8% — bare exclusion only | k=… degenerate | — |
| 60 (+40 pairs) | 6.0% | k=1–3 | k=4 (6.7%) |
| **80 (+60 pairs)** | **4.6%** | **k=1–5** | **k=6 (7.5%)** |
| 120 (+100 pairs) | 3.1% | k=1–8 | k=9 (11.2%) |

- At **N=80**: k=0 → [0, 4.6%]; k=2 (the carried camouflaged events alone) →
  [0.7%, 8.7%]; k=5 → [2.7%, 13.8%]; k=6 → [3.5%, 15.4%]; k=8 (the 10% point
  estimate holding) → [5.2%, 18.5%]. Every k lands in exactly one template.
- **Sensitivity to the floor being a floor:** the paper's own calibration
  model reads 34% (Fig. 6, RAG-4) vs 67.0% (Table 1, 10-tool) at the same
  cell — a ~2× schema discrepancy. Sized against a doubled reference (~28%):
  if the true rate is at that magnitude, expected k ≈ 22/80 → CI ≈ [19%, 38%],
  decisively T3. The sizing does not depend on 14% being exact.
- **Why not 24** (the bare-exclusion minimum): 0/24 clears the floor only if
  the extension observes zero events; the camouflaged cell already carries 2.
  The interesting deliverable is a **tight estimate**, not a bare exclusion.
- **Why not 120:** $0.034 more for template-band shifts that change no verb;
  and 100 new hand-authored themes materially raises corpus-quality risk.

**Pre-committed choice: combined N = 80 per cell per surface (E = +60 pairs).**

Power against the "does DG occur at all" direction (Wilson lower bound > 0),
by simulation with the repo's own interval (20k reps): if the true camouflaged
rate is 10%, P(lo > 0) ≈ 1.00 at N=80; if 5%, ≈ 0.98. The carried k=2 makes
the combined lower bound > 0 certain for the camouflaged cell; the question
N=80 answers is *where the upper bound lands*.

## D3 — One-look guard (the optional-stopping pre-commitment)

- **N is fixed here.** E = 60 new pairs; target 80 clean trials per gated
  cell per surface, combined.
- **One look.** `m1c.py verdict` runs once, after the full wave. No interim
  DG counts — the wave script logs trials and costs but computes no DG rate
  before the verdict. (Smoke checks pipeline mechanics — call success, doc
  fidelity, detector run — and its N≈5 DG output is quarantined: smoke trials
  never enter any N, and no wave/N decision keys off a smoke DG count.)
- **Clean-trial top-up, bounded and blind:** if clean yield < 100% (M1 ran
  240/240), top-up waves run only to reach the fixed N-clean target, still
  without computing DG. Top-up is capped by budget (D6); if the cap binds
  first, the verdict runs at the achieved N and the gate auto-reports
  UNDERPOWERED per the KICKOFF contract.
- **No further extension, regardless of outcome.** Whatever M1C shows, any
  subsequent wave is a new pre-registered study with its own brief — never an
  M1C top-up. This clause is the stopping rule.

## D4 — Reporting: templates fixed verbatim, direction only

Every rendering of the M1C result shows **three rows** per surface per cell:
original (N=20), extension-only (N=60), combined (N=80) — the original is
never replaced, the extension-only is never hidden.

The directional statement is selected by where the combined Wilson CI on the
primary estimand lands. Exactly one template fires per surface; the templates
are the only permitted verbs, and each carries its caveats inline so no
downstream rendering can drop them (the F9 failure mode):

- **T1 — k=0:** "At N=80 our measured DG rate is 0% [0%, 4.6%], below the
  nearest published floor for this model (≥14%, Qwen2.5-7B at
  `absent × prior_completing`, RAG-4 — a *different condition by definition*:
  the paper's completing evidence matches a parametric prior, ours is
  fabricated; a stated lower bound; a schema we did not run). Direction:
  lower. This is not a replication claim and not a contradiction claim."
- **T2 — CI excludes 0 and upper < 14%:** "DG occurs on this surface (k/N,
  Wilson [lo, hi], lower bound > 0) at a rate below the nearest published
  floor for this model (≥14% — different condition by definition, stated
  lower bound, schema we did not run). Direction: occurs, low. This is not a
  replication claim and not a contradiction claim."
- **T3 — CI reaches 14%:** "DG occurs on this surface (k/N, Wilson [lo, hi])
  at a rate whose interval reaches the magnitude of the nearest published
  floor (≥14% — different condition by definition, stated lower bound, schema
  we did not run). Direction: comparable magnitude, hedged. This is not a
  replication claim and not a contradiction claim."

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
  p01–p12 silently; `data/corpus_m0.json` / `docs_m0.json` are the committed
  guards and must remain bit-identical). `build_corpus` consumes the RNG in
  pair order, so appending leaves p01–p20 untouched; the M1 fixtures guard
  p13–p20 the same way.
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
  `data/m1c_spend.json`, each stage under min(own cap, remainder) — the D8
  pattern. The ~2× headroom absorbs price drift and top-ups.
- Price re-pin at `m1c.py ping` before any spend (the D7 pattern); drift is
  resolved consciously, never silently.
- Project total after M1C: ≈$0.08 spent of the <$5 KICKOFF target.

## D7 — Gates as code, dry-run before paid

- New flat script `m1c.py` (`ping|gen-docs|smoke|wave|verdict` per the D9
  conventions), sharing `corpus.py` / `assemble.py` / `detectors.py` /
  `prompts.py` / `client.py` / `stats.py`. `m0.py`/`m1.py` are untouched
  frozen records.
- `verdict` re-derives from wave logs (M1's zero-rescore-mismatch property),
  ingests the M1 logs read-only for the original and combined rows, renders
  the D4 template selection mechanically, and emits
  `data/m1c_verdict.json`.
- Detectors, fidelity gate, and per-trial manipulation verification:
  unchanged from M1. N≥20-clean-per-gated-cell auto-UNDERPOWERED rule:
  unchanged (trivially exceeded at target N; binding only if the budget cap
  truncates a top-up, per D3).
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
   and the contamination guard at matching precision for ~$0.010 of the
   $0.052. (Freezing null at 20 would have left the secondary contrast
   base-limited: 0/20's 16.1% upper would dominate the delta interval.)
3. **Combined N = 80 (+60 pairs).** $0.017 over the N=60 fallback buys the
   wider decisive bands in D2's table and headroom against the
   floor-is-a-floor caveat.

With those ruled, D1–D7 are the pre-registration. Build follows in D7's
order — dry-run, smoke, wave, verdict — and the brief is frozen from the
moment the first paid call runs. Nothing is built or spent until Kyle
green-lights the build on this committed brief.
