# History — blind-cite

> How this project got here: a chronological narrative of eras and milestones,
> reconstructed from merged PRs, git history, wrap logs, and ADRs.
> PR numbers, merge dates, tags, and SHAs are **Fact** by construction; rationale
> lines carry explicit labels (**Fact** when quoted from a PR body/ADR, **Inference**
> when reconstructed). Decisions are anchored by ID to the project's decision
> ledger — never restated here. **Append-only:** new milestones are added at the
> bottom (above the Mining coverage footer); existing entries are never rewritten.

## Origin — 2026-07

Reproduction #5 in the forge-gap → decay-pin → lossy-wall → ghost-patch lineage:
reproduce and measure **deceptive grounding** (arXiv 2607.09349) judge-free on a
fabricated corpus, chosen as a RANGE pick per the lineage selection bar — see D1 in
`Decisions.md`. First commit `a0733ed` (2026-07-15), scaffolded from the approved
kickoff brief at `docs/KICKOFF.md`.

## Era: Kickoff-to-park sprint (2026-07-15)

The entire active life of the project so far fit in one day: scaffold, pre-commit
the M0 design, build and run the fit-pilot, render the verdict, and park at that
evening's seed-hunt.

### M0 fit-pilot: verdict FIT — 2026-07-15
- **Landed:** pre-committed M0 brief, full judge-free harness (seeded 12-pair corpus, four mechanical detectors, controlled retrieval, metered client, 52 tests incl. 16/16 fidelity gate), and the paid waves → **verdict FIT**, total spend ≈$0.009 (PR #1, commit `049c5e4`)
- **Why:** gates and kill/swap triggers were committed as code before any paid call [Fact — PR #1 body] — see D2, D3 in `Decisions.md`
- **Headline:** DG = 0/36 at the adversarial cell with grounding at ceiling — all three subjects tripped the K4 flag (robust-low-DG for the right reason, an informative null) [Fact — PR #1 body]
- **Tradeoff:** the FIT verdict queued a fork rather than resolving it — pre-committed M1 (likely a well-powered NULL headline) vs. a documented camouflage-level variant — see D5 in `Decisions.md` (Unresolved)

### Parked at seed-hunt — 2026-07-15
- **Landed:** no code — the project was parked hours after the FIT verdict, displaced by the workspace/J-lens pick (dim-stage) and re-queued as default repro #6, with repo + approved KICKOFF + M0 results intact for resume — see D4 in `Decisions.md`

## Era: Parked maintenance (2026-07-17 – 2026-07-26)

No research work; the repo received fleet-wide upkeep so it stays resume-ready.

### Global Claude tooling vendored — 2026-07-17
- **Landed:** all missing global commands/skills from ksdisch/claude-config vendored into `.claude/`, CLAUDE.md tooling + operating-constraints sections refreshed (PR #2, commit `56b74ed`)
- **Why:** fleet-wide /claudify-repo sweep so tooling works in cloud/web sessions and for collaborators [Fact — PR #2 body]

### Project wiki initialized — 2026-07-26
- **Landed:** PROJECT.md, HANDOFF.md, Sources.md, Decisions.md created and CLAUDE.md wired to the project-wiki skill; no code or data changes (PR #3, merge `7ec3647`)
- **Why:** capture resume-ready state for the parked repo — status, the open M1 design call, and the source index [Fact — PR #3 body]

## Era: Resume & the M1 decision (2026-08-03 – )

The park ended with a docs-first resume: reconcile the repo's story, argue the
M1 design fork, and put it to Kyle before any code or spend.

### M1 decision brief written; README reconciled — 2026-08-03
- **Landed:** `docs/M1-BRIEF.md` arguing D5 (A pre-committed / B camouflage variant / C both sequenced — C recommended), README truth-fix (no more "M0 not yet started"), resume-state wiki updates (PR #8)
- **Why:** D5 must be argued at a brief and decided by Kyle, never slipped in [Fact — `docs/M0-BRIEF.md` addendum] — see D5 in `Decisions.md` (Unresolved)
- **Also:** paper re-checked 2026-08-03 — still v1, no code; the brief's E3 records the presentation-layer reading (JSON tool-result format; §5.3 mismatch-detection claim) [Fact — arXiv fetch, recorded in the brief]

---

## Mining coverage
_Backfilled 2026-07-26 by project-wiki BACKFILL. Entries after this date are
appended live by MAINTAIN._
- PR title sweep: all 3 merged PRs — no cap
- Deep reads: 3 of 3 PRs (under the 20 cap; first and most recent included)
- Fewer than 5 merged PRs → degenerate case: milestones derived from the commit log (5 commits, no tags) plus docs of intent (`docs/KICKOFF.md`, `docs/M0-BRIEF.md`) and the decision ledger `Decisions.md` (D1–D5, anchored not restated)
- Also swept: git log (merges/no-merges), tags (none), wrap logs (none — no `docs/session-logs/` or `.claude/session-logs/`), ADRs (none)
- Not mined: closed-unmerged PRs, issues
