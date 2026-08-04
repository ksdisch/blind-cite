# HANDOFF.md

_Last updated: 2026-08-04_

## What was just done
- **M1C ran end to end and the one look is rendered** (D24). The pre-registration in `docs/M1C-BRIEF.md` was executed in its committed order — F15/F16 follow-ups → M1 fixtures pinned → corpus p21–p80 → `m1c.py` → dry-run → `ping` → smoke → both waves → `m1c.py verdict`, run once. Nothing above the outcome addendum in the brief was edited after the first paid call.
- **The result: DG occurs at both surfaces once N is adequate.** Combined N=80 per gated cell per surface on `qwen-2.5-7b`. Stark **3/80, Wilson [1.3%, 10.5%] → T2**; camouflaged **7/80, Wilson [4.3%, 17.0%] → T3**. Extension-only and combined fired the same template on each surface, so D1's side-by-side clause did not fire. **The flagship blindness contrast now rests on ten answers** (3 stark + 7 camouflaged), faithfulness PASS 10/10, citation PASS 10/10.
- **M1's stark null did not survive the pre-registered extension, much as D18 predicted about the project.** M1 measured 0/20 there; at the pre-registered N the lower bound is above zero. The measurement stands as recorded — the inference drawn from it does not (D24). **Not attributable to N alone:** the extension's pairs also elicited materially more engagement (D25), and this study separates the two effects nowhere. (Wording corrected 2026-08-04 — the earlier "was a power artifact" asserted the single cause D25 says is not established; see PR #16 review F1.)
- Run quality: 240/240 calls ok on the first pass, zero errored / vague / confabulated; 180 doc generations with 0 rejections; fidelity 1068/1068; DG-any 0/160. Spend **$0.0446 / $0.10**.

## Where things stand
`main` carries everything through M1C — PR #12 squash-merged as `f1230fc` on Kyle's call after a three-round adversarial review (12 findings, no disputes, every should-fix fixed and verified, six nice-to-have follow-ups open). Project total ≈$0.072 of the <$5 budget. **D3's stopping rule is now binding** — no further extension, whatever these numbers invite; any further measurement is a new pre-registered study with its own brief.

The secondary paired gate disagrees with the primary on the stark arm (Newcombe +0.037 [−0.015, +0.105] straddles 0 → gate NULL, while the primary Wilson interval excludes 0). This is not a defect and not a conflict: DG-Y is impossible by construction at `absent × null_control`, so the paired interval carries the control's own Wilson width and is strictly the more conservative of the two. Both are reported; neither is presented as the other. The dry-run carried a scenario for this exact case before any spend.

## Immediate next move
**`/research-paper`.** The write-up is now off a substantive result rather than a null. Non-negotiable constraints for it:
- State the paper relationship **exclusively** through the M1C-BRIEF D4 templates (T0–T4). Direction only, caveats inline, no p-value against any paper cell, no point comparison. Three headlines have already been withdrawn here for breaking exactly this rule.
- Report **all three rows per surface** (N=20 / N=60 / N=80). The original is never replaced; the extension-only is never hidden.
- Carry **D25 (stage heterogeneity)** as a stated limitation in the body, not a footnote — engagement at the adversarial cell runs 35% on M1's pairs vs 55–65% on the extension's, and the combined row pools them.
- Do not conflate the primary estimand with the secondary paired gate.

Then `/seed-hunt` for repro #6.

## Open questions / blockers
- **No blockers.** M1C is complete, merged, and the stopping rule closes the measurement phase.
- **Six open follow-ups from PR #12's review, none blocking.** Ranked: **F11** — `m1.py cmd_gen_docs` is the last unpinned doc generator and the new `m0.py` HALT text points operators at it; same hazard class as F2/F6, latent until a milestone grows the pool past 80, and it would overwrite `data/gen_log_m1.json` and bill M1's ledger. Then **F8** (`m1.py cmd_wave` filters before slicing, so a missing early doc set would backfill an M1C pair into M1's published wave), **F4** — ✅ **RESOLVED 2026-08-04** (the "power artifact" headline credited N for a change partly driven by the engagement shift — stark opportunities 7/20 → 39/60, Fisher p = 0.035; stating the 0/7 → 3/39 denominator beside it would be more exact. The headline is corrected throughout the live record — D24, this file, `Wiki/Results.md`, `Wiki/Why-The-Null.md`, `Wiki/_index.md` — and `docs/paper/` never carried it. The opportunity denominators and the Fisher p above are recorded in **no committed file**, so the paper states the recorded engagement *shares* instead and says so explicitly; that half is deliberately not adopted), and **F9/F10/F12** (test hygiene). Full detail: `~/.claude/reviews/blind-cite/2026-08-04-feat-m1c-extension.md`.
- **Unresolved — what drives the stage heterogeneity (D25).** The extension pairs elicit materially more engagement than M1's. Two sources are live — theme/prose composition **and** repeat-draw instability (D27) — and no mechanism is established; the pre-registration correctly forbids adjusting for it after the fact.
- **Unresolved — the camouflage levers stay bundled.** Stark 3/80 [1.3%, 10.5%] vs camouflaged 7/80 [4.3%, 17.0%] have overlapping intervals, and M1C pre-registered no cross-surface test, so none was performed. No attribution among JSON rendering / constant titles / k=4 fillers is possible from this data.
- **Unresolved — one model only.** Nothing transfers to `llama-3.1-8b-instruct` or `gemma-3-12b-it`; the paper's Llama and Gemma entries are different models and neither has an anchor of any kind.
- **Resolved during review, recorded because it changed a pre-commitment (D26):** growing the shared corpus re-scoped the `corpus.N_PAIRS` that `m0.py` and `m1.py` read, silently changing their behaviour — `m1.py dryrun` began reporting FAILED, `m1.py wave` would have run 480 trials instead of 120, and both `verdict` commands would have rewritten their published verdict files with fidelity counts from a corpus those milestones never ran on. Both are now pinned to their own `N_PAIRS_M0` / `N_PAIRS_M1` and refuse to re-render a verdict once the pool has moved; `m1c.py` carries the same guard forward. **This makes M1C-BRIEF D7's "m0.py/m1.py are untouched frozen records" false as written** — superseded on that point by D26, and flagged for Kyle rather than slipped in.
- **Unresolved — repeat draws are not stable at temperature 0 (D27).** Of the 10 duplicate smoke-vs-wave trials this milestone committed, 3 differ in answer text, 2 change label, and 2 report different `prompt_tokens` for a byte-identical prompt — i.e. provider routing is unpinned (`client.py` sends no `provider` preference and no seed). Pinning it is a design change and belongs in a future brief, not a retrofit here.
- **Schema contradiction, flagged not resolved:** Figure 6 is RAG-4, Tables 1–2 are 10-tool; the paper claims <2pp yet its calibration model reads 34% vs 67.0% at the same cell. M1C sized against a doubled reference (~28%) so the verdict never depended on 14% being exact.
- Watch for an arXiv v2 (reference-only either way; still v1 as of 2026-08-04, no code).

## Files touched recently
- `docs/M1C-BRIEF.md` — the frozen pre-registration **plus** the "M1C outcome" addendum: what ran, the three rows per surface, the verbatim rendered statements, why the secondary gate disagrees on the stark arm, the ten-answer blindness artifact, and the limitations.
- `m1c.py` — the milestone script: gate, D4 template rendering, one-look verdict, pooling preconditions, spend ledger.
- `test_m1c.py`, `test_m1c_sizing.py` — the dry-run scenarios and the sizing/band pins; `band()` is now imported from `m1c.py` so the pin binds the rendering path rather than a copy of it.
- `corpus.py`, `data/corpus.json` — 80 pairs, append-only; `data/corpus_m1.json` / `data/docs_m1.json` are the new p01–p20 fixtures the pooling depends on.
- `data/m1c_verdict.json` — the machine-rendered one look, the primary record.
- `Decisions.md` — D24 (verdict) and D25 (stage heterogeneity) appended.
- `Wiki/Results.md`, `Wiki/Why-The-Null.md`, `Wiki/Paper-Mapping.md`, `Wiki/History.md` — updated for the result. **Read `Wiki/Paper-Mapping.md` first** for why no paper cell matches our condition.
