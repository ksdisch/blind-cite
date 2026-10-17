# blind-cite — project context

Reproduction #5 (lineage: forge-gap → decay-pin → lossy-wall → ghost-patch). Reproduce and measure **deceptive grounding** — entity-attribution failure in RAG (arXiv 2607.09349, Caruzzo, Yoo, Kim) — on cheap models: a RAG answer about queried entity X that passes every standard faithfulness/hallucination/citation check yet attributes entity Y's evidence to X. Built on a fully-controlled fabricated API/library corpus so the DG detector is pure token-ownership string-matching, never an LLM judge.

- **Source of truth:** `docs/KICKOFF.md` (approved 2026-07-15). Milestones, gates, scope, and the honesty contract live there — follow them exactly.
- **Current milestone:** **M0, M1 and M1C all COMPLETE (2026-08-04).** M0 fit-pilot: verdict FIT, DG 0/36 at the adversarial cell, all three models K4 "right-reason", spend ≈$0.009. M1 ran as Option C at 20 pairs (Decisions.md D6): gate verdict NULL at both surfaces (D10 — its "well-powered" wording **withdrawn**, D17/D18); 240/240 calls ok, fidelity 288/288; DG 0/20 everywhere except `qwen-2.5-7b` camouflaged (2/20). **M1C (D24) then ran the pre-registered power-sized extension and the null did not survive it:** combined **N=80** per gated cell per surface on `qwen-2.5-7b`, one look — **stark 3/80 Wilson [1.3%, 10.5%] → template T2** ("occurs, low"), **camouflaged 7/80 Wilson [4.3%, 17.0%] → template T3** ("comparable magnitude, hedged"). The stark surface, where M1 read 0/20, now has a lower bound above zero: M1's *measurement* stands, the inference "DG ≈ 0" does not. Secondary paired gate reported beside it, never conflated: Newcombe stark +0.037 [−0.015, +0.105] (NULL), camouflaged +0.087 [+0.024, +0.170] (DG-EFFECT). **The flagship blindness contrast now rests on ten answers** — faithfulness PASS 10/10, citation PASS 10/10. 240/240 M1C calls ok first pass, zero vague/confab/errored, fidelity 1068/1068, DG-any 0/160, spend $0.0446/$0.10 (project ≈$0.072). Principal limitation **D25: stage heterogeneity** — engagement 35% on M1's pairs vs 55–65% on the extension's; reported, not adjusted for. See `docs/M1C-BRIEF.md` "M1C outcome" addendum, `Wiki/Results.md`, `data/m1c_verdict.json`.
- **The paper relationship is unchanged and still binding (D21):** no point comparison is legitimate. The paper has **no cell for the condition we ran** — §4/Appendix A define `prior_completing` by evidence elicited to match a model's prior for X, and ours is fabricated. The nearest published cell (Qwen2.5-7B, `absent × prior_completing`, RAG-4) reads **14%**, which paper §5.2 / Appendix C Table 8 call a **lower bound** for non-L1 models, and we ran neither of its schemas. **Report only through the M1C-BRIEF D4 templates** (T0–T4) — direction only, caveats inline, no p-value, no point comparison. Three headlines have been withdrawn here (D12→D16, D13→D17, D17→D21), each failing the same way. See `Wiki/Paper-Mapping.md`. **D3's stopping rule now binds: no further extension, whatever the result invites** — any further measurement is a new pre-registered study with its own brief. **Next action: `/research-paper`**, then `/seed-hunt` for repro #6.
- **Riskiest assumption (keep front-of-mind):** cheap models must actually *ground* their answers in the retrieved docs (bar entry 10 precondition). Two failure directions — capability cliff (too weak to do RAG → no DG possible) and competence ceiling (too skeptical → notices docs are about Y and refuses → DG nulls for the *right* reason). A low DG rate from *non-engagement* is uninformative — M0 measures grounding rate separately and gates on it.
- **Honesty contract (non-negotiable):** reproduce-and-measure, never invent; deterministic judge-free scoring — the DG detector is token-ownership string-matching, never an LLM judge; per-trial mechanical verification of the manipulation; pre-committed gates as code, dry-run before paid runs; nulls are headlines; direction + structure, never point estimates; N≥20 clean trials per gated cell or the gate auto-reports UNDERPOWERED; the paper's code (if a v2 ships it) is reference-only, never imported.
- **Budget:** hobby, <$5 target (lineage precedent ≈$1.4–2 total). Measured-rate cost estimate before every paid wave; N≈5 smoke before every paid arm.
- **Reuse posture:** RANGE pick — new RAG/eval-blindness surface. Reuse the lineage measurement discipline (Wilson/Newcombe + metered OpenRouter client + gates-as-code) as a **pattern only**, never import lineage code. No Docker (no code execution).
- **Conventions:** ratified in docs/M0-BRIEF.md D9 — flat scripts at repo root; per-milestone verdict scripts `m0.py`…`m3.py` with subcommands (`ping|fidelity|gen-docs|smoke|pilot|verdict` pattern); `test_*.py` alongside for pure logic (pytest, no network); shared modules `corpus.py` / `assemble.py` / `detectors.py` / `prompts.py` / `client.py` / `stats.py`; frozen seeded corpus + derived data committed under `data/`; briefs at `docs/M<N>-BRIEF.md`; `OPENROUTER_API_KEY` in `.env` (never committed).

## Claude tooling for this repo

Global commands (`.claude/commands/`) and skills (`.claude/skills/`) vendored from `ksdisch/claude-config` via `/claudify-repo`, so they work in cloud/web sessions and for collaborators. ✅ = cloud-safe (pure reasoning + repo edits). 💻 = **local-only** — needs local tools (browser MCP, Chrome, local TTS/voice, or the local `nlm` CLI / NotebookLM MCP) and will NOT work in a cloud/web session.

### Commands

- ✅ `/handoff` — generate a paste-ready handoff prompt for a fresh session; captures lessons + plan state.
- ✅ `/tdd` — test-first loop: write failing tests, confirm they fail for the right reason, commit, then code until green without touching the tests.

### Skills (auto-trigger by description, or invoke by name)

- ✅ `paper-gloss` — post-process a `/paper-eli5` output into a self-contained interactive HTML page with click-to-reveal jargon glosses, a glossary panel, and an annotation layer. Vendored for its `scripts/` and `assets/`, which `docs/papers/gloss/verify.py` runs; `/paper-eli5` itself is not vendored (it ships no scripts).


## Operating Constraints

@.claude/operating-constraints.md

## Project Wiki

This project uses the project-wiki skill. When integrating new sources, recording decisions, or pausing work:
- Update `PROJECT.md` status and next actions
- Update `HANDOFF.md` with what changed and what's next
- Add durable understanding to `Wiki/` topic pages
- Record decisions in `Decisions.md`
- Keep `Wiki/_index.md` current

(`Wiki/`, `Decisions.md`, and `Sources.md` are created on first need — templates live in the skill.)

Invoke the `project-wiki` skill when wiki updates are needed.
