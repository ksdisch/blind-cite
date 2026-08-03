# blind-cite

**Reproduction #5** in a reproduce-and-measure research lineage (forge-gap → decay-pin → lossy-wall → ghost-patch). Take one published failure-mode claim, reproduce and measure a narrow slice on cheap models at hobby scale (<$5), under pre-committed statistical gates — never invent.

## One-liner
Reproduce and measure **deceptive grounding** (arXiv 2607.09349, Caruzzo, Yoo, Kim): a RAG answer about queried entity X that passes every standard faithfulness/hallucination/citation check yet attributes entity Y's evidence to X — using a fully-controlled fabricated API/library corpus so the entity-attribution detector is pure token-ownership string-matching (no LLM judge), and showing mechanically that standard checks are blind to it.

## Why
The paper (v1 2026-07-10; re-checked 2026-08-03, still v1) is unreplicated and ships **no code**. Its own entity-attribution detector is an LLM judge (Kimi-K2.5); on a corpus we author, entity-attribution becomes exact ground-truth **token ownership** — a stronger, judge-free version of the headline. This is the lineage's deliberate **range** pick: a new RAG + "the eval is blind" evaluation surface, reusing only the transferable statistics discipline.

The failure, concretely — two sibling fabricated libraries `Quill` (X) and `Quipp` (Y), each owning globally-unique tokens. Ask about **Quill**; the retrieved set carries a `Quipp` doc with `Quipp.force_sync()`. **Deceptive grounding = the Quill-answer cites `force_sync` as Quill's API.** A token-level faithfulness proxy *passes* (`force_sync` really is in a retrieved doc); the entity-attribution check *catches* it (`force_sync` is Quipp-owned).

## What success looks like (v1)
Core arms rendered by pre-committed verdict scripts (the per-milestone `m0.py`…`m3.py` pattern; `m0.py` shipped with M0, the rest land with their milestones) on real data, on ≥2 pilot-surviving cheap models, with Wilson/Newcombe CIs; every scored trial mechanically verified; the flagship "blindness contrast" rendered as a concrete artifact (answers where faithfulness + citation proxies pass 100% while entity-attribution flags them). A null is a reportable headline.

- **M0** — fit-pilot: grounding precondition + the mechanical detectors.
- **M1** — DG exists + the blindness contrast (flagship).
- **M2** — protection boundary (complete queried-entity evidence suppresses DG).
- **M3** — ablation: strip the completing tokens → DG vanishes, failures shift to confabulation.

## Status
**M0 fit-pilot COMPLETE — verdict FIT (2026-07-15).** All three subjects survive: detector fidelity 16/16, generator rejection 0/36, 144/144 pilot calls ok, grounding at ceiling. Headline: **DG = 0/36 at the adversarial cell** — every engagement was refusal or explicit discrimination, so all three models carry the K4 flag ("robust-low-DG for the right reason", the informative kind of null). Total spend ≈$0.009. Results: [`docs/M0-BRIEF.md`](docs/M0-BRIEF.md) (pilot-outcome addendum) + [`data/m0_verdict.json`](data/m0_verdict.json).

**M1 COMPLETE — verdict NULL at both surfaces, well-powered (2026-08-03).** D-M1 resolved to Option C: M1a ran exactly as pre-committed, then M1b as a labeled camouflage arm (JSON tool-result rendering, constant titles, k=4 off-theme filler docs), both at 20 pairs. Every model held **20/20 clean trials in both gated cells on both arms**; 240/240 calls ok, zero vague, zero confabulation; fidelity gate 288/288. DG was 0/20 everywhere except `qwen-2.5-7b` at the camouflaged adversarial cell (2/20; Newcombe +0.100 [−0.077, +0.301] — straddles 0, so the null stands). Per-model Wilson 95% upper bound on DG: **16.1%** for every model/arm on 0/20 — except that one `qwen-2.5-7b` camouflaged cell, whose interval is **[2.8%, 30.1%]**.

**The flagship blindness contrast rendered** on those two answers: mechanical **faithfulness PASS 2/2 and citation PASS 2/2** while token ownership flags both — Y's evidence attributed to X by name, Y never mentioned, a genuinely retrieved doc cited. Every standard check is blind; only ownership sees it. n=2 is an existence proof of the mechanism, not a rate, and is reported as such.

**What the null means — the v1 headline.** Not "the paper fails to replicate on cheap models": a direct re-read on 2026-08-03 showed that claim was never cell-matched (the 66.3% we had been citing is that model's **peak cell**, `absent × synthetic_Y`, and the paper publishes no per-cell breakdown for any non-calibration model — the comparison is withdrawn). The supported claim is sharper. The paper's mechanism is prior-driven — *"Stage 1 opens when disease-context overlap activates a parametric attribution prior"* — and this corpus fabricates **both** entities *and* all their evidence, precisely so that token ownership is exact and no training prior can contaminate it. There is nothing for a prior to activate, so by the paper's own account Stage 1 cannot open:

> **Deceptive grounding is prior-dependent. Remove the parametric prior and it disappears — DG 0/60 and 2/60 across two presentation surfaces and three cheap models, measured judge-free and well-powered.**

This is a boundary condition the paper's stated mechanism predicts, not a failed replication, and it explains why heavier camouflage moved answers into refusal rather than misattribution. The structural tension is worth stating plainly: **the property that makes this detector judge-free is the property that removes the paper's mechanism** — testing the prior axis needs entities the model already knows, which forfeits exact token ownership. That axis is a stated limitation, not an attempted arm. Full reasoning: [`Wiki/Paper-Mapping.md`](Wiki/Paper-Mapping.md).

M1 spend $0.0177 (cap $0.45); project total ≈$0.027. **v1 is closed at M1** (Decisions.md D15). Results: [`docs/M1-BRIEF.md`](docs/M1-BRIEF.md) ("M1 outcome" addendum), [`Wiki/Results.md`](Wiki/Results.md), and the machine-rendered [`data/m1a_verdict.json`](data/m1a_verdict.json) / [`data/m1b_verdict.json`](data/m1b_verdict.json). Source of truth: [`docs/KICKOFF.md`](docs/KICKOFF.md).

## Honesty contract
Reproduce-and-measure, never invent. Judge-free deterministic scoring only. Per-trial mechanical verification of the manipulation. Pre-committed gates as code, dry-run before paid data; nulls are headlines. Direction + structure, never point estimates.

---

📚 **Project wiki:** [PROJECT.md](PROJECT.md) — status, scope, and next actions · [Wiki/_index.md](Wiki/_index.md) — topic pages and history
