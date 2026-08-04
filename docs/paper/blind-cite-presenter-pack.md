# blind-cite — presenter pack

*Companion to `blind-cite-paper.md`. Built so every claim in the paper can be defended live, traced to a file, and — where it was wrong — owned rather than argued.*

---

## The 60-second story

> There's a RAG failure where you ask about library X, the system retrieves a document about library Y, and the model answers X's question entirely with Y's method names and error codes — while citing the document it read. Every standard check passes: the claims *are* supported by a retrieved document, the citation *is* real. Nothing in a normal eval stack asks whose evidence it is. A paper describes this and calls it deceptive grounding, but it detects it with an LLM judge and ships no code. I reproduced it without a judge: I fabricated the whole corpus — sibling libraries that don't exist, each owning four globally-unique tokens — so "whose evidence is this" becomes an exact string lookup instead of a model's opinion. Three cheap models. My first two runs measured zero at the un-camouflaged surface and I reported a null. Then I audited my own sample size and found I'd sized it for how many trials would survive, not for what effect it could detect — at N=20 even a perfect zero couldn't rule out the magnitude I cared about. So I pre-registered a power-sized extension: fixed N, one look, the exact wording frozen in advance. DG occurs at both surfaces — 3 out of 80 and 7 out of 80, both lower bounds above zero. My measurement was right; the conclusion I drew from it was a power artifact. And on all ten deceptive answers, the faithfulness check and the citation check both passed — ten out of ten. That's the whole point: the eval is blind, and the fix is knowing who owns the token. Total spend: seven cents.

---

## Results at a glance

### The headline — M1C primary estimand, `qwen/qwen-2.5-7b-instruct`, DG-Y at `absent × completing`

| surface | original N=20 | extension-only N=60 | **combined N=80** | template fired |
|---|---|---|---|---|
| stark | 0/20 — [0.0%, 16.1%] — T0 | 3/60 — [1.7%, 13.7%] — T2 | **3/80 — [1.3%, 10.5%]** | **T2** — "occurs, low" |
| camouflaged | 2/20 — [2.8%, 30.1%] — T3 | 5/60 — [3.6%, 18.1%] — T3 | **7/80 — [4.3%, 17.0%]** | **T3** — "comparable magnitude, hedged" |

All three rows are always shown. Extension-only and combined fired the **same** template on each surface, so the pre-registration's side-by-side clause never fired.

### Per-milestone verdicts

| milestone | design | verdict | headline |
|---|---|---|---|
| **M0** fit-pilot | 12 pairs × 4 cells × 3 models = 144 trials | **FIT** | Grounding at ceiling (12/12 both complete-Cx cells, all models); **DG 0/36** at the adversarial cell; all three models flagged K4 "robust-low-DG, right reason"; fidelity 16/16; generator rejection 0/36; ≈$0.009 |
| **M1a** stark | 20 pairs × 2 cells × 3 models = 120 | **NULL** | DG 0/20 every model; Wilson upper 16.1%; engagement present (`discriminated` 7/8/15 of 20) |
| **M1b** camouflaged | 20 pairs × 2 cells × 3 models = 120 | **NULL** | DG 2/20 for qwen only (Newcombe +0.100 [−0.077, +0.301], straddles 0); **DG-any 0/120**; blindness contrast rendered on 2 answers |
| **M1C** extension | 60 new pairs × 2 cells × 2 surfaces = 240, qwen only | **DG occurs at both surfaces** | Stark 3/80 [1.3%, 10.5%] → T2; camouflaged 7/80 [4.3%, 17.0%] → T3; **blindness 10/10 and 10/10**; DG-any 0/160; fidelity 1068/1068; $0.0446 / $0.10 |

### Two estimands, never conflated

| | primary — Wilson on the arm cell | secondary — Newcombe on the paired difference |
|---|---|---|
| stark | 3/80, **[1.3%, 10.5%]** — excludes 0 | +0.037 **[−0.015, +0.105]** — straddles 0 → gate **NULL** |
| camouflaged | 7/80, **[4.3%, 17.0%]** — excludes 0 | +0.087 **[+0.024, +0.170]** — excludes 0 → gate **DG-EFFECT** |

They disagree at stark. That is expected, was scripted for in the dry-run before any spend, and is explained in one line below.

### The flagship artifact

**10 DG answers** (3 stark + 7 camouflaged) · **faithfulness proxy PASS 10/10** · **citation proxy PASS 10/10** · Y never named on any of them.

---

## Provenance table — claim → number → file

Every number said out loud, and where to open it live.

| # | Claim | Number | Source file |
|---|---|---|---|
| 1 | Stark DG at combined N | 3/80, Wilson [1.3%, 10.5%], band T2 | `data/m1c_verdict.json` → `surfaces.a.rows.combined` |
| 2 | Camouflaged DG at combined N | 7/80, Wilson [4.3%, 17.0%], band T3 | `data/m1c_verdict.json` → `surfaces.b.rows.combined` |
| 3 | Stark original / extension-only rows | 0/20 [0.0%, 16.1%] T0 · 3/60 [1.7%, 13.7%] T2 | `data/m1c_verdict.json` → `surfaces.a.rows.{original,extension_only}` |
| 4 | Camouflaged original / extension-only rows | 2/20 [2.8%, 30.1%] T3 · 5/60 [3.6%, 18.1%] T3 | `data/m1c_verdict.json` → `surfaces.b.rows.{original,extension_only}` |
| 5 | The two carried statements, verbatim | full T2 / T3 strings | `data/m1c_verdict.json` → `…combined.statement` |
| 6 | Secondary paired gate | stark +0.037 [−0.015, +0.105] NULL · camouflaged +0.087 [+0.024, +0.170] DG-EFFECT | `data/m1c_verdict.json` → `surfaces.{a,b}.newcombe_delta_combined`, `.verdict` |
| 7 | Blindness contrast | n_dg 3 / faith 3 / cit 3 · n_dg 7 / faith 7 / cit 7 | `data/m1c_verdict.json` → `…combined.blindness_contrast` |
| 8 | Which answers are the DG ones | stark p41, p52, p71 · camouflaged p14, p18, p21, p36, p52, p54, p70 | `data/m1ca_wave.jsonl`, `data/m1cb_wave.jsonl`, `data/m1b_wave.jsonl` (`scored.label == "DG"`) |
| 9 | The worked example (Munivex ← Muneshin) | answer text + all four Y tokens | `data/m1ca_wave.jsonl` (p41) · `data/corpus.json` (p41) |
| 10 | Label counts behind stage heterogeneity | stark 13/7 → 21/36/3 · camouflaged 13/5/2 → 27/28/5 | `data/m1c_verdict.json` → `…labels.absentxcompleting` |
| 11 | Engagement shares per stage | stark 35% → 65% · camouflaged 35% → 55% | `docs/M1C-BRIEF.md` "Limitations, stated"; `Decisions.md` D25; re-derived + asserted by `docs/paper/derived_contrasts.py` |
| 12 | Run quality | 240/240 ok, 0 vague, 0 confab, 0 errored | `docs/M1C-BRIEF.md` "What ran"; `errors: 0` in every row of `data/m1c_verdict.json` |
| 13 | Fidelity gate | 1068/1068 (M1C) · 288/288 (M1) · 16/16 (M0) | `data/m1c_verdict.json`, `data/m1{a,b}_verdict.json`, `data/m0_verdict.json` → `fidelity` |
| 14 | Contamination guard | DG-any 0/160 (M1C) · 0/120 (M1) | `data/m1c_verdict.json` → `…dg_any`; `data/m1b_verdict.json` |
| 15 | Document generation | 180 attempts, 0 rejections, generator `openai/gpt-4o-mini` | `data/gen_log_m1c.json` → `summary` |
| 16 | M1 per-model results | 0/20 all three stark; 2/20 qwen camouflaged; both arms NULL | `data/m1a_verdict.json`, `data/m1b_verdict.json` |
| 17 | M0 results | FIT, 3 survivors, DG 0/36, grounding 12/12, rejection 0.0, pairs_needed 20 | `data/m0_verdict.json` |
| 18 | The sizing table | 0/N Wilson upper: 16.1 / 13.8 / 6.0 / 4.6 / 3.1 % at N = 20 / 24 / 60 / 80 / 120 | `docs/M1C-BRIEF.md` D2; pinned by `test_m1c_sizing.py::test_zero_k_uppers` |
| 19 | Smallest N clearing the reference magnitude | 24 | `docs/M1C-BRIEF.md` D2; `test_m1c_sizing.py`; `Decisions.md` D22 |
| 20 | Power at N=80 (against "does DG occur at all") | 0.9998 if the true rate is 10%; 0.9835 if it is 5% — closed-form, not a p-value | `docs/M1C-BRIEF.md` D2; `test_m1c_sizing.py::test_power_closed_form` |
| 21 | Repeat-draw instability | 10 duplicates → 3 text differences, 2 label flips, 2 differing `prompt_tokens`; M1: 30 duplicates → 8 / 2 | `Decisions.md` D27; `docs/M1C-BRIEF.md` Limitations |
| 22 | Nearest published cell + its caveats | 14% (Fig. 6 / Appendix C, RAG-4); lower bound per §5.2; synthetic_Y 61% | `Wiki/Paper-Mapping.md` |
| 23 | Spend | M0 ≈$0.009 · M1 $0.017735 · M1C $0.044642 · total ≈$0.072 | `data/m1_spend.json`, `data/m1c_spend.json`, `docs/M0-BRIEF.md`; total in `PROJECT.md` |
| 24 | Every Wilson / Newcombe value re-derives | all assertions pass | `uv run docs/paper/derived_contrasts.py` |
| 25 | Every plotted number | printed to stdout | `uv run --with matplotlib docs/paper/figures.py` |

**Live demo that lands well:** run `uv run docs/paper/derived_contrasts.py`. It re-derives every interval in the paper through the repo's own `stats.py`, asserts each against the committed verdict file, and prints them. It writes nothing if anything mismatches.

---

## Anticipated Q&A

**Q: Why fabricate the corpus? Isn't that a manufactured gap?**
Yes, and it is labeled as manufactured everywhere it matters. It buys the one thing the whole project depends on: if the libraries and their tokens don't exist, a token in an answer *cannot* have come from pretraining — it can only have been copied from a retrieved document. That makes "whose evidence is this?" an exact set-membership lookup instead of a judgment call, which is what lets me drop the LLM judge. The cost is stated in the paper and is real: fabricating the evidence moves my condition off the target paper's grid entirely (see the residual question below).

**Q: Why is a null a result?**
Because the alternative is a file drawer. But note what actually happened here, because it's the more honest answer: I reported two nulls, then dismantled one of them myself. A null is a result *when it comes with a power argument*. Mine didn't — and when I sized properly, the stark null turned into 3/80 with a lower bound above zero. So my position is stronger than "nulls are results": a null needs its own power argument, and "we hit our pre-committed N" is not one if the N was sized for something else.

**Q: Then didn't you just keep collecting data until you got a result? That's p-hacking.**
It's the right question, and it's why the extension is a pre-registration rather than a top-up. Three guards, all fixed before any build or spend. **One:** the decision was argued in a written brief and approved before anything ran, and its *trigger* was the sizing audit, not the observed rate. **Two:** N, cells, primary estimand, secondary gate and the exact reporting language were frozen, and the verdict script ran **once**, after the full wave — no interim looks, and no wave decision keyed off a DG label. **Three:** the original N=20 result is reported beside the new one forever, never replaced, and the extension-only rows are shown as the unconditioned check. If the combined and extension-only rows had selected different reporting templates, the brief required printing both side by side. They didn't, and that's recorded either way. Also pre-committed: **no further extension regardless of outcome.** That clause is binding, and no further wave has run.

**Q: Why Wilson intervals rather than a normal approximation?**
Because every quantity here is a proportion and my cells live at the edges — several are exactly 0/N. The normal approximation gives a zero-width interval at k=0, which is nonsense: it would claim I'd *proved* 0%. Wilson is asymmetric near the boundaries, never escapes [0,1], and at 0/20 correctly reads [0%, 16.1%] — "consistent with about zero", not "zero". That 16.1% is exactly the number that later told me my study was underpowered, so the choice of interval is what surfaced the study's own flaw.

**Q: At stark, the Wilson interval excludes zero but the Newcombe gate reads NULL. Which is it?**
Both, and they answer different questions. The primary estimand asks "is the DG rate at the adversarial cell above zero?" — 3/80, lower bound 1.3%, yes. The secondary asks "is the adversarial cell higher than its paired control?" Now, DG-Y is **impossible by construction** at the control cell — the null document contains zero token-shaped strings — yet the Newcombe interval still carries that cell's own Wilson width (0/80 → upper 4.6%) into the difference, and at k=3 that's wider than the arm cell's distance from zero. So the paired test is strictly the more conservative instrument here, and its NULL is *not* evidence against occurrence. I report both, never one as the other, and the dry-run carried a scenario for exactly this case before I spent a cent.

**Q: How does this compare to the paper's number?**
It doesn't, and that's a finding rather than a dodge. Three published framings of that comparison came out of this project and all three were withdrawn — I have the ledger entries. The nearest published cell for my model reads 14%, and it is **not my cell**, for three structural reasons: the paper *defines* that condition as evidence matching the model's parametric prior for X, and mine is fabricated and matches no prior; the paper explicitly calls that figure a lower bound for non-calibration models; and it's from a schema I didn't run. None of those is statistical, so no amount of data fixes any of them. So I report direction only, through five templates I fixed in advance — the stark surface fired T2 ("occurs, low"), the camouflaged fired T3 ("comparable magnitude, hedged") — each carrying its caveats inline. **No p-value against any paper cell, no point comparison.**

**Q: So N fixed it. More data, better answer?**
No — and that's the correction I'd want a reviewer to catch me on before I made it. The extension's pairs didn't just give me more trials; they gave me materially more trials in which the model engaged at all. Engagement at the adversarial cell was 35% on the original pairs against 65% stark and 55% camouflaged on the new ones. The two stages aren't behaviourally exchangeable and the combined row pools them. **N and the engagement shift are both live, and this study separates neither.** A rate conditioned on engagement would sharpen it — my own pre-merge review named it as a nice-to-have — but that number isn't recorded in any committed file here, so it isn't in the paper. Manufacturing it after the fact is exactly what the pre-registration exists to prevent.

**Q: What's the un-validatable residual?**
Whether what I measured is the *same phenomenon* the paper measures. Judge-free detection needs fabricated evidence; the paper's completing-information axis needs evidence the model already believes. Those are mutually exclusive by construction, not by budget. So every cross-study statement I make stays directional however much data I collect, and I can't close the gap by writing more carefully. A reproduction can be honest about a hole it can't fill; it can't fill it with prose.

**Q: Why these three models?**
Cheap, open-weight, and available on OpenRouter at hobby budget — the lineage constraint is under $5 total, and this came in at seven cents. `qwen-2.5-7b` is the load-bearing pick: it's the cheap kin of the only model in the paper's cross-model matrix I have any anchor for, which is why it's the one the extension took to N=80. Two roster substitutions were forced by slug availability and are documented as deviations. And the extension's single-model scope is a limitation, not a design win: the other two stay at 0/20 with a 16.1% upper bound, which after everything above means **untested at power, not shown clean.**

**Q: How do I know the detectors are right?**
They're regex and set membership — no model anywhere in the grading path — and they're gated three ways. A hand-labeled fidelity set covering all label classes plus boundary traps had to pass 100% before any paid call (16/16 at M0, 288/288 at M1, 1068/1068 at M1C). Every generated document passes a mechanical verifier before entering the corpus, including a clause that the Y-document must never contain X's name — so the mis-attribution has to be the model's own act, never something the prompt handed it. And when the detector was amended for filler documents, all 144 committed M0 rows were re-scored byte-identically to prove the change was non-regressive. On top of that, the label rule is deliberately conservative: any mention of Y's name at all scores `discriminated`, not DG — so every rate I report is a floor.

**Q: What would you do next?**
Three things, in order. **Pin provider routing** — repeat draws aren't stable even at temperature 0; I have byte-identical prompts returning different token counts, which means different backends, so no committed rate here is exactly reproducible. That's a design change and belongs in a new pre-registration. **Re-sample the original pairs** rather than adding new ones, which would separate the N effect from the stage effect — the extension's own brief wrongly claimed that wasn't possible, and that error is recorded. **Unbundle the camouflage levers**, since rendering, titles and fillers all moved together. What I would *not* do is extend M1C: the stopping rule is binding, and anything further is a new study with its own brief.

**Q: Roads not taken?**
M2 (does the queried entity's own evidence suppress DG?) and M3 (strip the completing tokens and watch failures shift from DG to confabulation, flipping the faithfulness proxy from PASS to FAIL) were both designed and never run — they were judged degenerate against a rate near zero, and that judgement was made *before* the extension showed the rate isn't zero. They're live again on the new numbers, as new studies. Also parked: a `synthetic_Y` positive control (degenerate for a corpus that already fabricates every name), a prompt-level "verify entity ownership first" cure arm, and a specialization arm comparing a code-tuned model against its general sibling.

**Q: What's the single most important thing you learned?**
That the sizing step can be competent at the wrong question. My N came from a funnel that answered "how many trials will survive?" — a perfectly good question — and I read it as if it had answered "what effect could this detect?" Nothing in the process caught it, because the number was pre-committed, the gate was code, and the wave hit its target exactly. It took auditing my own pre-registration against a reference magnitude to see it. That's a failure mode I'll now check for by default, and it's the reason this paper reports a reversal against itself in the same detail as the positive result.

---

## Vocabulary crib

| Term | In one line |
|---|---|
| **Deceptive grounding (DG)** | An answer about X that presents another entity Y's evidence as X's, while every claim is still supported by a retrieved document — so faithfulness checks can't see it. |
| **DG-Y** | The primary measure: ≥1 Y-owned token in the answer **and** Y's name absent. The paper-analog quantity. |
| **DG-any / misattributed-other** | Descriptive only: a *third-party* filler library's token pulled into the answer. Never enters the gate. Read 0/160. |
| **Entity X / entity Y** | X is the library the question asks about; Y is its fabricated sibling whose document is the one actually retrieved. |
| **Owned token** | One of the four globally-unique strings (method, flag, error code, version) belonging to exactly one fabricated library. Ownership is exact map lookup. |
| **Cx / Cy** | The two factors: Cx = whether X's own evidence is retrieved (absent / complete); Cy = what Y's document is (null_control / completing). |
| **The adversarial cell** | `absent × completing` — X's documentation withheld, Y's completing document present. The only cell where DG is possible. |
| **Completing evidence** | Y's document answering the *shape* of X's question — method, flag, error, version — but for Y, as Y's. |
| **null_control** | Y's document with **zero** token-shaped strings. Hygiene cell: DG-Y is impossible there by construction. |
| **Stark surface** | Prose documents, entity-named titles, one document. The originally pre-committed presentation. |
| **Camouflaged surface** | JSON tool-results, one constant title for every document, plus 4 off-theme filler documents. Entity identity only inside the content. |
| **Faithfulness proxy** | PASS iff every token in the answer appears in *some* retrieved document. Passes on DG by construction — that's the blindness. |
| **Citation proxy** | PASS iff the answer cites ≥1 real retrieved doc and every token appears in a **cited** doc. Also passes on DG. |
| **`discriminated`** | The conservative rung: Y's tokens are present *and* Y is named. Not scored DG — which makes every reported DG rate a floor. |
| **`correct-refusal`** | The model says the documentation doesn't cover it. Non-refusal (discriminated + DG) is what "engagement" counts. |
| **Engagement** | Share of clean trials at the adversarial cell that were **not** a refusal. The quantity that shifted between stages: 35% → 55–65%. |
| **Blindness contrast** | The artifact: DG answers on which faithfulness and citation both PASS. 10/10 and 10/10 here. |
| **Wilson interval** | Confidence interval for a proportion that behaves correctly at 0/N and n/N and never leaves [0,1]. Every per-cell interval here. |
| **Newcombe interval** | Square-and-add interval for the *difference* between two proportions. The secondary paired gate. |
| **Fidelity gate** | The detectors must reproduce a hand-labeled answer set 100% before any paid call. 16/16 → 288/288 → 1068/1068. |
| **K1 / K4** | K1 = capability-cliff kill (can the model do RAG at all?). K4 = *not* a kill — "robust-low-DG for the right reason", a model that grounds fine but refuses or discriminates. |
| **UNDERPOWERED** | The auto-verdict when a gate doesn't reach its pre-committed clean N. Reported instead of a result, with the shortfall stated. |
| **Templates T0–T4** | Five reporting sentences frozen before the run, selected mechanically by where the Wilson interval falls relative to the reference magnitude. The only permitted verbs for the paper comparison. |
| **Reference magnitude (14%)** | The nearest published cell for this model — used for **sizing and wording only**, never as a null hypothesis, because it is a different condition, a stated lower bound, and a schema not run. |
| **Original / extension-only / combined** | The three pre-committed reporting scopes: N=20 (M1's), N=60 (new trials alone), N=80 (pooled). All three always shown. |
| **One look** | The verdict script runs exactly once, after the full wave. No interim aggregation, no optional stopping. |
| **Stage heterogeneity** | The principal limitation: the original and extension pairs elicit materially different engagement, and the combined row pools them. |
| **Seed-preserving extension** | Growing the corpus by appending only to two pools, so earlier pairs regenerate bit-identically — asserted against committed fixtures before anything is written. |

---

## Two things to have open on screen

1. `data/m1c_verdict.json` — every headline number, machine-rendered by a script that ran once.
2. A terminal at the repo root, ready to run `uv run docs/paper/derived_contrasts.py` — the whole numeric spine of the paper, re-derived and asserted in about a second.
