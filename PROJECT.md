# PROJECT.md

## Purpose
Reproduce and measure **deceptive grounding** (arXiv 2607.09349) on cheap models at hobby scale: a RAG answer about queried entity X that passes standard faithfulness/hallucination/citation checks yet attributes entity Y's evidence to X — using a fully-controlled fabricated API/library corpus so the detector is pure token-ownership string-matching (no LLM judge). Reproduction #5 in the forge-gap → decay-pin → lossy-wall → ghost-patch lineage.

## Scope
**In (v1):** fabricated sibling-library corpus with globally-unique owned tokens; controlled deterministic retrieval (no vector DB); reduced 2×2 factorial (Cx ∈ {absent, complete} × Cy ∈ {null_control, completing}); four mechanical detectors (DG, confabulation, faithfulness proxy, citation proxy); milestones M0 (fit-pilot) → M1 (DG exists + blindness contrast, flagship) → M2 (protection boundary) → M3 (token-strip ablation); ≥2 pilot-surviving cheap OpenRouter models; Wilson/Newcombe CIs; pre-committed verdict scripts.

**Out / deferred / never:** LLM judges in grading (never); frontier/70B/medical models; real learned retriever; tool-calling apparatus (docs inline instead — documented deviation); the paper's production 7.8%/740-pair measurement; specialization arm and cure arm (gated stretch/post-v1); importing lineage or paper code (patterns only). Full scope contract: `docs/KICKOFF.md` (source of truth).

## Current status
**Active (resumed 2026-08-03; parked 2026-07-15 → 2026-08-03).** M0 fit-pilot COMPLETE with verdict FIT: all three subjects survive, grounding at ceiling, detector fidelity 16/16, generator rejection 0/36, DG = 0/36 at the adversarial cell (all K4 "robust-low-DG for the right reason"), total spend ≈$0.009. On resume: `docs/M1-BRIEF.md` written arguing the M1 design decision (D5/D-M1 — pre-committed vs. camouflage variant vs. both sequenced, recommendation C); README reconciled with recorded reality; paper re-checked 2026-08-03 (still v1, no code). **Blocked on Kyle's D5 pick — no paid call until it resolves.**

## Next actions
1. **Kyle: resolve D5/D-M1** at `docs/M1-BRIEF.md` (Option A pre-committed / B camouflage / C both sequenced — C recommended). Record the pick in Decisions.md + a brief addendum.
2. Then pre-commit `m1.py` + gates per the pick, dry-run, smoke N≈5, and run at the sized corpus (20 pairs, from M0's measured funnel).
3. Pending Kyle (separate): flip the repo public again — README contradiction is fixed by this change; the flip was waiting on that plus the D-M1 decision.

## Boundaries
Hobby budget <$5 total (M0 spent ≈$0.009); N≥20 clean trials per gated cell or the gate auto-reports UNDERPOWERED; macOS, no GPU, no Docker; OpenRouter for all model calls (`OPENROUTER_API_KEY` in `.env`, never committed); honesty contract is non-negotiable — reproduce-and-measure, judge-free deterministic scoring, per-trial mechanical verification, pre-committed gates as code, nulls are headlines, direction + structure never point estimates.
