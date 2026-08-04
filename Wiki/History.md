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
- **Landed:** `docs/M1-BRIEF.md` arguing D5 (A pre-committed / B camouflage variant / C both sequenced — C recommended), README truth-fix (no more "M0 not yet started"), resume-state wiki updates (PR #8, merge `1beb5ac`)
- **Why:** D5 must be argued at a brief and decided by Kyle, never slipped in [Fact — `docs/M0-BRIEF.md` addendum] — see D5, D6 in `Decisions.md`
- **Also:** paper re-checked 2026-08-03 — still v1, no code; the brief's E3 records the presentation-layer reading (JSON tool-result format; §5.3 mismatch-detection claim) [Fact — arXiv fetch, recorded in the brief]

### M1 built and run — both surfaces, verdict NULL — 2026-08-03
- **Landed:** `m1.py` + `test_m1.py` with every gate as code and dry-run on synthetic answers **before** the first paid call; corpus extension 12→20 pairs (seed-preserving, append-only pools, M0 fixtures pinned); the misattributed-other/confabulation detector split; the M1b camouflage surface (JSON tool-results, constant titles, k=4 off-theme fillers); both paid arms and their verdicts (PR #9)
- **Why:** Option C runs the pre-commitment untouched and tests the fidelity-faithful surface beside it, converting the forking-paths objection into a measured factor [Fact — `docs/M1-BRIEF.md` D3] — see D6, D10 in `Decisions.md`
- **Headline:** NULL at both surfaces, well-powered — 20/20 clean per gated cell per model on both arms, DG-Y 0/20 everywhere except `qwen-2.5-7b` at the camouflaged adversarial cell (2/20, CI straddles 0). **The flagship blindness contrast rendered** on those 2 answers: faithfulness PASS 2/2, citation PASS 2/2 [Fact — `data/m1b_verdict.json`]
- **Tradeoff:** rendering, fillers and constant titles were bundled as one camouflage lever, so a positive result could not have been attributed to any one of them; accepted for a descriptive first pass and stated as a limitation up front [Fact — `docs/M1-BRIEF.md` D2 risks]
- **Also:** `m1.py ping` caught price drift on two Qwen slugs before anything spent — see D7; the $0.45 M1 ceiling was made an enforced ledger cap after D4's table proved to under-count its own smoke row — see D8. Total M1 spend $0.0177

### Paper re-read; three headlines withdrawn; extension approved — 2026-08-03/04
- **Landed:** direct re-read of arXiv 2607.09349 (§4, Tables 1–2, Appendix A, limitations; still v1, no code) → the 66.3% Qwen2.5-7B anchor is that model's **peak** cell, not our gated cell, so the "paper-contradicting for cheap models" claim was withdrawn; new `Wiki/Paper-Mapping.md`; headline reframed, then reframed again after review (PR #10 — merge SHA to be backfilled on the next wiki touch)
- **Why:** the comparison was checked before a write-up could inherit it — the honesty contract's "direction + structure, never point estimates" applies to the *comparison* as much as to our own numbers [Fact — the correction commit body] — see D12, D13 in `Decisions.md`
- **Headline (as finally established):** the paper has **no cell for the condition this project ran** — §4/Appendix A define `prior_completing` by evidence elicited to match a model's prior for X, and ours is fabricated. Only a hedged directional statement against a 14% *lower bound*, at a schema we did not run, is reportable [Fact — `Wiki/Paper-Mapping.md`] — see D21 in `Decisions.md`
- **Correction in flight:** **three** headlines were published and withdrawn inside this one PR — "paper-contradicting for cheap models" (D12→D16, premise false), "prior-dependence, well-powered" (D13→D17, sized against the wrong anchor), and "consistent with the paper at our exact cell" (D17→D21, the cell is not ours). Adversarial review caught the second and third; all withdrawals are recorded rather than hidden [Fact — PR #10 review F1/F2, F9/F10]
- **Also:** the pre-registration gap recorded as D18 — the pre-committed N came from clean-trial yield, not a power calculation — and D19, Kyle's approval of a pre-registered power-sized extension, to be planned before anything is spent
- **Tradeoff:** the judge-free detector and the paper's grid are mutually exclusive — reaching the completing-information axis needs evidence a model already believes, forfeiting exact token ownership. Recorded as a limitation, not attempted
- **Also:** a `synthetic_Y` positive-control arm was proposed, approved, then retired before any build or spend — as degenerate for this corpus, not (as D14 first recorded) because we "already perform the manipulation" — see D14, corrected by D20

### Corrections merged after a five-round review; M1C pre-registration committed — 2026-08-04
- **Landed:** PR #10 squash-merged as `2de0f1b` — the full correction campaign: 23 findings over 5 review rounds across 2 runs, every one fixed and verified, zero waivers (Kyle flipped the final nice-to-haves to fix-now at the round-4 triage gate); resolves the prior entry's "merge SHA to be backfilled" note. Then `docs/M1C-BRIEF.md`, the pre-registered power-sized extension design (this PR)
- **Why:** run 1 hit the 3-dispatch cap NOT CLEAR with six fixes unverified; Kyle ruled for a fresh verification round rather than a waiver, and rounds 4–5 closed everything [Fact — review mailbox; adjudicated PR #10 comment] — see D23 in `Decisions.md`
- **Headline:** the extension is sized by a real power calculation this time — combined N=80 per gated cell per surface makes every reachable outcome map to exactly one of five pre-committed direction-only templates, with the D21 caveats inline and the sizing table pinned by `test_m1c_sizing.py` [Fact — `docs/M1C-BRIEF.md` D2/D4]
- **Tradeoff:** combined-N primary analysis maximizes precision at the cost of conditioning on stage-1 data; bounded by the one-look guard and by always reporting the extension-only rows beside it [Fact — `docs/M1C-BRIEF.md`, "The argument, ruled"]

### M1C — the pre-registered extension ran, and the null did not survive it — 2026-08-04
- **Landed:** PR #12, squash-merged as `f1230fc` — the D23 pre-registration executed end to end: PR #11's two pre-freeze follow-ups (F15/F16) first, then p01–p20 pinned as `data/corpus_m1.json` / `data/docs_m1.json`, the corpus appended to 80 pairs, `m1c.py` + `test_m1c.py`, a full dry-run, the `ping` price re-pin, smoke on both arms, both waves (240/240 ok, first pass), and `m1c.py verdict` run **once**
- **Why:** D18 recorded that M1's N came from clean-trial yield rather than a power calculation and could not resolve the nearest published floor; D19 approved an extension only if argued in advance, fixed in advance, and reported alongside the original [Fact — `docs/M1C-BRIEF.md` "Why this document exists"] — see D19, D23, D24 in `Decisions.md`
- **Headline:** **DG occurs at both surfaces once N is adequate.** Combined N=80 per gated cell per surface on `qwen-2.5-7b` — stark **3/80, Wilson [1.3%, 10.5%] → template T2**; camouflaged **7/80, [4.3%, 17.0%] → template T3**. The stark surface, measured at 0/20 by M1, now has a lower bound above zero: the measurement stands, the "DG ≈ 0" inference does not. **The flagship blindness contrast rose from 2 answers to 10** — faithfulness PASS 10/10, citation PASS 10/10 [Fact — `data/m1c_verdict.json`] — see D24 in `Decisions.md`
- **Tradeoff:** combined-N primary analysis conditions on stage-1 data; bounded by the one-look guard and by reporting the extension-only rows beside it, which is also what made the run's largest limitation visible — engagement at the adversarial cell is 35% on M1's pairs against 55–65% on the extension's, and the combined row pools them [Fact — `data/m1c_verdict.json` label distributions] — see D25 in `Decisions.md`
- **Also:** the secondary paired gate disagrees with the primary on the stark arm (Newcombe +0.037 [−0.015, +0.105] straddles 0 while the Wilson interval excludes it). Not a defect: DG-Y is impossible by construction at `absent × null_control`, so the paired interval carries the control's own width and is strictly the more conservative. `m1c.py dryrun` carried a scenario for this exact case before any spend
- **Also:** measured spend $0.0446 against the $0.10 cap (estimate $0.052; 180 doc generations, 0 rejections, so the 30% retry margin went unused); fidelity 1068/1068 over the grown corpus; DG-any 0/160. D3's stopping rule now binds — no further extension, whatever the result invites

- **Also:** the pre-merge review ran three rounds and 12 findings, no disputes, every should-fix fixed and verified. **Two of them were defects the review's own fixes introduced** — pinning `m0.py` to `N_PAIRS_M0` turned its `gen-docs` into a write that would have deleted p13–p80 from the shared evidence bank (F6), and the promised D7 correction reached `Decisions.md` but not the brief (F7). Both caught by the next round [Fact — PR #12 mailbox]. Two pre-registration clauses were superseded on Kyle's merge call: D7's "untouched frozen records" (D26) and D5's "no re-sampling alternative" (D27, repeat draws are not stable at temperature 0 and provider routing is unpinned)

---

## Mining coverage
_Backfilled 2026-07-26 by project-wiki BACKFILL. Entries after this date are
appended live by MAINTAIN._
- PR title sweep: all 3 merged PRs — no cap
- Deep reads: 3 of 3 PRs (under the 20 cap; first and most recent included)
- Fewer than 5 merged PRs → degenerate case: milestones derived from the commit log (5 commits, no tags) plus docs of intent (`docs/KICKOFF.md`, `docs/M0-BRIEF.md`) and the decision ledger `Decisions.md` (D1–D5, anchored not restated)
- Also swept: git log (merges/no-merges), tags (none), wrap logs (none — no `docs/session-logs/` or `.claude/session-logs/`), ADRs (none)
- Not mined: closed-unmerged PRs, issues
