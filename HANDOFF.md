# HANDOFF.md

_Last updated: 2026-08-03_

## What was just done
- **M1 built and run end to end, Option C, both arms.** `m1.py` pre-committed with every gate as code, dry-run on synthetic answers through the real scoring path, committed and pushed **before** the first paid call — then `ping` → `gen-docs` → M1a smoke/wave/verdict → M1b smoke/wave/verdict.
- **Verdict: NULL at both surfaces, well-powered** (Decisions.md D10). 240/240 trials ok on first pass; 20/20 clean per gated cell per model on both arms; zero vague, zero confabulation, zero errors; fidelity gate 288/288 at both verdicts.
- **The flagship blindness contrast rendered** — the artifact M1 exists to produce — on `qwen-2.5-7b`'s 2 DG answers at the camouflaged cell: faithfulness PASS 2/2, citation PASS 2/2.
- Supporting build: M0 fixtures pinned (`corpus_m0`/`docs_m0`/`gen_log_m0`), seed-preserving corpus extension 12→20 pairs (append-only pools), incremental `gen-docs` (24 new docs, 0% rejection), the misattributed-other/confabulation detector split, and the M1b camouflage surface (JSON tool-results, constant titles, k=4 off-theme fillers).

## Where things stand
M0 FIT and M1 NULL are both closed and recorded. The pre-committed design (M1a) rendered its own verdict untouched, and the camouflage surface (M1b) was tested beside it rather than instead of it — Option C did exactly what it was chosen to do. Every DG in the project (n=2) appeared only at the camouflage surface and only on the paper's own kin model; the cross-surface delta straddles 0, so that is texture, not a claim. Total project spend ≈$0.027 against the <$5 budget. Branch `feat/m1-option-c`, PR open.

## Immediate next move
**Kyle's call: close v1 at M1 (D11, Proposed).** M2 suppresses a rate that is already ~0 and M3 ablates a phenomenon that occurred twice — both degenerate on the measured data, exactly as the M1 brief's D1 anticipated. If the null should instead be pushed on, the two documented escalations are pre-named and each needs its own argued addendum before any spend: (1) a small frozen title pool assigned by post-shuffle doc *position*, (2) same-theme filler generation with a new verifier contract. On closing v1: `/research-paper`, then `/seed-hunt`.

## Open questions / blockers
- None blocking. **D11 is Proposed, not decided** — closing v1 is Kyle's call.
- Watch for an arXiv v2 of 2607.09349 (reference-only either way; last checked 2026-08-03, still v1, no code).
- Noted, not a blocker: `qwen-2.5-coder-7b` still gone from OpenRouter — matters only if the parked specialization arm unparks.
- Resolved this session: review follow-up F9 (PR #8 merge SHA backfilled in `Wiki/History.md`).

## Files touched recently
- `m1.py` + `test_m1.py` — the M1 gates and their dry-run; the pre-commitment in code.
- `corpus.py`, `assemble.py`, `detectors.py`, `prompts.py` — 20-pair extension, camouflage surface, detector split.
- `data/` — `corpus_m0`/`docs_m0`/`gen_log_m0` fixtures, `gen_log_m1.json`, `m1a`/`m1b` smoke+wave+verdict, `m1_surface_contrast.json`, `m1_spend.json`, `handlabeled_m1.json`.
- `docs/M1-BRIEF.md` — the "M1 outcome" addendum (the results of record).
- `Wiki/Results.md` (new), `Wiki/Why-The-Null.md`, `Wiki/Detector-Design.md`, `Wiki/History.md`, `Decisions.md` (D7–D11), `PROJECT.md`.
