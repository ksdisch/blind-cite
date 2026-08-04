# HANDOFF.md

_Last updated: 2026-08-04_

## What was just done
- **PR #10 (the correction campaign) is merged** — squash `2de0f1b`. The adversarial review ran five rounds across two runs: run 1 hit the 3-dispatch cap NOT CLEAR with six fixes unverified; Kyle ruled for a fresh verification round over a waiver; rounds 4–5 verified everything. **All 23 findings fixed and verified, zero waivers** — including the nice-to-haves, which Kyle flipped to fix-now at the round-4 triage gate. Adjudicated comment on the PR.
- **The M1C pre-registration is written and committed** (`docs/M1C-BRIEF.md`, D23). It was argued before landing: Kyle ruled the three open design points in-session — combined-N primary analysis, full null_control extension, combined **N=80** per gated cell per surface (+60 pairs). Sizing is a real power calculation this time (the repo's own `stats.wilson`; every reachable outcome maps to exactly one of three pre-committed direction-only templates).
- The three-headline history (D12→D16, D13→D17, D17→D21) stands recorded in `Wiki/Paper-Mapping.md`; the brief's templates carry the D21 caveats inline so no rendering can drop them.

## Where things stand
M0 FIT; M1 gate NULL at both surfaces at N=20 (direction only — no paper cell matches our condition, D21). `main` carries M1 (PR #9, `e057c6d`) and the full correction campaign (PR #10, `2de0f1b`). The M1C pre-registration is the current branch's payload. **Nothing of M1C is built and nothing is spent** — that is gated on Kyle's explicit go on the committed brief. Total project spend ≈$0.027 of the <$5 budget; M1C is estimated ≈$0.052 under its own $0.10 cap.

## Immediate next move
**Kyle's go/no-go on the M1C build.** On go, build in `docs/M1C-BRIEF.md` D7's order: corpus extension p21–p80 (seed-preserving, append-only `THEMES`/`NAME_PREFIXES` only, fixtures pinned) → `m1c.py` (`ping|gen-docs|smoke|wave|verdict`) with gates as code → dry-run on synthetic answers → `ping` price re-pin → smoke N≈5 per arm → both waves → **one-look verdict**. The brief freezes at the first paid call.

Only after M1C: `/research-paper`, which must render the paper relationship exclusively through the brief's D4 templates (direction only, caveats inline, no p-value against any paper cell). Then `/seed-hunt` for repro #6.

## Open questions / blockers
- **The build green-light (the only blocker).** D23 commits the design; Kyle has not yet said "build it".
- **The live scientific question:** what our kin-model rate actually is. At N=20 the interval spans the nearest published floor either way; combined N=80 resolves it into exactly one pre-committed template.
- No published anchor of any kind for `llama-3.1-8b-instruct` or `gemma-3-12b-it` — the paper's Llama and Gemma entries are **different models**. M1C deliberately excludes them (D23).
- **Schema contradiction, flagged not resolved:** Figure 6 is RAG-4, Tables 1–2 are 10-tool; the paper claims <2pp yet its calibration model reads 34% vs 67.0% at the same cell. The brief sizes against a doubled reference (~28%) so the verdict does not depend on 14% being exact.
- Watch for an arXiv v2 (reference-only either way; re-read 2026-08-04 during review rounds 4–5, still v1, no code).
- Six nice-to-have follow-ups from PR #9's review; none blocks anything. (PR #10 has none — everything was fixed.)

## Files touched recently
- `docs/M1C-BRIEF.md` — **the pre-registration.** Scope/estimand, power calculation, one-look guard, report templates, corpus-extension mechanics, budget cap, gates-as-code plan, and the record of Kyle's three rulings.
- `Decisions.md` — D23 appended (M1C pre-registration committed; build gated on Kyle's go).
- `PROJECT.md` — status and next actions now point at the M1C build.
- `Wiki/History.md` — appended: PR #10 merged after the five-round review; M1C pre-registration committed.
- `Wiki/Paper-Mapping.md` — unchanged this branch; still **read this first** for why no paper cell matches our condition.
