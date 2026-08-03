# PROJECT.md

## Purpose
Reproduce and measure **deceptive grounding** (arXiv 2607.09349) on cheap models at hobby scale: a RAG answer about queried entity X that passes standard faithfulness/hallucination/citation checks yet attributes entity Y's evidence to X — using a fully-controlled fabricated API/library corpus so the detector is pure token-ownership string-matching (no LLM judge). Reproduction #5 in the forge-gap → decay-pin → lossy-wall → ghost-patch lineage.

## Scope
**In (v1):** fabricated sibling-library corpus with globally-unique owned tokens; controlled deterministic retrieval (no vector DB); reduced 2×2 factorial (Cx ∈ {absent, complete} × Cy ∈ {null_control, completing}); four mechanical detectors (DG, confabulation, faithfulness proxy, citation proxy); milestones M0 (fit-pilot) → M1 (DG exists + blindness contrast, flagship) → M2 (protection boundary) → M3 (token-strip ablation); ≥2 pilot-surviving cheap OpenRouter models; Wilson/Newcombe CIs; pre-committed verdict scripts.

**Out / deferred / never:** LLM judges in grading (never); frontier/70B/medical models; real learned retriever; tool-calling apparatus (docs inline instead — documented deviation); the paper's production 7.8%/740-pair measurement; specialization arm and cure arm (gated stretch/post-v1); importing lineage or paper code (patterns only). Full scope contract: `docs/KICKOFF.md` (source of truth).

## Current status
**Active — M0 and M1 both COMPLETE (2026-08-03).**

M0 fit-pilot: verdict FIT — all three subjects survive, grounding at ceiling, detector fidelity 16/16, generator rejection 0/36, DG = 0/36 at the adversarial cell (all K4 "robust-low-DG for the right reason"), spend ≈$0.009.

M1 ran as Option C (Decisions.md D6) — both surfaces, sequenced, at 20 pairs. **Verdict: NULL at both, well-powered** (D10). Every model held 20/20 clean in both gated cells on both arms; 240/240 trials ok on first pass; zero vague, zero confabulation, zero errors; fidelity gate 288/288. DG-Y was 0/20 everywhere except `qwen-2.5-7b` at the *camouflaged* adversarial cell (2/20; Newcombe +0.100 [−0.077, +0.301] — straddles 0, so the null stands). **The flagship blindness contrast rendered** on those 2 answers: faithfulness PASS 2/2, citation PASS 2/2 — Y's evidence attributed to X by name, Y never mentioned, a real doc cited, every standard check blind. DG-any 0/120 under k=4 fillers. M1 spend $0.0177 / $0.45; project total ≈$0.027 of the <$5 budget. Paper re-checked 2026-08-03 (still v1, no code).

## Next actions
1. **Kyle's call (D11, Proposed):** close v1 at M1. M2 (suppress a rate already ~0) and M3 (ablate a phenomenon that occurred twice) are degenerate on the measured data — see the `docs/M1-BRIEF.md` outcome addendum.
2. If instead the null should be pushed on, the two documented escalations are available and each needs its own addendum first: a position-assigned title pool, then same-theme filler generation (new docs + new verifier contract).
3. Whenever v1 does close: `/research-paper` for the write-up, then `/seed-hunt` for repro #6.

## Boundaries
Hobby budget <$5 total (M0 spent ≈$0.009); N≥20 clean trials per gated cell or the gate auto-reports UNDERPOWERED; macOS, no GPU, no Docker; OpenRouter for all model calls (`OPENROUTER_API_KEY` in `.env`, never committed); honesty contract is non-negotiable — reproduce-and-measure, judge-free deterministic scoring, per-trial mechanical verification, pre-committed gates as code, nulls are headlines, direction + structure never point estimates.
