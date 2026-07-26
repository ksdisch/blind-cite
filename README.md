# blind-cite

**Reproduction #5** in a reproduce-and-measure research lineage (forge-gap → decay-pin → lossy-wall → ghost-patch). Take one published failure-mode claim, reproduce and measure a narrow slice on cheap models at hobby scale (<$5), under pre-committed statistical gates — never invent.

## One-liner
Reproduce and measure **deceptive grounding** (arXiv 2607.09349, Caruzzo, Yoo, Kim): a RAG answer about queried entity X that passes every standard faithfulness/hallucination/citation check yet attributes entity Y's evidence to X — using a fully-controlled fabricated API/library corpus so the entity-attribution detector is pure token-ownership string-matching (no LLM judge), and showing mechanically that standard checks are blind to it.

## Why
The paper (v1 2026-07-10) is days old, unreplicated, and ships **no code**. Its own entity-attribution detector is an LLM judge (Kimi-K2.5); on a corpus we author, entity-attribution becomes exact ground-truth **token ownership** — a stronger, judge-free version of the headline. This is the lineage's deliberate **range** pick: a new RAG + "the eval is blind" evaluation surface, reusing only the transferable statistics discipline.

The failure, concretely — two sibling fabricated libraries `Quill` (X) and `Quipp` (Y), each owning globally-unique tokens. Ask about **Quill**; the retrieved set carries a `Quipp` doc with `Quipp.force_sync()`. **Deceptive grounding = the Quill-answer cites `force_sync` as Quill's API.** A token-level faithfulness proxy *passes* (`force_sync` really is in a retrieved doc); the entity-attribution check *catches* it (`force_sync` is Quipp-owned).

## What success looks like (v1)
Core arms rendered by pre-committed verdict scripts (`m1.py`–`m3.py`) on real data, on ≥2 pilot-surviving cheap models, with Wilson/Newcombe CIs; every scored trial mechanically verified; the flagship "blindness contrast" rendered as a concrete artifact (answers where faithfulness + citation proxies pass 100% while entity-attribution flags them). A null is a reportable headline.

- **M0** — fit-pilot: grounding precondition + the mechanical detectors.
- **M1** — DG exists + the blindness contrast (flagship).
- **M2** — protection boundary (complete queried-entity evidence suppresses DG).
- **M3** — ablation: strip the completing tokens → DG vanishes, failures shift to confabulation.

## Status
**Scaffolded (2026-07-15).** Milestone 0 not yet started. Source of truth: [`docs/KICKOFF.md`](docs/KICKOFF.md).

## Honesty contract
Reproduce-and-measure, never invent. Judge-free deterministic scoring only. Per-trial mechanical verification of the manipulation. Pre-committed gates as code, dry-run before paid data; nulls are headlines. Direction + structure, never point estimates.

---

📚 **Project wiki:** [PROJECT.md](PROJECT.md) — status, scope, and next actions · [Wiki/_index.md](Wiki/_index.md) — topic pages and history
