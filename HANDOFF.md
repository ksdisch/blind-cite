# HANDOFF.md

_Last updated: 2026-07-26_

## What was just done
- Project wiki initialized (PROJECT.md, HANDOFF.md, Sources.md, Decisions.md) — no code or data changes.
- Prior work (2026-07-15/17): M0 fit-pilot completed with verdict **FIT** (PR #1, commit 049c5e4); global Claude tooling vendored via /claudify-repo (PR #2, commit 56b74ed).

## Where things stand
The project is **parked** (2026-07-15, displaced at seed-hunt by dim-stage; re-queued as default repro #6). M0 closed clean: fidelity gate 16/16, generator rejection 0/36, 144/144 pilot calls ok, grounding at ceiling for all three subjects, and DG = 0/36 at the adversarial cell — every model tripped the K4 flag (robust-low-DG for the right reason). M1 sizing is already computed from the measured funnel: 20 pairs. Working tree is clean on `main`; branches `feat/m0-fit-pilot` and `feat/claudify-repo` are merged.

## Immediate next move
On resume: write `docs/M1-BRIEF.md` and put the M1 design decision to Kyle — run M1 as pre-committed (likely a well-powered NULL headline, legitimate per the honesty contract) vs. a documented camouflage-level variant (e.g. multi-doc retrieval with filler docs so the Y-doc's name-mismatch is less glaring). This is a real design change that must be argued in the brief, not slipped in.

## Open questions / blockers
- **D-M1 (Unresolved):** pre-committed M1 vs. documented camouflage variant — Kyle's call at the M1 brief.
- Does an arXiv v2 with code/appendix appear? Reference-only either way (honesty contract).
- Not a blocker, but noted: the gated specialization arm needs a fresh model pairing if it ever unparks (`qwen-2.5-coder-7b` gone from OpenRouter).

## Files touched recently
- `PROJECT.md`, `HANDOFF.md`, `Sources.md`, `Decisions.md` — wiki init (this change).
- `CLAUDE.md` — Project Wiki section appended (this change); status line already reflects M0 COMPLETE.
- `docs/M0-BRIEF.md` — pre-committed M0 design D1–D9 + pilot-outcome addendum (source of truth for M0 results alongside `data/m0_verdict.json`).
