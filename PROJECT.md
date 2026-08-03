# PROJECT.md

## Purpose
Reproduce and measure **deceptive grounding** (arXiv 2607.09349) on cheap models at hobby scale: a RAG answer about queried entity X that passes standard faithfulness/hallucination/citation checks yet attributes entity Y's evidence to X — using a fully-controlled fabricated API/library corpus so the detector is pure token-ownership string-matching (no LLM judge). Reproduction #5 in the forge-gap → decay-pin → lossy-wall → ghost-patch lineage.

## Scope
**In (v1):** fabricated sibling-library corpus with globally-unique owned tokens; controlled deterministic retrieval (no vector DB); reduced 2×2 factorial (Cx ∈ {absent, complete} × Cy ∈ {null_control, completing}); four mechanical detectors (DG, confabulation, faithfulness proxy, citation proxy); milestones M0 (fit-pilot) → M1 (DG exists + blindness contrast, flagship) → M2 (protection boundary) → M3 (token-strip ablation); ≥2 pilot-surviving cheap OpenRouter models; Wilson/Newcombe CIs; pre-committed verdict scripts.

**Out / deferred / never:** LLM judges in grading (never); frontier/70B/medical models; real learned retriever; tool-calling apparatus (docs inline instead — documented deviation); the paper's production 7.8%/740-pair measurement; specialization arm and cure arm (gated stretch/post-v1); importing lineage or paper code (patterns only). Full scope contract: `docs/KICKOFF.md` (source of truth).

## Current status
**v1 CLOSED at M1 (2026-08-03).** M0 and M1 both complete; D15 closes v1.

M0 fit-pilot: verdict FIT — all three subjects survive, grounding at ceiling, detector fidelity 16/16, generator rejection 0/36, DG = 0/36 at the adversarial cell (all K4 "robust-low-DG for the right reason"), spend ≈$0.009.

**Headline (D13):** deceptive grounding is **prior-dependent**. The paper's mechanism opens when "disease-context overlap activates a parametric attribution prior"; this corpus fabricates both entities and all their evidence — the property that makes the detector judge-free — so no prior exists and the effect disappears. Measured judge-free and well-powered across two presentation surfaces and three cheap models. The earlier "paper-contradicting" framing was withdrawn as not cell-matched (D12); see `Wiki/Paper-Mapping.md`.

M1 ran as Option C (Decisions.md D6) — both surfaces, sequenced, at 20 pairs. **Verdict: NULL at both, well-powered** (D10). Every model held 20/20 clean in both gated cells on both arms; 240/240 trials ok on first pass; zero vague, zero confabulation, zero errors; fidelity gate 288/288. DG-Y was 0/20 everywhere except `qwen-2.5-7b` at the *camouflaged* adversarial cell (2/20; Newcombe +0.100 [−0.077, +0.301] — straddles 0, so the null stands). **The flagship blindness contrast rendered** on those 2 answers: faithfulness PASS 2/2, citation PASS 2/2 — Y's evidence attributed to X by name, Y never mentioned, a real doc cited, every standard check blind. DG-any 0/120 under k=4 fillers. M1 spend $0.0177 / $0.45; project total ≈$0.027 of the <$5 budget. Paper re-checked 2026-08-03 (still v1, no code).

## Next actions
1. `/research-paper` — the write-up, built on the prior-dependence framing (D13) and `Wiki/Results.md`. Every number traceable to a committed file.
2. `/seed-hunt` — harvest lessons into the selection bar and pick repro #6.
3. Nothing further to run. M2/M3 are degenerate at DG≈0, the cure arm has nothing to cure, the specialization arm has no headroom off a 0–2/20 base, and the prior axis is unreachable judge-free — stated as a limitation, not attempted (D15).

## Boundaries
Hobby budget <$5 total (M0 spent ≈$0.009); N≥20 clean trials per gated cell or the gate auto-reports UNDERPOWERED; macOS, no GPU, no Docker; OpenRouter for all model calls (`OPENROUTER_API_KEY` in `.env`, never committed); honesty contract is non-negotiable — reproduce-and-measure, judge-free deterministic scoring, per-trial mechanical verification, pre-committed gates as code, nulls are headlines, direction + structure never point estimates.
