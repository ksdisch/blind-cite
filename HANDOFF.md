# HANDOFF.md

_Last updated: 2026-08-03_

## What was just done
- **Resumed from park.** `docs/M1-BRIEF.md` written: argues the unresolved M1 design decision (D5/D-M1) — Option A (run exactly as pre-committed; likely well-powered NULL), Option B (documented camouflage variant: JSON tool-result rendering + seeded filler docs), Option C (both, sequenced — recommended). No code, no paid calls.
- README reconciled with recorded reality (it previously claimed "Milestone 0 not yet started"): M0-complete status + headline + D-M1 pointer.
- Paper re-checked (2026-08-03): arXiv 2607.09349 still **v1 only, no code, no withdrawal**. New reading recorded in the brief (E3): the paper's docs are JSON tool-call results with entity identity only in content text, and §5.3 claims mismatch-detection doesn't prevent DG — evidence our null may live in the presentation layer.

## Where things stand
M0 closed FIT (fidelity 16/16, generator rejection 0/36, 144/144 calls ok, grounding at ceiling, DG 0/36 all-K4). M1 is sized at 20 pairs from the measured funnel. The M1 brief is written and the project is **blocked on exactly one thing: Kyle's D5 pick**. Working tree on `docs/m1-brief` (PR pending merge at handoff time); no other branches open.

## Immediate next move
Kyle resolves D5/D-M1 at `docs/M1-BRIEF.md`. On the pick: record it in Decisions.md (append-resolve D5), add a brief addendum with the choice + any trims (filler count k, JSON lever), then pre-commit `m1.py` + gates, dry-run, smoke, run. No paid call before the pick.

## Open questions / blockers
- **D5/D-M1 (Unresolved — the blocker):** A pre-committed / B camouflage / C both sequenced. Brief recommends C.
- Repo visibility: flip back to public now that the README contradiction is fixed — Kyle's call, was waiting on README + D-M1.
- Watch for an arXiv v2 with code/appendix (reference-only either way). Last checked 2026-08-03: v1 only.
- Noted, not a blocker: `qwen-2.5-coder-7b` gone from OpenRouter — matters only if the parked specialization arm unparks.

## Files touched recently
- `docs/M1-BRIEF.md` — the decision brief (new; the thing Kyle reads to pick).
- `README.md` — status section rewritten to match recorded reality; verdict-script phrasing fixed.
- `PROJECT.md`, `Decisions.md`, `Sources.md`, `Wiki/History.md` — resume-state wiki updates.
- `docs/M0-BRIEF.md` + `data/m0_verdict.json` — unchanged; still the source of truth for M0 results.
