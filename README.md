# blind-cite

[![CI](https://github.com/ksdisch/blind-cite/actions/workflows/ci.yml/badge.svg)](https://github.com/ksdisch/blind-cite/actions/workflows/ci.yml)

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

**M1 COMPLETE — gate verdict NULL at both surfaces at N=20 (2026-08-03).** ("Well-powered" was claimed here and is withdrawn — see the correction below. **The null itself did not survive M1C**: at the pre-registered N=80 the stark surface reads 3/80 with a lower bound above zero — see the M1C section. The measurements below stand as recorded; the inference drawn from them does not.) D-M1 resolved to Option C: M1a ran exactly as pre-committed, then M1b as a labeled camouflage arm (JSON tool-result rendering, constant titles, k=4 off-theme filler docs), both at 20 pairs. Every model held **20/20 clean trials in both gated cells on both arms**; 240/240 calls ok, zero vague, zero confabulation; fidelity gate 288/288. DG was 0/20 everywhere except `qwen-2.5-7b` at the camouflaged adversarial cell (2/20; Newcombe +0.100 [−0.077, +0.301] — straddled 0, so the paired gate read NULL *at that N*; M1C's N=80 look reversed it to +0.087 [+0.024, +0.170], DG-EFFECT). Per-model Wilson 95% upper bound on DG: **16.1%** for every model/arm on 0/20 — except that one `qwen-2.5-7b` camouflaged cell, whose interval is **[2.8%, 30.1%]**.

**The flagship blindness contrast rendered** on those two answers: mechanical **faithfulness PASS 2/2 and citation PASS 2/2** while token ownership flags both — Y's evidence attributed to X by name, Y never mentioned, a genuinely retrieved doc cited. Every standard check is blind; only ownership sees it. n=2 is an existence proof of the mechanism, not a rate, and was reported as such — M1C raised it to **ten answers with a rate interval attached**.

**What the result means — corrected twice on 2026-08-04, both corrections recorded in [`Wiki/Paper-Mapping.md`](Wiki/Paper-Mapping.md).** Three successive framings of this section have been withdrawn, all failing the same way: comparing our rate against a paper cell that is not the one we ran.

**There is no cell-matched anchor.** The paper's Appendix C (Fig. 6) does publish per-cell rates for all 13 of its models — the nearest cell for our design is `Qwen2.5-7B, absent × prior_completing = 14%` — but that is *not our condition*, for three verified reasons: (1) §4/Appendix A **define** `prior_completing` as evidence elicited to match a model's parametric prior for X, and our evidence is fabricated tokens matching no prior; (2) paper §5.2 (and Appendix C Table 8) states those absolutes are *"lower bounds for non-L1 models"*, so 14% is a floor, not a value; (3) Fig. 6 is the RAG-4 schema, Tables 1–2 are 10-tool, and **we ran neither**.

> **What we can say:** direction only, against a floor at a cell that is not ours and a schema we did not run. **What we cannot say:** that we reproduced it, contradicted it, or that the phenomenon disappears. No point comparison is legitimate here.

**And M1 was underpowered even for that.** At N = 20/cell, 0/20 has a Wilson upper of 16.1% — above the floor; `0/24` is the smallest run that would clear it. The pre-committed N ≥ 20 came from M0's clean-**trial-yield** funnel, never from a power calculation against a target effect size. **That mis-sizing is the project's main methodological finding about itself**, and it is why a pre-registered power-sized extension was designed and committed (Decisions.md D19 → D23) rather than the result being written up as-is.

## M1C — the extension ran, and the null did not survive it

**M1C (2026-08-04, D24).** Combined **N=80** clean trials per gated cell per surface on `qwen-2.5-7b`, one look, analysis and report templates frozen in advance ([`docs/M1C-BRIEF.md`](docs/M1C-BRIEF.md)).

| surface | original (N=20) | extension-only (N=60) | **combined (N=80)** | template |
|---|---|---|---|---|
| stark | 0/20 [0.0%, 16.1%] | 3/60 [1.7%, 13.7%] | **3/80 [1.3%, 10.5%]** | **T2** — occurs, low |
| camouflaged | 2/20 [2.8%, 30.1%] | 5/60 [3.6%, 18.1%] | **7/80 [4.3%, 17.0%]** | **T3** — comparable magnitude, hedged |

**DG occurs at both surfaces once N is adequate.** The stark surface — where M1 measured 0/20 and reported a null — reads 3/80 with a Wilson lower bound above zero. M1's measurement stands; the inference "DG ≈ 0" drawn from it does not. This is D18's self-diagnosis bearing out on the project's own data.

**The blindness contrast now rests on ten answers, not two** — 3 stark + 7 camouflaged, **faithfulness PASS 10/10, citation PASS 10/10**.

The secondary paired gate is reported beside the primary and never conflated with it: Newcombe delta stark +0.037 [−0.015, +0.105] (straddles 0 → NULL), camouflaged +0.087 [+0.024, +0.170] (excludes 0 → DG-EFFECT). DG-Y is impossible by construction at `absent × null_control`, so the paired interval carries the control's own width and is the more conservative of the two.

240/240 calls ok first pass; zero errored, vague or confabulated; 180 doc generations with 0 rejections; fidelity 1068/1068; DG-any 0/160. **Principal limitation (D25):** engagement at the adversarial cell runs 35% on M1's pairs vs 55–65% on the extension's — the stages are not behaviourally exchangeable and the combined row pools them. Reported, not adjusted for.

M1 spend $0.0177 (cap $0.45); M1C $0.0446 (cap $0.10); project total ≈$0.072 of the <$5 budget. Results: the "M1C outcome" addendum in [`docs/M1C-BRIEF.md`](docs/M1C-BRIEF.md), [`Wiki/Results.md`](Wiki/Results.md), and the machine-rendered [`data/m1c_verdict.json`](data/m1c_verdict.json) / [`data/m1a_verdict.json`](data/m1a_verdict.json) / [`data/m1b_verdict.json`](data/m1b_verdict.json). Source of truth: [`docs/KICKOFF.md`](docs/KICKOFF.md).

## Honesty contract
Reproduce-and-measure, never invent. Judge-free deterministic scoring only. Per-trial mechanical verification of the manipulation. Pre-committed gates as code, dry-run before paid data; nulls are headlines. Direction + structure, never point estimates.

---

📚 **Project wiki:** [PROJECT.md](PROJECT.md) — status, scope, and next actions · [Wiki/_index.md](Wiki/_index.md) — topic pages and history
