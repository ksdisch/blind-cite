# Kickoff Brief — blind-cite
*Created 2026-07-15 · status: scoped (approved 2026-07-15) · repo: github.com/ksdisch/blind-cite (private) · repro #5 (forge-gap → decay-pin → lossy-wall → ghost-patch)*

## One-liner
Reproduce and measure, on cheap models at hobby scale, **deceptive grounding** (arXiv 2607.09349, Caruzzo, Yoo, Kim): a RAG answer about queried entity X that passes every standard faithfulness/hallucination/citation check yet attributes entity Y's evidence to X — using a fully-controlled fabricated API/library corpus so the entity-attribution detector is pure token-ownership string-matching (no LLM judge), and showing mechanically that standard checks are blind to it.

## Why now / the problem
Fifth rung of the reproduce-and-measure lineage, and the deliberate **RANGE** pick (bar entry 8): RAG + "the eval is blind" is a genuinely new evaluation surface — it reuses none of ghost-patch's Docker/code-execution muscle, only the transferable statistics discipline (Wilson/Newcombe, pre-committed gates-as-code, mechanical verification). The paper is days old (v1 2026-07-10), unreplicated, and **ships no code** — an honest independent reproduction has real standalone value. The flagship claim is unusually clean to make *mechanical*: the paper's own detector is a Kimi-K2.5 judge (would hard-fail bar entry 2), but on a corpus we author, entity-attribution becomes exact ground-truth token ownership — a *stronger*, judge-free version of the paper's headline.

## Who it's for
Kyle — portfolio of honest reproductions + the learning arc. Recruiter-legible artifact: the repo + the flagship "blindness contrast" table (answers where a mechanical faithfulness+citation proxy passes 100% while entity-attribution flags them). New skill: building a controlled RAG evaluation harness and a judge-free detector for a failure mode that standard RAG evals structurally miss. Current alternative: the paper sits unreplicated; no released framework implements the mechanical check.

## What success looks like
- **v1 done means:** all core arms have pre-committed verdict scripts (`m1.py`–`m3.py` pattern) that ran on real data and rendered REPRODUCED / PARTIAL / NULL / UNDERPOWERED, on **≥2 pilot-surviving cheap models**, with Wilson/Newcombe CIs; every scored trial's manipulation mechanically verified; the flagship blindness contrast rendered as a concrete artifact; a null is a reportable headline.
- **Would be amazing:** a clean DG main effect (completing ≫ null, CI-separated) on 2+ models; a floor-clean protection boundary (complete-X evidence → DG≈0); an ablation that drives DG→~0 **and** mechanically shifts failures into confabulation (faithfulness proxy flips from PASS on DG → FAIL on confabulation — the mirror image); plus the gated specialization arm showing a code-tuned cheap model deceptively-grounds *more* than its general sibling (the paper's most surprising finding, on-domain).
- **Explicitly NOT trying to:** invent mechanisms; match the paper's point estimates (direction + structure only); use any LLM judge in grading; run frontier/70B or real medical models; reproduce the production 7.8%/740-pair measurement (needs a deployed system); build a real learned retriever.

## Scope
**In (v1):**
- **Fabricated API/library corpus** — ~30 entity-pairs, expandable (sibling made-up libraries, e.g. `Quill`/`Quipp`), each owning a frozen set of **globally-unique tokens** (method names, version strings, config flags, error codes). Authored + seed-prefixed like ghost-patch's bank; synthetic docs **LLM-drafted by a fixed non-roster generator, mechanically verified, frozen**.
- **Controlled retrieval, not learned** — the "retrieved doc set" for each trial is *deterministically assembled* per factorial condition (we hand the model exactly the docs the condition specifies). Faithful to the paper's controlled factorial; keeps everything deterministic and cheap. No vector DB, no embeddings.
- **Reduced factorial** — Cx (queried-entity X's own evidence) ∈ {absent, complete}; Cy (alternate-entity Y's doc) ∈ {null_control, completing}. Core cells carry the thesis; partial-Cx and non-completing-present-Cy gradations deferred to "if cheap."
- **M1 — DG exists + the blindness contrast (flagship, R1 analog):** completing Cy vs null_control at absent Cx. Primary: DG-rate delta (Newcombe CI excluding 0). Flagship: on DG-positive answers, mechanical faithfulness + citation proxies PASS (expected near-ceiling).
- **M2 — protection boundary (R2):** complete Cx vs absent Cx at completing Cy. DG suppressed under complete Cx (floor headline if ≈0).
- **M3 — ablation (causal mechanism, falsification arm):** within absent Cx × completing Cy, strip Y's completing tokens → DG→~0 **and** failures shift to confabulation (faithfulness proxy now FAILS).
- **Mechanical detectors (the heart):** (a) **DG detector** — a Y-owned token appearing in an X-answer = attribution of Y's evidence to X; (b) **confabulation detector** — a token-shaped string owned by *neither* entity; (c) **faithfulness proxy** — every evidence-token in the answer appears in *some* retrieved doc (PASSES on DG, FAILS on confabulation); (d) **citation proxy** — cited doc exists + contains the token. All pure regex + set-membership. Outcome taxonomy per trial is mutually exclusive and fully mechanical: DG / confabulation / correct-refusal / correct-answer.
- **Generator + mechanical verifier** (ghost-patch pattern): verifier confirms each Y-doc contains all intended Y-tokens + Y's name, contains **no** X-token (no leakage) and **no** direct mislabel instruction (the model must mis-attribute itself). Unverifiable doc = discard, rate reported.
- Roster: 3 cheap OpenRouter general models — `qwen-2.5-7b-instruct` (cheap kin of the paper's Qwen2.5-7B @ 66.3%), `llama-3.1-8b-instruct`, `gemma-2-9b-it`; bench `qwen-2.5-14b`, `gpt-oss-20b` (paper's low end @ 8.0%). M0 decides who survives.

**Out / deferred / never:**
- **Specialization-amplifies arm** (code-tuned `qwen-2.5-coder-7b` vs general `qwen-2.5-7b` at the adversarial cell — the on-domain analog of "medical fine-tunes worse, 86.7%") — **stretch, gated, descriptive.**
- **Cure arm** (a cheap prompt-level "verify entity ownership before answering" instruction — does DG collapse?) — **gated post-v1 flagship**, analogous to ghost-patch's parked cure arm.
- Tool-calling apparatus (paper's 10-/4-tool schemas) → docs presented inline instead (documented deviation); real retriever; partial-Cx & graded non-completing Cy (if-cheap only); LLM judges (never); >3 subject models; frontier/medical models; production/740-pair measurement; the paper's harness in our code (none exists; reference-only if a v2 ships one).

## Shape
CLI pipeline, lineage pattern: Python + JSON per-trial artifacts + per-milestone verdict scripts, run logs committed. **No Docker** (no code execution). New pieces vs the lineage: the controlled-retrieval assembly layer + the four mechanical detectors + the synthetic-doc generator/verifier.

## Inputs & data
**Fully self-authored — no external dataset, no access risk** (contrast ghost-patch's RunBugRun fetch). Entity pairs + owned-token maps authored and frozen; docs generated by a fixed non-roster model and mechanically verified. Fabricated names/tokens mean **zero training-prior contamination** (bar entry 4) — the model can only get tokens from the retrieved docs.

## Integrations & dependencies
OpenRouter (existing key) for subject models + the fixed generator model; GitHub via `gh` (authed as ksdisch). No dataset dependency, no Docker, no paper code.

## Constraints
Hobby budget (**<$5 target**; lineage precedent ≈$1.4–2 total); statistics is the binding constraint (N≥20 clean trials per gated cell, else the gate auto-reports UNDERPOWERED); macOS, no GPU; measured-rate cost estimate before every paid wave; N≈5 smoke before every paid arm.

## Riskiest assumptions & unknowns
1. **The precondition (bar entry 10) — cheap models must actually ground in retrieved docs.** Two failure directions, per-model: (a) **capability cliff** — too weak to do RAG at all, refuses/babbles made-up tokens → no DG possible; (b) **competence ceiling** — too skeptical, notices the docs are about Y and refuses to attribute → DG nulls for the *right* reason. Crucial denominator subtlety: a low DG rate from *non-engagement* is uninformative and must be distinguished from robust-low-DG. — *cheap test:* M0 pilot, N≈12 pairs × roster × core cells, measuring **grounding rate** (does the answer use retrieved tokens at all) separately from DG rate; require grounding ≥ threshold before trusting any DG number; per-model kill/swap triggers pre-committed.
2. **Detector fidelity** — the four mechanical detectors must classify hand-crafted answers correctly (no token-boundary/substring false positives, confabulation-vs-DG separation clean). — *cheap test:* M0 smoke: detectors run against a hand-labeled set of ~15 crafted answers spanning all four outcome classes; must match Kyle's labels 100% before any paid run.
3. **Generator + verifier viability** — synthetic docs must read as fluent, confident, self-consistently-about-Y API references and survive the mechanical verifier at a workable rate. — *cheap test:* M0 generates ~20 docs, measures rejection rate, Kyle spot-reads 5.
4. **Answer parseability** — answers must contain evaluable token-shaped strings; a model that answers in vague prose with no concrete tokens starves every detector. — *cheap test:* counted in M0; high vague-rate on a model = prompt fix or swap.
5. **Confound: framing must not instruct the mislabel** (bar entry 4). The Y-doc must be about Y and present Y's tokens as Y's; if it says "for X: [Y-token]" we've handed over the answer. — *mitigation:* verifier rejects X-name-adjacent-to-token; the mis-attribution must be the model's own act.

## Open questions
- Does a v2 with code/appendix appear? (Watch; reference-only either way.)
- Exact manipulation *direction* — confirm against the paper HTML at M0 that "completing information" = Y-owned tokens that complete the *shape* of an X-answer (the reproduction targets the phenomenon + structure, not the paper's exact template).
- Corpus sizing: M0's measured grounding funnel sets the final entity-pair count (computed, not guessed) so projected clean N ≥ 20/cell/model; authoring more pairs is nearly free.

## Phased plan
### Milestone 0 — Fit-pilot: the grounding precondition + the new muscle
- Author the fabricated API corpus (entities + frozen owned-token maps), build the controlled-retrieval assembler, the generator+verifier, and the four mechanical detectors; smoke-test detector fidelity against hand-labeled answers (risk 2).
- Pilot the roster on ~12 pairs across the core cells: **grounding rate**, DG signal at the adversarial cell (absent×completing), refusal/confabulation/vague rates (risks 1, 4). Kill/swap triggers **written before the pilot runs**.
- Pilot the generator+verifier (risk 3). Measured per-trial cost → corpus sizing (risk 5/open-q).
### Milestone 1 — DG exists + the blindness contrast (flagship, RQ1 analog)
- Freeze the verified corpus. Run completing vs null_control at absent Cx across the roster; `m1.py` pre-committed + dry-run (Newcombe delta, gate: DG drop from completing→null ≥ threshold with CI excluding 0). Render the flagship: faithfulness+citation proxies PASS on DG-positive answers.
### Milestone 2 — Protection boundary (RQ2 analog)
- complete Cx vs absent Cx at completing Cy; `m2.py`; gate: DG suppressed under complete Cx (Newcombe CI excluding 0; floor headline if ≈0).
### Milestone 3 — Ablation / causal mechanism (RQ analog, falsification arm)
- Strip Y's completing tokens within absent×completing; `m3.py`; primary DG→~0 (floor); secondary: failures shift to confabulation (faithfulness proxy flips PASS→FAIL).
### Stretch (gated, descriptive) — Specialization amplifies
- code-tuned vs general cheap model at the adversarial cell: does specialization raise DG on-domain?
### Post-v1 (gated) — The cure arm
- Cheapest intervention the paper never tests at the prompt level: an explicit "verify the evidence is about the queried library before citing it" instruction — does DG collapse?

## Tech stack
Python 3.12 + uv; `openai` SDK → OpenRouter; hand-rolled Wilson/Newcombe (port the *pattern* from lossy-wall's `stats.py` — our own code); no external stats deps; no Docker. Rationale: the proven lineage stack minus code-execution, plus the controlled-retrieval + detector layer as the one new component.

## Honesty contract (inherited, non-negotiable)
Reproduce-and-measure, never invent. Judge-free deterministic scoring only — the DG detector is token-ownership string-matching, never an LLM judge. Per-trial mechanical verification of the manipulation. Pre-committed gates as code, dry-run before paid data; nulls are headlines. Direction + structure, never point estimates. Fit-pilot with kill/swap triggers before any grid. Paper harness (if ever released): reference-only, never imported.
