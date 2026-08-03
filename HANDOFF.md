# HANDOFF.md

_Last updated: 2026-08-03_

## What was just done
- **Resumed from park and D5 resolved.** `docs/M1-BRIEF.md` written (A pre-committed / B camouflage / C both sequenced), adversarially reviewed on PR #8 — 3 rounds, 17 findings, all accepted, 15 fixed+verified or swept, F16/F17 fixed under Kyle's explicit re-verify waiver — and **Kyle picked Option C** in-session (Decisions.md D6, brief addendum "The pick").
- README reconciled with recorded reality; CLAUDE.md/PROJECT.md/wiki brought in step; paper re-checked 2026-08-03 (arXiv 2607.09349 still v1, no code).
- Repo flipped back to **public** (README contradiction fixed + D-M1 decided — both stated preconditions met).

## Where things stand
M0 closed FIT (fidelity 16/16, generator rejection 0/36, 144/144 calls ok, grounding at ceiling, DG 0/36 all-K4). **D6: M1 runs as Option C** — M1a exactly as pre-committed, then labeled camouflage arm M1b (JSON tool-result rendering, constant titles, k=4 off-theme fillers, misattributed/confab detector split). Sized at 20 pairs; est. ~$0.04 against the $5 budget. `main` carries the merged brief; no branches open.

## Immediate next move
Build `m1.py` per the brief's "The pick" addendum, in order: pre-commit gates → dry-run on synthetic answers → `ping` + measured-rate check → smoke N≈5 → M1a wave → verdict → M1b build (M0 fixtures `corpus_m0/docs_m0/gen_log_m0`, seed-preserving corpus extension +8 themes/prefixes append-only, incremental gen-docs writing `gen_log_m1.json`, extended fidelity gate 100%) → M1b smoke → wave → verdict. The top-up policy (re-run errored trials only, until ≥20 clean per cell or the cap binds) is pre-committed in the brief's D4.

## Open questions / blockers
- None blocking. Watch for an arXiv v2 (reference-only either way; last checked 2026-08-03).
- Review follow-up F9: backfill PR #8's merge SHA in `Wiki/History.md` at the next wiki touch.
- Noted, not a blocker: `qwen-2.5-coder-7b` gone from OpenRouter — matters only if the parked specialization arm unparks.

## Files touched recently
- `docs/M1-BRIEF.md` — the decision brief + "The pick" addendum (D5→C); the M1 build spec.
- `Decisions.md` — D5 Resolved (by D6); D6 Approved (Option C).
- `README.md`, `CLAUDE.md`, `PROJECT.md`, `Sources.md`, `Wiki/History.md`, `Wiki/_index.md` — resume-state + post-decision consistency.
- `docs/M0-BRIEF.md` + `data/m0_verdict.json` — unchanged; still the source of truth for M0 results.
