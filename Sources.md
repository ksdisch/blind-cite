# Sources

| Source | Location | Type | Authoritative for |
|--------|----------|------|-------------------|
| Kickoff brief | `docs/KICKOFF.md` | brief (approved 2026-07-15) | Scope, milestones, honesty contract, riskiest assumptions, tech stack — the project's source of truth |
| M0 brief + addendum | `docs/M0-BRIEF.md` | pre-committed design + results addendum | M0 design decisions D1–D9 (roster, corpus, detectors, kill/swap triggers, budget) and the pilot outcome |
| M0 verdict | `data/m0_verdict.json` | machine-rendered verdict | The FIT verdict, survivor roster, and per-model gate results |
| M0 run data | `data/pilot.jsonl`, `data/smoke.jsonl`, `data/gen_log.json`, `data/handlabeled.json` | raw run artifacts | Per-trial evidence behind every M0 number |
| Frozen corpus | `data/corpus.json`, `data/docs.json` | frozen seeded data (SEED=20260715) | Entity pairs, owned-token maps, verified synthetic docs |
| Target paper | arXiv 2607.09349 (Caruzzo, Yoo, Kim), v1 2026-07-10 (re-checked 2026-08-03: still v1, no code) | external paper (no code shipped) | The deceptive-grounding claim being reproduced; directional anchors only, never point-estimate targets |
| Project context | `CLAUDE.md` | working context | Current-milestone status line, conventions, honesty contract summary |
