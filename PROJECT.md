# PROJECT.md

## Purpose
Reproduce and measure **deceptive grounding** (arXiv 2607.09349) on cheap models at hobby scale: a RAG answer about queried entity X that passes standard faithfulness/hallucination/citation checks yet attributes entity Y's evidence to X — using a fully-controlled fabricated API/library corpus so the detector is pure token-ownership string-matching (no LLM judge). Reproduction #5 in the forge-gap → decay-pin → lossy-wall → ghost-patch lineage.

## Scope
**In (v1):** fabricated sibling-library corpus with globally-unique owned tokens; controlled deterministic retrieval (no vector DB); reduced 2×2 factorial (Cx ∈ {absent, complete} × Cy ∈ {null_control, completing}); four mechanical detectors (DG, confabulation, faithfulness proxy, citation proxy); milestones M0 (fit-pilot) → M1 (DG exists + blindness contrast, flagship) → M2 (protection boundary) → M3 (token-strip ablation); ≥2 pilot-surviving cheap OpenRouter models; Wilson/Newcombe CIs; pre-committed verdict scripts.

**Out / deferred / never:** LLM judges in grading (never); frontier/70B/medical models; real learned retriever; tool-calling apparatus (docs inline instead — documented deviation); the paper's production 7.8%/740-pair measurement; specialization arm and cure arm (gated stretch/post-v1); importing lineage or paper code (patterns only). Full scope contract: `docs/KICKOFF.md` (source of truth).

## Current status
**Active — M0 and M1 complete; v1 does NOT close at M1** (D19 supersedes D15). A pre-registered, power-sized extension is approved and awaiting its planning session.

M0 fit-pilot: verdict FIT — all three subjects survive, grounding at ceiling, detector fidelity 16/16, generator rejection 0/36, DG = 0/36 at the adversarial cell (all K4 "robust-low-DG for the right reason"), spend ≈$0.009.

**Headline (D21 — three prior framings withdrawn).** The paper has **no cell for the condition we ran**: §4/Appendix A define `prior_completing` as evidence elicited to match a model's parametric prior for X, and ours is fabricated tokens matching no prior. Its nearest published cell (`Qwen2.5-7B, absent × prior_completing` = **14%**, Fig. 6, RAG-4) is explicitly a **lower bound for non-L1 models**, and we ran neither of the paper's schemas. So only a hedged **directional** statement is legitimate: our rates sit at or below that floor while the paper's completing-Cy regime for that model spans 14% → 61%. No point comparison, no verb claiming agreement or disagreement. Withdrawn along the way: "paper-contradicting" (D12→D16), "prior-dependence, well-powered" (D13→D17), "consistent with the paper at our exact cell" (D17→D21). See `Wiki/Paper-Mapping.md`.

**And underpowered for even that (D18).** 0/20's Wilson upper is 16.1%, above the floor; `0/24` is the smallest run that clears it. The pre-committed N≥20 came from M0's clean-**trial-yield** funnel, never from a power calculation. That mis-sizing is the project's main methodological finding about itself.

M1 ran as Option C (Decisions.md D6) — both surfaces, sequenced, at 20 pairs. **Gate verdict: NULL at both** (D10) — but see the headline above: "well-powered" was claimed and is withdrawn (D17/D18); the wave met its pre-committed N, which was sized for clean-trial yield, not for power against a 14% effect. Every model held 20/20 clean in both gated cells on both arms; 240/240 trials ok on first pass; zero vague, zero confabulation, zero errors; fidelity gate 288/288. DG-Y was 0/20 everywhere except `qwen-2.5-7b` at the *camouflaged* adversarial cell (2/20; Newcombe +0.100 [−0.077, +0.301] — straddles 0, so the null stands). **The flagship blindness contrast rendered** on those 2 answers: faithfulness PASS 2/2, citation PASS 2/2 — Y's evidence attributed to X by name, Y never mentioned, a real doc cited, every standard check blind. DG-any 0/120 under k=4 fillers. M1 spend $0.0177 / $0.45; project total ≈$0.027 of the <$5 budget. Paper re-checked 2026-08-03 (still v1, no code).

## Next actions
1. **Plan the pre-registered, power-sized extension (D19, approved).** A dedicated Fable session designs it *with* Kyle before anything is built or spent: target N from a power calculation against 14% **as a reference magnitude for sizing** (never as a null hypothesis about our cell — D21), and against a plausibly higher value given the lower-bound caveat and the ~2× schema discrepancy, the optional-stopping guard, the analysis pre-commitment, and how it is reported **alongside** — never in place of — the original N=20 result. Est. **≈$0.06** including the corpus extension it needs.
2. Then run it under the standing discipline (gates committed → dry-run → `ping` → smoke → wave → verdict), and only then `/research-paper`.
3. Then `/seed-hunt` for repro #6.

## Boundaries
Hobby budget <$5 total (M0 spent ≈$0.009); N≥20 clean trials per gated cell or the gate auto-reports UNDERPOWERED; macOS, no GPU, no Docker; OpenRouter for all model calls (`OPENROUTER_API_KEY` in `.env`, never committed); honesty contract is non-negotiable — reproduce-and-measure, judge-free deterministic scoring, per-trial mechanical verification, pre-committed gates as code, nulls are headlines, direction + structure never point estimates.
