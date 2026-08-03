# blind-cite — project context

Reproduction #5 (lineage: forge-gap → decay-pin → lossy-wall → ghost-patch). Reproduce and measure **deceptive grounding** — entity-attribution failure in RAG (arXiv 2607.09349, Caruzzo, Yoo, Kim) — on cheap models: a RAG answer about queried entity X that passes every standard faithfulness/hallucination/citation check yet attributes entity Y's evidence to X. Built on a fully-controlled fabricated API/library corpus so the DG detector is pure token-ownership string-matching, never an LLM judge.

- **Source of truth:** `docs/KICKOFF.md` (approved 2026-07-15). Milestones, gates, scope, and the honesty contract live there — follow them exactly.
- **Current milestone:** **M0 and M1 both COMPLETE (2026-08-03).** M0 fit-pilot: verdict FIT, DG 0/36 at the adversarial cell, all three models K4 "right-reason", spend ≈$0.009. M1 ran as Option C at 20 pairs (Decisions.md D6): **verdict NULL at both surfaces, well-powered** (D10) — 20/20 clean per gated cell per model on both arms, 240/240 calls ok, zero vague/confab, fidelity 288/288; DG 0/20 everywhere except `qwen-2.5-7b` camouflaged (2/20, CI straddles 0). **The flagship blindness contrast rendered** on those 2 answers (faithfulness PASS 2/2, citation PASS 2/2). DG-any 0/120 under fillers. M1 spend $0.0177/$0.45. See `docs/M1-BRIEF.md` "M1 outcome" addendum, `Wiki/Results.md`, `data/m1{a,b}_verdict.json`. **Next action: Kyle's call on D11 (Proposed) — close v1 at M1**, since M2 suppresses a rate already ~0 and M3 ablates a phenomenon that occurred twice. The two documented escalations (position-assigned title pool; same-theme filler generation) each need their own argued addendum before any spend.
- **Riskiest assumption (keep front-of-mind):** cheap models must actually *ground* their answers in the retrieved docs (bar entry 10 precondition). Two failure directions — capability cliff (too weak to do RAG → no DG possible) and competence ceiling (too skeptical → notices docs are about Y and refuses → DG nulls for the *right* reason). A low DG rate from *non-engagement* is uninformative — M0 measures grounding rate separately and gates on it.
- **Honesty contract (non-negotiable):** reproduce-and-measure, never invent; deterministic judge-free scoring — the DG detector is token-ownership string-matching, never an LLM judge; per-trial mechanical verification of the manipulation; pre-committed gates as code, dry-run before paid runs; nulls are headlines; direction + structure, never point estimates; N≥20 clean trials per gated cell or the gate auto-reports UNDERPOWERED; the paper's code (if a v2 ships it) is reference-only, never imported.
- **Budget:** hobby, <$5 target (lineage precedent ≈$1.4–2 total). Measured-rate cost estimate before every paid wave; N≈5 smoke before every paid arm.
- **Reuse posture:** RANGE pick — new RAG/eval-blindness surface. Reuse the lineage measurement discipline (Wilson/Newcombe + metered OpenRouter client + gates-as-code) as a **pattern only**, never import lineage code. No Docker (no code execution).
- **Conventions:** ratified in docs/M0-BRIEF.md D9 — flat scripts at repo root; per-milestone verdict scripts `m0.py`…`m3.py` with subcommands (`ping|fidelity|gen-docs|smoke|pilot|verdict` pattern); `test_*.py` alongside for pure logic (pytest, no network); shared modules `corpus.py` / `assemble.py` / `detectors.py` / `prompts.py` / `client.py` / `stats.py`; frozen seeded corpus + derived data committed under `data/`; briefs at `docs/M<N>-BRIEF.md`; `OPENROUTER_API_KEY` in `.env` (never committed).

## Claude tooling for this repo

Global commands (`.claude/commands/`) and skills (`.claude/skills/`) vendored from `ksdisch/claude-config` via `/claudify-repo`, so they work in cloud/web sessions and for collaborators. ✅ = cloud-safe (pure reasoning + repo edits). 💻 = **local-only** — needs local tools (browser MCP, Chrome, local TTS/voice, or the local `nlm` CLI / NotebookLM MCP) and will NOT work in a cloud/web session.

### Commands

- ✅ `/autonomous-milestone` — plan/build/test/verify a target end-to-end, or triage the backlog into ranked candidates; ultracode multi-agent orchestration.
- ✅ `/begin` — open a session: orient on branch/commits/open PRs, recap the last `/wrap` log, route into the session-start spec. (Optional audio recap is local-only.)
- 💻 `/boot_server` — detect how the project is served, start the dev server in the background, open it in Chrome.
- ✅ `/brainstorm` — multi-mode structured brainstorm (Moonshot default; QuickWin, Subtract, Harden, Premortem, Friction, Delight, Positioning, Reach); blind agent teams + critic gate → `docs/ideas/` vision docs + backlog stubs.
- 💻 `/catchup` — mid-session audio catch-up as an MP3 (local TTS); keeps working after.
- ✅ `/claudify-repo` — vendor global commands/skills into this repo and/or brainstorm repo-specific automations.
- 💻 `/envsetup` — open `.env` in the editor + the credential's generation page in Chrome, with a key stub pre-added.
- ✅ `/explore-plan` — explore → plan → confirm before any code; proposes 2–3 ranked approaches and waits for a pick.
- ✅ `/handoff` — generate a paste-ready handoff prompt for a fresh session; captures lessons + plan state. (Optional audio is local-only.)
- ✅ `/prompt-optimize` — one-shot prompt rewrite: diagnose, pick a workflow archetype + model + effort, return a ready-to-paste prompt. Advisory only.
- ✅ `/reframe-orchestrator` — reframe `.claude/orchestrator.md` into a mode-independent invariants & gates doc; docs-only.
- 💻 `/screenshot-iterate` — visual loop: implement against a mock, screenshot the running app, compare, iterate.
- 💻 `/smoke-test` — set up a manual smoke test: opens the needed pages in Chrome (auto-boots the dev server) and hands over a do-this-see-that checklist saved under `docs/smoke/`.
- ✅ `/tdd` — test-first loop: write failing tests, confirm they fail for the right reason, commit, then code until green without touching the tests.
- ✅ `/trim-context` — find and fix Claude Code token bloat (oversized CLAUDE.md, bloated memory, `.claude/` cruft); auto-applies fixes.
- ✅ `/wrap` — end-of-session recap: the why, vocabulary, active-recall quiz, next moves; saves a dated file. (Optional audio is local-only.)

### Skills (auto-trigger by description, or invoke by name)

- ✅ `artifacts-audit` — audit which engineering artifacts the repo should have; writes `docs/artifacts-plan.md`. Plans only.
- ✅ `artifacts-generate` — generate artifacts from `docs/artifacts-plan.md` (one-at-a-time or batch). Companion to `artifacts-audit`.
- 💻 `audio-series` — episodic NotebookLM audio series for an existing notebook (needs `nlm`/NotebookLM MCP).
- ✅ `bug-hunt` — proactive bug hunt: fan out finder agents, adversarially verify findings, ranked triage list; optional hand-off to a fix flow.
- 💻 `interview-prep` — init/maintain a NotebookLM interview-prep notebook from the local job-search dossier (needs `nlm`/NotebookLM MCP).
- ✅ `kickoff` — deep one-question-at-a-time discovery interview → approved kickoff brief + phased plan → scaffold the project + GitHub repo.
- 💻 `match-the-mock` — implement a UI against a mock and iterate via browser screenshots until it matches.
- ✅ `mini` — kick off a new mini project under `~/Projects/mini/` (short interview + scaffold).
- 💻 `narrate` — turn a short brief into a single-voice MP3 narration (local Kokoro TTS).
- 💻 `nlm-skill` — expert guide for the NotebookLM CLI (`nlm`) and MCP server.
- 💻 `notebook-assist` — refine artifacts / brainstorm / manage sources for an existing NotebookLM notebook.
- 💻 `notebook-init` — initialize a new NotebookLM notebook end-to-end.
- 💻 `notebook-merge` — merge 2+ overlapping NotebookLM notebooks into one unified notebook.
- ✅ `project-guide` — comprehensive point-in-time guide to the project (purpose, architecture, history, interview lens); saves a dated file. (Optional audio is local-only.)
- ✅ `research-paper` — end-of-project research paper + presenter pack from a completed repo's recorded results; opens a PR for review, never merges.
- ✅ `seed-hunt` — end-of-project seed hunt: verify closure, harvest lessons into the selection bar, sweep arXiv, decision brief. (Optional audio is local-only.)
- ✅ `ship-and-route` — land outstanding git work behind a review gate, walk the findings, route the next move with a starter prompt.
- 💻 `video-series` — episodic NotebookLM video series for an existing notebook (needs `nlm`/NotebookLM MCP).

To vendor more global tooling or brainstorm repo-specific automations, run `/claudify-repo`.

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
