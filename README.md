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

**M1 COMPLETE — gate verdict NULL at both surfaces (2026-08-03).** ("Well-powered" was claimed here and is withdrawn — see the correction below.) D-M1 resolved to Option C: M1a ran exactly as pre-committed, then M1b as a labeled camouflage arm (JSON tool-result rendering, constant titles, k=4 off-theme filler docs), both at 20 pairs. Every model held **20/20 clean trials in both gated cells on both arms**; 240/240 calls ok, zero vague, zero confabulation; fidelity gate 288/288. DG was 0/20 everywhere except `qwen-2.5-7b` at the camouflaged adversarial cell (2/20; Newcombe +0.100 [−0.077, +0.301] — straddles 0, so the null stands). Per-model Wilson 95% upper bound on DG: **16.1%** for every model/arm on 0/20 — except that one `qwen-2.5-7b` camouflaged cell, whose interval is **[2.8%, 30.1%]**.

**The flagship blindness contrast rendered** on those two answers: mechanical **faithfulness PASS 2/2 and citation PASS 2/2** while token ownership flags both — Y's evidence attributed to X by name, Y never mentioned, a genuinely retrieved doc cited. Every standard check is blind; only ownership sees it. n=2 is an existence proof of the mechanism, not a rate, and is reported as such.

**What the result means — corrected 2026-08-04.** Two successive framings of this section were wrong and are recorded as withdrawn in [`Wiki/Paper-Mapping.md`](Wiki/Paper-Mapping.md). The paper's Appendix C (Figure 6) publishes per-cell DG matrices for **all 13 of its models**, and it gives the cell-matched anchor for our exact model at our exact condition: **Qwen2.5-7B, `absent × prior_completing` = 14%**. Measured against that:

| `qwen-2.5-7b` at the adversarial cell | measured | Wilson 95% | contains 14%? |
|---|---|---|---|
| M1a stark | 0/20 | [0.0%, 16.1%] | yes |
| M1b camouflaged | 2/20 = 10.0% | [2.8%, 30.1%] | yes |

> **The camouflaged result is consistent with the paper's published rate for the same model at the same cell (10% observed vs 14% expected, exact binomial p = 0.455). This is not a refutation of the paper, and at N = 20 per cell this study cannot resolve 14% from 0.**

The gate's NULL verdict is correct *as a gate outcome* — the Newcombe delta straddles zero — but it must not be read as "the phenomenon is absent." The pre-committed N ≥ 20 was derived from M0's clean-**trial yield**, never from a power calculation against a target effect size; 0/25 would have been the minimum needed to exclude 14%. That mis-sizing is the project's main methodological finding about itself, and it is reported rather than buried.

What survives, labelled **Inference** and not claimed as a headline: our corpus fabricates Y's name (matching the paper's `synthetic_Y`, which reads **61%** for this model) yet also fabricates all evidence (which no paper cell does), and we observe 0–10% — near `prior_completing`, far below `synthetic_Y`. That is consistent with completing information being load-bearing, which is what the paper itself argues. It is a confounded cross-study comparison at small N, not a measurement.

M1 spend $0.0177 (cap $0.45); project total ≈$0.027. **v1 closure (D15) is back with Kyle** — it was decided on the premise that nothing informative remained to run, and the 14% anchor changes that premise. Results: [`docs/M1-BRIEF.md`](docs/M1-BRIEF.md) ("M1 outcome" addendum), [`Wiki/Results.md`](Wiki/Results.md), and the machine-rendered [`data/m1a_verdict.json`](data/m1a_verdict.json) / [`data/m1b_verdict.json`](data/m1b_verdict.json). Source of truth: [`docs/KICKOFF.md`](docs/KICKOFF.md).

## Honesty contract
Reproduce-and-measure, never invent. Judge-free deterministic scoring only. Per-trial mechanical verification of the manipulation. Pre-committed gates as code, dry-run before paid data; nulls are headlines. Direction + structure, never point estimates.

---

📚 **Project wiki:** [PROJECT.md](PROJECT.md) — status, scope, and next actions · [Wiki/_index.md](Wiki/_index.md) — topic pages and history
