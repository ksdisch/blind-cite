# blind-cite

**Reproduction #5** in a reproduce-and-measure research lineage (forge-gap → decay-pin → lossy-wall → ghost-patch). Take one published failure-mode claim, reproduce and measure a narrow slice on cheap models at hobby scale (<$5), under pre-committed statistical gates — never invent.

## One-liner
Reproduce and measure **deceptive grounding** (arXiv 2607.09349, Caruzzo, Yoo, Kim): a RAG answer about queried entity X that passes every standard faithfulness/hallucination/citation check yet attributes entity Y's evidence to X — using a fully-controlled fabricated API/library corpus so the entity-attribution detector is pure token-ownership string-matching (no LLM judge), and showing mechanically that standard checks are blind to it.

## Why
The paper (v1 2026-07-10) is days old, unreplicated, and ships **no code**. Its own entity-attribution detector is an LLM judge (Kimi-K2.5); on a corpus we author, entity-attribution becomes exact ground-truth **token ownership** — a stronger, judge-free version of the headline. This is the lineage's deliberate **range** pick: a new RAG + "the eval is blind" evaluation surface, reusing only the transferable statistics discipline.

The failure, concretely — two sibling fabricated libraries `Quill` (X) and `Quipp` (Y), each owning globally-unique tokens. Ask about **Quill**; the retrieved set carries a `Quipp` doc with `Quipp.force_sync()`. **Deceptive grounding = the Quill-answer cites `force_sync` as Quill's API.** A token-level faithfulness proxy *passes* (`force_sync` really is in a retrieved doc); the entity-attribution check *catches* it (`force_sync` is Quipp-owned).

## What success looks like (v1)
Core arms rendered by pre-committed verdict scripts (the per-milestone `m0.py`…`m3.py` pattern; `m0.py` shipped with M0, the rest land with their milestones) on real data, on ≥2 pilot-surviving cheap models, with Wilson/Newcombe CIs; every scored trial mechanically verified; the flagship "blindness contrast" rendered as a concrete artifact (answers where faithfulness + citation proxies pass 100% while entity-attribution flags them). A null is a reportable headline.

- **M0** — fit-pilot: grounding precondition + the mechanical detectors.
- **M1** — DG exists + the blindness contrast (flagship).
- **M2** — protection boundary (complete queried-entity evidence suppresses DG).
- **M3** — ablation: strip the completing tokens → DG vanishes, failures shift to confabulation.

## Status
**M0 fit-pilot COMPLETE — verdict FIT (2026-07-15).** All three subjects survive: detector fidelity 16/16, generator rejection 0/36, 144/144 pilot calls ok, grounding at ceiling. Headline: **DG = 0/36 at the adversarial cell** — every engagement was refusal or explicit discrimination, so all three models carry the K4 flag ("robust-low-DG for the right reason", the informative kind of null). Total spend ≈$0.009. Results: [`docs/M0-BRIEF.md`](docs/M0-BRIEF.md) (pilot-outcome addendum) + [`data/m0_verdict.json`](data/m0_verdict.json).

**Next: M1, pending decision D-M1** — run M1 as pre-committed (likely a well-powered null headline) vs. a documented camouflage-level design variant; argued in [`docs/M1-BRIEF.md`](docs/M1-BRIEF.md), decided by Kyle before any paid call. M1 is sized at 20 pairs from M0's measured funnel. Source of truth: [`docs/KICKOFF.md`](docs/KICKOFF.md).

## Honesty contract
Reproduce-and-measure, never invent. Judge-free deterministic scoring only. Per-trial mechanical verification of the manipulation. Pre-committed gates as code, dry-run before paid data; nulls are headlines. Direction + structure, never point estimates.

---

📚 **Project wiki:** [PROJECT.md](PROJECT.md) — status, scope, and next actions · [Wiki/_index.md](Wiki/_index.md) — topic pages and history
