# HANDOFF.md

_Last updated: 2026-08-03_

## What was just done
- **M1 built and run end to end (Option C, both arms), reviewed, and merged** — PR #9, squash `e057c6d`. Verdict **NULL at both surfaces, well-powered**; the flagship blindness contrast rendered on 2 answers (faithfulness PASS 2/2, citation PASS 2/2).
- **The paper was re-read in full**, which produced a correction and a reframing. The 66.3% Qwen2.5-7B anchor carried since KICKOFF is that model's **peak cell** (`absent × synthetic_Y`, Table 2), not our gated cell, and the paper publishes no per-cell breakdown for any non-calibration model — so "paper-contradicting for cheap models" was never cell-matched and is **withdrawn** (D12).
- **Headline reframed to prior-dependence (D13).** The paper's mechanism opens when "disease-context overlap activates a parametric attribution prior"; this corpus fabricates both entities *and* all evidence — the property that makes the detector judge-free — so Stage 1 cannot open. The null is a boundary condition the paper's own mechanism predicts, and it explains M1b's refusal shift (30→43) that the camouflage hypothesis did not.
- **A proposed `synthetic_Y` positive-control arm was retired before any build or spend (D14)** — our corpus already fabricates both entities, which is the manipulation that cell performs. The recommendation was withdrawn by the session that made it.
- **v1 closed at M1 (D15).**

## Where things stand
M0 FIT, M1 NULL at both surfaces, v1 closed. Total spend ≈$0.027 against the <$5 budget. `main` carries M1; the reframing and correction are on `docs/paper-cell-mapping-correction` pending review + merge. Every number in the write-up artifacts is traceable to a committed file, and both verdicts re-derive from the wave logs with 0/240 rescore mismatches.

## Immediate next move
**`/research-paper`** — the write-up, built on D13's prior-dependence framing and `Wiki/Results.md`. The paper's argument is already assembled: two well-powered nulls, a rendered flagship artifact (n=2, reported as an existence proof not a rate), the withdrawn comparison stated openly, and the structural limitation that the judge-free detector and the paper's mechanism are mutually exclusive. Then **`/seed-hunt`** for repro #6.

## Open questions / blockers
- None blocking. Nothing further to run: M2/M3 degenerate at DG≈0, the cure arm has nothing to cure, the specialization arm has no headroom off a 0–2/20 base (and `qwen-2.5-coder-7b` is gone from OpenRouter), and the prior axis is unreachable judge-free.
- **The one open scientific question, stated as a limitation rather than attempted:** whether DG appears on a fabricated corpus when the *evidence* matches a prior while entities stay fabricated. Not reachable without forfeiting exact token ownership.
- Watch for an arXiv v2 (reference-only either way; re-read in full 2026-08-03, still v1, no code).
- Six review follow-ups (nice-to-have) are listed on PR #9; none blocks the write-up.

## Files touched recently
- `Wiki/Paper-Mapping.md` (new) — the axis table, the withdrawn comparison, the prior-dependence reasoning. **Read this first.**
- `Wiki/Results.md`, `Wiki/Why-The-Null.md` — corrected and reframed.
- `Decisions.md` — D12 (correction), D13 (reframe), D14 (arm retired), D15 (v1 closed); D11 superseded.
- `README.md`, `PROJECT.md`, `CLAUDE.md` — headline reframed to prior-dependence.
- `docs/M1-BRIEF.md` — "M1 outcome" addendum (the results of record); frozen pre-commitments above it stand as written.
