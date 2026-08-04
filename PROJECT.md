# PROJECT.md

## Purpose
Reproduce and measure **deceptive grounding** (arXiv 2607.09349) on cheap models at hobby scale: a RAG answer about queried entity X that passes standard faithfulness/hallucination/citation checks yet attributes entity Y's evidence to X — using a fully-controlled fabricated API/library corpus so the detector is pure token-ownership string-matching (no LLM judge). Reproduction #5 in the forge-gap → decay-pin → lossy-wall → ghost-patch lineage.

## Scope
**In (v1):** fabricated sibling-library corpus with globally-unique owned tokens; controlled deterministic retrieval (no vector DB); reduced 2×2 factorial (Cx ∈ {absent, complete} × Cy ∈ {null_control, completing}); four mechanical detectors (DG, confabulation, faithfulness proxy, citation proxy); milestones M0 (fit-pilot) → M1 (DG exists + blindness contrast, flagship) → M2 (protection boundary) → M3 (token-strip ablation); ≥2 pilot-surviving cheap OpenRouter models; Wilson/Newcombe CIs; pre-committed verdict scripts.

**Out / deferred / never:** LLM judges in grading (never); frontier/70B/medical models; real learned retriever; tool-calling apparatus (docs inline instead — documented deviation); the paper's production 7.8%/740-pair measurement; specialization arm and cure arm (gated stretch/post-v1); importing lineage or paper code (patterns only). Full scope contract: `docs/KICKOFF.md` (source of truth).

## Current status
**v1 CLOSED at M1 (2026-08-03).** M0 and M1 both complete; D15 closes v1.

M0 fit-pilot: verdict FIT — all three subjects survive, grounding at ceiling, detector fidelity 16/16, generator rejection 0/36, DG = 0/36 at the adversarial cell (all K4 "robust-low-DG for the right reason"), spend ≈$0.009.

**Headline (D17, supersedes D13):** measured against the paper's cell-matched anchor for our exact model — **Qwen2.5-7B, `absent × prior_completing` = 14%** (Appendix C, Fig. 6) — our camouflaged result of 2/20 (10%, [2.8%, 30.1%]) is **consistent with the paper**, not a refutation (exact binomial p = 0.455). At N = 20/cell the study cannot resolve 14% from 0. The gate's NULL is a correct gate outcome, not evidence of absence. The earlier "paper-contradicting" and "prior-dependence, well-powered" framings are both **withdrawn** (D12 corrected by D16; D13 by D17) — see `Wiki/Paper-Mapping.md`.

M1 ran as Option C (Decisions.md D6) — both surfaces, sequenced, at 20 pairs. **Gate verdict: NULL at both** (D10) — but see the headline above: "well-powered" was claimed and is withdrawn (D17/D18); the wave met its pre-committed N, which was sized for clean-trial yield, not for power against a 14% effect. Every model held 20/20 clean in both gated cells on both arms; 240/240 trials ok on first pass; zero vague, zero confabulation, zero errors; fidelity gate 288/288. DG-Y was 0/20 everywhere except `qwen-2.5-7b` at the *camouflaged* adversarial cell (2/20; Newcombe +0.100 [−0.077, +0.301] — straddles 0, so the null stands). **The flagship blindness contrast rendered** on those 2 answers: faithfulness PASS 2/2, citation PASS 2/2 — Y's evidence attributed to X by name, Y never mentioned, a real doc cited, every standard check blind. DG-any 0/120 under k=4 fillers. M1 spend $0.0177 / $0.45; project total ≈$0.027 of the <$5 budget. Paper re-checked 2026-08-03 (still v1, no code).

## Next actions
1. **Kyle's call (open):** close v1 on the honestly-underpowered result, or run a **pre-registered, power-sized extension** on the one cell-matched model (`qwen-2.5-7b`) to resolve 14% vs ~0. ~$0.02 at measured rates. This would be an N-extension after seeing data, so it is only legitimate if argued in an addendum, fixed in advance, and reported alongside the original N=20 result — never as a replacement for it.
2. Whatever is decided: `/research-paper` must compare to **14%**, not 66.3%, and use "consistent with" rather than "disappears".
3. Then `/seed-hunt` for repro #6.

## Boundaries
Hobby budget <$5 total (M0 spent ≈$0.009); N≥20 clean trials per gated cell or the gate auto-reports UNDERPOWERED; macOS, no GPU, no Docker; OpenRouter for all model calls (`OPENROUTER_API_KEY` in `.env`, never committed); honesty contract is non-negotiable — reproduce-and-measure, judge-free deterministic scoring, per-trial mechanical verification, pre-committed gates as code, nulls are headlines, direction + structure never point estimates.
