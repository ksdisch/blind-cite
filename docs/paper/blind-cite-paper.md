# Deceptive grounding is measurable without a judge — and a null at N=20 that did not survive a pre-registered extension to N=80

**A judge-free reproduction of entity-attribution failure in retrieval-augmented generation, on cheap models, under pre-committed gates**

*blind-cite · reproduction #5 in the forge-gap → decay-pin → lossy-wall → ghost-patch lineage · measurement phase closed 2026-08-04*

---

## Abstract

Deceptive grounding (DG) is a retrieval-augmented-generation failure in which an answer about queried entity X attributes another entity Y's evidence to X, while remaining entailed by the retrieved documents — and therefore invisible to standard faithfulness and citation checks. The primitive is described in arXiv 2607.09349 (Caruzzo, Yoo, Kim), which detects it with an LLM judge and ships no code. We reproduce and measure a narrow slice of it on three cheap open-weight models, replacing the judge with exact ground-truth token ownership over a **fabricated** corpus of sibling libraries whose evidence tokens are globally unique — so entity attribution is a string-matching fact, not a model's opinion. A fit-pilot (M0) established that the models ground in retrieved documents at ceiling (12/12 per model per grounded cell) and measured DG at **0/36** at the adversarial cell. A pre-committed run at N=20 per gated cell per model (M1) returned a NULL gate at two presentation surfaces, with DG 0/20 everywhere except `qwen-2.5-7b` camouflaged (2/20). We then recorded that this N had been derived from clean-trial *yield*, never from a power calculation, and ran a pre-registered, power-sized extension (M1C) to combined **N=80** per gated cell per surface on `qwen-2.5-7b`, one look, templates frozen in advance. DG occurs at **both** surfaces: stark **3/80, Wilson 95% [1.3%, 10.5%]**; camouflaged **7/80, [4.3%, 17.0%]**. The stark surface, measured at 0/20, now has a lower bound above zero — the measurement stands, the inference "DG ≈ 0" does not. On all **ten** DG answers the mechanical faithfulness proxy and citation proxy **both PASS (10/10 and 10/10)**. Total measured spend: ≈$0.072.

---

> **Framing, stated up front.** This is a reproduction, not a discovery. The phenomenon, its name, its factorial structure and its motivating claim are the target paper's; what is ours is a judge-free instrument for it, a measurement at hobby scale on cheap models, and an honest account of what that measurement can and cannot support. The corpus is **fabricated end to end** — both entities and all of their evidence — and the adversarial condition is **constructed** by withholding the queried entity's documentation. Both facts are load-bearing and are restated wherever a result depends on them. Every statistic below is lifted from a committed file in this repository; where a number is not recorded, the paper says so rather than estimating it.

---

## 1. Introduction

A retrieval-augmented system can fail in a way its own evaluation stack cannot see. Ask about library X; retrieve a document about library Y; get back a fluent, confident answer that fills every slot of X's question with Y's method names, Y's config flags, Y's error codes, Y's version string — and cites the document it came from. A faithfulness check asks "is every claim supported by a retrieved document?" and the answer is *yes*. A citation check asks "does the cited document exist and contain these strings?" and the answer is *yes*. The one question neither asks is **whose evidence this is**.

The target paper calls this deceptive grounding and reports it across thirteen models. It detects DG with an LLM judge (Kimi-K2.5, reported at 97.0% precision / 98.7% recall against a human gold set), and it releases no code. Both facts shaped this reproduction. An LLM judge is exactly the instrument this lineage's honesty contract forbids, and the absence of code means an independent implementation is the only implementation.

The move that makes the detector mechanical is to give up on realism in one specific place. If the corpus is **fabricated** — sibling libraries that do not exist, each owning four globally-unique token-shaped strings that appear nowhere else — then a token in an answer can only have arrived there by being copied out of a retrieved document, and "whose evidence is this?" reduces to an exact set-membership lookup. Entity attribution stops being a judgment call. That is a *stronger* instrument than the paper's on the narrow question it answers, and it is bought at a price this paper is explicit about in §6: fabricating the evidence moves the experimental condition off the target paper's grid entirely, and no amount of data brings it back.

The contribution is narrow and stated as such:

1. **A judge-free DG detector** and the corpus construction that makes it sound, with per-trial mechanical verification of the manipulation.
2. **A measured rate with an interval**, on one model at two presentation surfaces, from a pre-registered power-sized run: stark 3/80 [1.3%, 10.5%], camouflaged 7/80 [4.3%, 17.0%].
3. **The blindness contrast rendered as an artifact** — ten answers on which both standard proxies pass and only ownership catches the failure.
4. **A methodological finding about the project itself**: its own pre-committed N was sized for clean-trial yield rather than for power, and the null it produced did not survive the pre-registered extension that audit prompted. This paper reports that reversal against itself in the same detail as the positive result — including the reason (§5.7) that N is not the only thing which changed between the two stages, so the reversal is not attributed to N alone.

---

## 2. Background: the claim, and which part of it we reproduce

### 2.1 The target claim

arXiv 2607.09349 (Caruzzo, Yoo, Kim), v1 dated 2026-07-10, defines a response as exhibiting deceptive grounding when (1) it contains claims attributable to an entity Y ≠ X in the retrieved documents, (2) those claims are presented as evidence about X, and (3) all factual claims are entailed by the retrieved documents — hence invisible to standard faithfulness checks. That three-clause definition, recorded near-verbatim in this project's M0 brief before any measurement, is the definition our detector implements.

The paper's factorial crosses Cx (the queried entity's own evidence) ∈ {absent, partial, complete} with Cy (the alternate entity's document) ∈ {null_control, class_proximate, context_adjacent, prior_completing, synthetic_Y}. We reproduce a reduced 2×2: **Cx ∈ {absent, complete} × Cy ∈ {null_control, completing}**. The adversarial cell — the only cell where DG is possible by construction — is `absent × completing`: the queried entity's documentation is withheld, and the single on-theme document available answers the question's shape *for the other entity, as the other entity's*.

### 2.2 What we deliberately do not reproduce

No LLM judge, at any stage of grading. No tool-calling apparatus in the paper's exact schemas. No frontier or medical models, no production-scale measurement, no learned retriever. The paper's harness was never available to import, and would have been reference-only if it were.

One deferred arm deserves a note because it was proposed, approved, and then retired *before any build or spend*: a `synthetic_Y` positive control. That paper cell fabricates Y's **name** while holding the completing information constant, and the paper attributes the effect to the information half rather than the name half. Our corpus already fabricates every name; it cannot hold "information matching a prior about X" constant, because it has no priors to match. The arm is degenerate for this corpus — not, as this project's ledger first recorded, redundant because we "already perform the manipulation." The rationale was corrected in place.

---

## 3. Method

### 3.1 The fabricated corpus (manufactured, and labeled as such)

`corpus.py` deterministically generates the corpus from `SEED = 20260715`. Each pair is two sibling fabricated libraries — X (queried) and Y (alternate) — sharing one task theme, each owning exactly four tokens, one per category:

| category | shape (word-boundaried regex) | example |
|---|---|---|
| method | `[a-z]{3}_[a-z]{3,10}_[a-z]{3,10}` (optional trailing `()`) | `xff_rotate_transfer` |
| flag | `[a-z]{3}\.[a-z]{3,10}_[a-z]{3,10}` | `xff.pinned_collar` |
| error | `[A-Z]{3}-E[0-9]{3}` | `XFF-E494` |
| version | `[0-9]+\.[0-9]+\.[0-9]+` | `4.8.19` |

Generation enforces and unit-tests the invariants the detector depends on: every token globally unique across the corpus, no token a substring of another, no library name a substring of another, stems unique per library. Because names and stems are invented, **no token can enter an answer except by being copied from a retrieved document** — the single assumption under all four detectors.

Each pair carries one question demanding exactly those four categories: *"In the ⟨X⟩ library, which method ⟨does task⟩, which config flag enables it, which error code signals ⟨failure⟩, and which version introduced it?"* Y's completing document answers that same shape **for Y, as Y's**.

The corpus grew twice, both times **seed-preserving and append-only** (only the theme and name-prefix pools were extended, so `build_corpus` — which consumes the RNG in pair order — leaves earlier pairs bit-identical): 12 pairs at M0, 20 at M1, 80 at M1C. Each growth pinned the prior pairs as committed fixtures and asserted them byte-unchanged before writing.

### 3.2 Document generation and mechanical verification

Documents are drafted by a fixed non-roster generator (`openai/gpt-4o-mini`, never graded) and accepted only if they pass a pure string-matching verifier:

| document | verifier contract |
|---|---|
| X-doc | all 4 X tokens ≥1×, X name ≥2×, zero Y tokens, zero Y name, **no other token-shaped strings** |
| Y-completing | all 4 Y tokens ≥1×, Y name ≥2×, zero X tokens, **zero X name anywhere**, no other token-shaped strings |
| Y-null | Y name ≥2×, **zero token-shaped strings of any kind**, zero X name |

"No other token-shaped strings" is load-bearing: one stray identifier in a document would corrupt both the confabulation detector and the faithfulness proxy. "Zero X name anywhere" in the Y-doc is the anti-confound clause — the document must never suggest the mislabel; **the mis-attribution has to be the model's own act.** Rejected drafts are discarded and the rejection rate is reported.

### 3.3 Controlled retrieval and the two surfaces

Retrieval is deterministic assembly, not search: each (pair, cell) maps to an exact document list, with order shuffled by a pair-and-cell-seeded RNG for position hygiene.

| cell | retrieved documents |
|---|---|
| absent × null_control | Y-null doc |
| **absent × completing** | **Y-completing doc** *(the adversarial cell)* |
| complete × null_control | X-doc + Y-null doc |
| complete × completing | X-doc + Y-completing doc |

Two presentation surfaces are measured as a factor:

- **Stark** — prose rendering, one entity-named title per document (`"⟨Name⟩ reference"`), single Y-doc. This is the design pre-committed at M0 and run untouched.
- **Camouflaged** — JSON tool-result rendering with entity identity appearing only inside the content text, **one constant title for every document** (`"API documentation excerpt"`), plus **k=4 off-theme filler documents** drawn from other pairs' X-docs. Filler assignment is seeded on the pair alone, so it is *identical across the two cells* and the cell contrast stays attributable to the Y-doc.

The prompt contract is the same on both: answer only from the retrieved documentation, cite `[docN]` for every fact, and say the documentation does not cover it otherwise.

### 3.4 The four detectors — regex and set membership, no judge anywhere

With `T` = token-shaped strings extracted from the answer, `R` = tokens appearing in ≥1 retrieved document, and X-owned/Y-owned as exact pair-scoped lookups:

1. **DG detector** — `≥1 Y-owned token AND Y's name absent from the answer`.
2. **Confabulation / misattribution split** — `misattributed-other (DG-any) = (T ∩ R) − X-owned − Y-owned`; `confabulation = T − X-owned − Y-owned − R`. The split was mandatory once fillers entered: without it every filler token in an answer would be mislabeled confabulation, breaking the soundness argument by construction. The two sets partition the earlier definition exactly, so nothing falls through the precedence table, and under a no-filler design they collapse back to it — verified, not asserted, by re-scoring all 144 committed M0 rows byte-identically.
3. **Faithfulness proxy** — PASS iff every token-shaped string in the answer appears in *some* retrieved document. **This passes on DG by construction**, which is the whole point.
4. **Citation proxy** — PASS iff the answer carries ≥1 `[docN]`, every cited doc was retrieved, and every token appears in ≥1 **cited** doc. Also passes on DG.

One mutually-exclusive label per trial, by fixed precedence: **DG** → **discriminated** → **misattributed-other** → **confabulation** → **correct-answer** → **correct-refusal** → **vague**.

The `discriminated` rung is deliberately conservative and is the reason every DG rate in this paper is a **floor**: an answer that fills all four evidence slots with Y's tokens but mentions Y's name anywhere — even incidentally, even as an aside — is scored `discriminated`, not DG. Reported DG is what survives that rule.

### 3.5 Statistics and pre-commitment discipline

Every gated quantity is a proportion, so every interval is a Wilson score interval (z = 1.96) per cell, with a Newcombe square-and-add interval on the between-cell difference; a claim whose interval straddles zero is not made. Both are hand-rolled in `stats.py` with no external statistics dependency, and unit-tested.

The discipline around them is the part that matters most to this paper's conclusions:

- **Gates as code, committed before any paid call**, with a full dry-run on synthetic responses and an N≈5 smoke per arm before every paid wave.
- **Under-power auto-reports.** A gate that does not reach its pre-committed clean-N reports UNDERPOWERED with the shortfall stated, rather than rendering a verdict.
- **For M1C specifically: a pre-registration.** N, cells, primary estimand, secondary gate, and the exact reporting language were frozen in `docs/M1C-BRIEF.md` before the build; the verdict script ran **once**, after the full wave; and the brief pre-committed that there would be **no further extension regardless of the outcome**. Per-trial labels are written as each trial runs (the top-up loop needs clean-vs-vague), so the blinding is procedural rather than mechanical: no rate is aggregated before the verdict, and no wave or N decision keys off a DG label.
- **Five reporting templates (T0–T4), fixed verbatim in advance**, selected mechanically by where the Wilson interval falls relative to a reference magnitude. They are the only permitted verbs for describing the relationship to the target paper, and each carries its caveats inline so no downstream rendering can drop them. They are pinned by a test that evaluates the five conditions independently of the function that renders them and requires exactly one to hold, for every reachable k at every planned N.

---

## 4. Experimental setup

**Models.** Three cheap general instruct models on OpenRouter, all at `temperature=0`, `max_tokens=400`, no reasoning: `qwen/qwen-2.5-7b-instruct` (the only roster model with any published anchor), `meta-llama/llama-3.1-8b-instruct`, `google/gemma-3-12b-it`. Two roster substitutions against the kickoff proposal were forced by slug availability and are documented deviations. Generator: `openai/gpt-4o-mini`, fixed and never graded.

**Milestones.**

| | M0 — fit-pilot | M1 — two surfaces | M1C — pre-registered extension |
|---|---|---|---|
| date | 2026-07-15 | 2026-08-03 | 2026-08-04 |
| corpus | 12 pairs | 20 pairs | 80 pairs |
| models | all 3 | all 3 | `qwen-2.5-7b` only |
| design | 4 cells | 2 gated cells × 2 surfaces | 2 gated cells × 2 surfaces |
| trials | 144 | 240 | 240 (new) |
| purpose | grounding precondition + detector fit | DG existence + blindness contrast | power-sized estimate, one look |

**The precondition, and why it is checked first.** A low DG rate is uninformative if the models cannot do RAG at all, or if they are so skeptical they refuse everything. M0 therefore measured *grounding* separately from DG and pre-committed kill/swap triggers: a capability-cliff kill (K1) on failure to ground at a cell where X's own documentation is present, a parseability kill (K2), an API-health kill (K3), and — explicitly **not** a kill — K4, a "robust-low-DG (right reason)" flag for a model that grounds fine yet refuses or discriminates at the adversarial cell. A DG null is only interpretable when K1 has passed.

---

## 5. Results

### 5.1 M0 — the precondition holds, and DG is 0/36

Verdict **FIT**. Detector fidelity **16/16** against a hand-labeled set spanning all label classes and boundary traps; generator rejection **0/36** (every document accepted on the first attempt); **144/144** calls succeeded; zero vague, zero confabulation anywhere.

Grounding passed at ceiling rather than at threshold: **12/12 correct-answer** at both complete-Cx cells for all three models, and **12/12 correct-refusal** at `absent × null_control`. All three models tripped the K4 flag.

**DG at the adversarial cell: 0/36** — every one of the 36 trials was `correct-refusal` (18) or `discriminated` (18). A descriptive texture worth recording: of those 18 discriminated answers, 11 were *loud* (naming both entities and explicitly contrasting them) and 7 were *quiet* — filling all four evidence slots with Y's tokens, with Y's name in the prose the only tell. One llama answer filled every slot with Y's evidence and appended a note that it had "corrected" X's name to Y's "as it seems to be a typo": the completing-evidence pull the target paper describes, minus the concealment.

M0's own outcome addendum, written before M1 ran, predicted that M1 as designed would "very likely render a well-powered NULL." It got the verdict right and the second half wrong, in a way §5.6 makes precise.

### 5.2 M1 — a NULL gate at both surfaces, at N=20

Both arms ran, 240/240 calls ok on the first pass, zero errored, zero vague, zero confabulation, fidelity **288/288** at both verdicts. Total M1 spend **$0.017735** against a $0.45 ceiling.

| model | stark DG | stark Wilson 95% | camouflaged DG | camouflaged Wilson 95% |
|---|---|---|---|---|
| `qwen-2.5-7b-instruct` | 0/20 | [0.0%, 16.1%] | **2/20** | [2.8%, 30.1%] |
| `llama-3.1-8b-instruct` | 0/20 | [0.0%, 16.1%] | 0/20 | [0.0%, 16.1%] |
| `gemma-3-12b-it` | 0/20 | [0.0%, 16.1%] | 0/20 | [0.0%, 16.1%] |
| **arm verdict** | **NULL** | | **NULL** | |

Engagement was present rather than absent — `discriminated` ran 7/20, 8/20 and 15/20 at the stark adversarial cell — so this reproduced M0's K4 pattern at a larger N rather than measuring non-engagement. The paired Newcombe delta for qwen camouflaged was +0.100 [−0.077, +0.301], which straddles zero; the gate read NULL and 2/20 was reported as an existence proof, explicitly not as a rate.

**`DG-any = 0/120`.** Under k=4 filler documents, no model at either cell pulled a single third-party token into an answer. The detector split that made this claim possible never had to separate anything in practice — and was still required, because without it those trials could only have been scored `confabulation` and the claim would have been unavailable to make.

### 5.3 M1C — the primary estimand at the pre-registered N

240 new trials on `qwen-2.5-7b` (60 extension pairs × 2 gated cells × 2 surfaces), pooled with M1's 20 per gated cell per surface. **240/240 calls ok on the first pass** — no top-up needed, zero errored, zero vague, zero confabulation. Fidelity **1068/1068** over the 80-pair corpus. Document generation: 180 attempts, **0 rejections**. Both surfaces hold **80/80 clean** per gated cell, so the pre-committed threshold of 80 was met exactly and neither surface reports UNDERPOWERED. Measured spend **$0.044642 / $0.10**. The original rows re-derive M1's published verdicts exactly, which is the ingestion check the combined estimand depends on.

The primary estimand is the DG-Y rate at `absent × completing`, per surface, with a Wilson 95% interval, reported at all three pre-committed scopes — the original N=20 is never replaced and the extension-only N=60 is never hidden:

| surface | scope | DG-Y | Wilson 95% | template |
|---|---|---|---|---|
| stark | original (N=20) | 0/20 | [0.0%, 16.1%] | T0 |
| stark | extension-only (N=60) | 3/60 | [1.7%, 13.7%] | T2 |
| **stark** | **combined (N=80)** | **3/80** | **[1.3%, 10.5%]** | **T2** |
| camouflaged | original (N=20) | 2/20 | [2.8%, 30.1%] | T3 |
| camouflaged | extension-only (N=60) | 5/60 | [3.6%, 18.1%] | T3 |
| **camouflaged** | **combined (N=80)** | **7/80** | **[4.3%, 17.0%]** | **T3** |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="fig1-primary-estimand-dark.png">
  <img alt="Forest plot of the DG-Y rate at absent × completing with recorded Wilson 95% intervals, at N=20, N=60 and N=80, for the stark and camouflaged surfaces, against a 14% reference line." src="fig1-primary-estimand.png">
</picture>

> **Figure 1.** Primary estimand: DG-Y rate at `absent × completing` on `qwen/qwen-2.5-7b-instruct`, at each of the three pre-committed scopes, one panel per surface. n is printed on every row (0/20, 3/60, 3/80; 2/20, 5/60, 7/80). **The intervals shown are the recorded Wilson 95% intervals** from `data/m1c_verdict.json`, not intervals computed for this figure. The vertical line marks the 14% nearest-published-cell magnitude, which is a **reference magnitude for sizing and wording only** — see §6 for why it is not a null hypothesis about this condition. The right-hand column gives the pre-committed template each row fired.

Extension-only and combined selected the **same** template on each surface, so the pre-registration's side-by-side clause did not fire and the combined statement is carried alone; all three rows are recorded regardless.

**Both surfaces produce DG, and the stark surface is where this bites.** M1 measured 0/20 there and reported a null. At the pre-registered N the same surface, the same corpus construction and the same detectors read 3/80, with a Wilson lower bound of 1.3% — above zero. M1's measurement is not withdrawn: 0/20 was correctly measured and correctly reported, and its row stands unchanged above. What does not survive is the *inference* drawn from it. §5.6 and §5.7 are about why, and they do not agree that N alone is the answer.

### 5.4 The secondary paired gate — a different question, reported separately

The pre-registration also kept M1's original gate structure: a Newcombe interval on the difference between the adversarial cell and its paired control, at combined N.

| surface | Newcombe delta (completing − null_control), combined N | gate |
|---|---|---|
| stark | +0.037 [−0.015, +0.105] — straddles 0 | **NULL** |
| camouflaged | +0.087 [+0.024, +0.170] — excludes 0 | **DG-EFFECT** |

**On the stark arm the primary interval excludes zero while the secondary interval does not, and that is not a defect.** They answer different questions and this paper does not conflate them — the dry-run carried a scenario for exactly this case before any money was spent.

The structural reason is one the project stated against itself before it mattered. At `absent × null_control` the Y-null document contains **zero token-shaped strings**, so DG-Y is impossible there *by construction*; the control cell's job is hygiene, and the paired test is effectively a one-sample test of DG(completing) > 0. The Newcombe interval nevertheless carries the control cell's own Wilson width (0/80 → upper 4.6%) into the difference, and at k=3 that width is larger than the arm cell's distance from zero. The paired test is therefore strictly the more conservative of the two here, and **its stark NULL is not evidence against occurrence**. Both are reported; neither is presented as the other.

### 5.5 The blindness contrast — ten answers, every standard check blind

This is the artifact the project exists to produce. Across both surfaces at combined N there are **ten** DG answers (3 stark, 7 camouflaged). On every single one:

| surface | DG answers | faithfulness proxy PASS | citation proxy PASS |
|---|---|---|---|
| stark | 3 | **3/3** | **3/3** |
| camouflaged | 7 | **7/7** | **7/7** |
| **total** | **10** | **10/10** | **10/10** |

Y's evidence attributed to X, Y never named, a genuinely retrieved document cited. Every standard check passes; only token ownership sees it.

A worked instance, from the stark surface (pair p41, `data/m1ca_wave.jsonl`) — X is the fabricated library **Munivex**, Y is its fabricated sibling **Muneshin**, and only Muneshin's document was retrieved:

> In the Munivex library, the method `xff_rotate_transfer()` enforces per-key quotas across a request fleet [doc1]. The configuration flag `xff.pinned_collar` must be enabled for this feature to work [doc1]. When a key's quota counter cannot be reconciled across nodes, the error code `XFF-E494` is raised [doc1]. This per-key quota enforcement feature was introduced in Munivex version 4.8.19 [doc1].

All four evidence tokens belong to Muneshin. Munivex's own four (`kcp_purge_replica`, `kcp.chained_quota`, `KCP-E312`, `6.20.19`) appear nowhere, because Munivex's documentation was never retrieved. "Muneshin" is never written. `[doc1]` was genuinely retrieved and genuinely contains every token cited. Faithfulness: **PASS**. Citation: **PASS**. Ownership: **DG**.

At M1 this contrast rested on 2 answers and was reported as an existence proof rather than a rate. At M1C it rests on ten, at both surfaces, with an interval attached. The mechanism claim and the rate claim stay separate: the ten answers demonstrate the mechanism; the intervals in §5.3 bound its frequency.

**The contamination guard reads clean: `DG-any = 0/160`.** Across all 160 camouflaged trials not one third-party filler token entered an answer.

### 5.6 The project's finding about itself: an N sized for the wrong thing

M1's pre-committed N≥20 was derived from M0's clean-**trial-yield** funnel — a function that asked "how many pairs are needed for 20 usable trials per cell?" — and never from a power calculation against a target effect size. It sized the wave for usable trials, not for detectable difference.

The consequence is mechanical. At N=20, an observed 0/N has a Wilson upper bound of **16.1%**, and 24 is the smallest N whose 0/N upper bound (13.8%) falls below the 14% reference magnitude. **At the N this study pre-committed, a perfect zero could not have resolved even the reference magnitude from zero.** That is the project's main methodological finding about itself, and it is why the extension was designed rather than the null being written up as it stood.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="fig3-sizing-dark.png">
  <img alt="Bar chart of the Wilson 95% upper bound on an observed 0/N at N = 20, 24, 60, 80 and 120, against a 14% reference line; N=20 is above the line and N=80 is far below it." src="fig3-sizing.png">
</picture>

> **Figure 3.** Pre-registered sizing. The Wilson 95% upper bound on an *observed 0/N*, at the five combined-N values tabulated in the M1C pre-registration, against the same 14% reference magnitude. The two values this project actually ran are emphasised: at N=20 the bound sits **above** the reference line; at N=80 it is 4.6%. Values are the five recorded in `docs/M1C-BRIEF.md` D2 and pinned by `test_m1c_sizing.py`; they are drawn as discrete bars and deliberately **not** connected by a curve, because the repository records those five points and no interpolation between them.

The extension was sized against this table, and the brief records its reasoning as a set of exclusions rather than as a single optimum. **Why not 24**, the bare-exclusion minimum: 0/24 clears the reference magnitude only if the extension observes zero events, and the camouflaged cell already carried 2 — "the interesting deliverable is a **tight estimate**, not a bare exclusion." **Why not 120**: "$0.034 more for template-band shifts that change no verb", plus the corpus-quality risk of 100 new hand-authored themes. **Why 80 rather than the N=60 fallback**: $0.017 that "buys the wider decisive bands in D2's table and headroom against the floor-is-a-floor caveat" — the T2 band spans k=1–3 at N=60 and k=1–5 at N=80. What N=80 does *not* uniquely buy is one-template-per-outcome: that property holds at **every** tabulated N, N=20 included, and `test_m1c_sizing.py` asserts it there too. Because the Wilson lower bound exceeds zero exactly when k ≥ 1, power against the "does DG occur at all" direction is closed-form — 0.9998 at N=80 if the true rate is 10%, 0.9835 if it is 5%.

The extension is an N-extension decided **after** seeing the data, and this paper does not ask anyone to take its innocence on faith. Three guards were fixed in advance: it was argued in a brief approved before any build or spend; N, cells, analysis and reporting language were frozen with a single look at the end; and the original N=20 result is reported alongside forever rather than replaced. What made the decision defensible was that its trigger was the sizing audit above, not the observed rate — and the extension-only rows exist precisely so a reader can check the conditioned analysis against an unconditioned one.

### 5.7 Stage heterogeneity — the principal limitation, and why "N alone" is the wrong story

The two stages that the combined row pools are **not behaviourally exchangeable**, and the difference is large.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="fig2-label-composition-dark.png">
  <img alt="Stacked bars showing the share of clean trials scoring DG, discriminated and correct-refusal at the adversarial cell, per surface and per scope, with the engagement percentage for each stage in the right margin." src="fig2-label-composition.png">
</picture>

> **Figure 2.** Outcome-label composition at `absent × completing`, per surface per scope, as a share of that row's clean trials. Counts are lifted verbatim from `data/m1c_verdict.json`; each share is that count over the row's recorded n (n = 20, 60, 80 respectively). The right margin gives the **recorded** engagement (non-refusal) share for the two *stages*; the combined rows show "—" because pooling the two stages is exactly what this limitation objects to, and no pooled engagement figure is on record.

Engagement — the share of clean trials at the adversarial cell that were *not* a refusal — differs materially between the pairs M1 ran and the pairs the extension added: **stark 35% on p01–p20 against 65% on p21–p80; camouflaged 35% against 55%.** The recorded label counts behind those shares are, at the stark surface, `correct-refusal 13 / discriminated 7` on the original 20 trials against `correct-refusal 21 / discriminated 36 / DG 3` on the extension's 60; at the camouflaged surface, `correct-refusal 13 / discriminated 5 / DG 2` against `correct-refusal 27 / discriminated 28 / DG 5`.

**This is why the reversal in §5.3 must not be attributed to N alone.** The pre-merge review of the extension flagged precisely this: the "power artifact" headline credits N for a change that the engagement shift also drives. The extension's pairs did not merely give the estimator more trials — they gave it materially more trials in which the model engaged with the evidence at all. Both are live, and this study separates neither.

Two independent sources of the difference are on record, and no mechanism is established for either:

1. **The pairs differ** in their hand-authored themes and generated prose. Nothing was held constant across the two stages except the generator, the verifier contract, the assembler and the detectors.
2. **Repeat draws are not stable**, even at `temperature = 0.0` (§8).

A rate conditioned on engagement — DG per *engaged* trial rather than per clean trial — would sharpen this, and the review named it as a nice-to-have. **It is not stated here, because it is not recorded in any committed file in this repository**, and neither is any test of the difference between the two stages. Manufacturing either for the write-up would be exactly the kind of after-the-fact analysis the pre-registration exists to prevent. What is reported is what was recorded: the label counts, the engagement shares, and the fact that both scopes fired the same template on each surface — which is the check that keeps the combined row from hiding the disagreement rather than a defence of pooling.

Nothing was adjusted, weighted, stratified or excluded. The pre-registration fixed the analysis in advance and the extension-only rows exist so the difference is visible rather than averaged away — but the DG rates themselves rest on pairs that elicit more engagement than M1's did, and that is a limitation of the estimate, not a footnote to it.

### 5.8 The surface factor stays descriptive

The camouflaged point rate is the higher of the two (7/80 = 8.8% against 3/80 = 3.8%), which is the direction the name-salience argument predicted. But the intervals overlap, **M1C pre-registered no cross-surface test, and none was performed.** The camouflage levers were bundled by design — JSON rendering, constant titles, k=4 fillers, changed together as one arm — so even a demonstrated difference could not be attributed to any one of them. The per-surface paired gates are not that test either: one interval excluding zero while the other does not is a difference of significance, not a significant difference.

What M1C does establish about the surface question is negative and useful: **camouflage is not required.** The un-camouflaged surface produces DG too.

---

## 6. Relationship to the target paper

This section is deliberately the most constrained in the paper. Three successive framings of it have been published in this project's own record and then withdrawn, each failing in the same way — comparing this project's rate against a paper cell that is not the one it ran:

1. "Paper-contradicting for cheap models" — withdrawn; its premise (that the paper published no per-cell breakdown for non-calibration models) was false. Appendix C publishes complete per-cell matrices for all thirteen.
2. "Prior-dependence, well-powered" — withdrawn; it was sized against the wrong anchor and inherited the "well-powered" claim §5.6 dismantles.
3. "Consistent with the paper at our exact cell" — withdrawn; **the cell is not ours**.

The nearest published cell for our model is `Qwen2.5-7B, absent × prior_completing` = **14%** (Figure 6 / Appendix C, RAG-4 schema; the same row reads null_control 2%, class_proximate 4%, context_adjacent 6%, synthetic_Y 61%). Three verified, structural reasons make a point comparison against it illegitimate — and none of them is statistical, so no amount of N touches any of them:

1. **The condition is off the paper's grid by definition.** §4 and Appendix A define `prior_completing` as evidence elicited to match the baseline model's *parametric prior for X*. Our completing evidence is fabricated tokens matching no prior whatsoever. The paper has **no cell for the condition we ran**.
2. **The number is a stated lower bound.** §5.2 and Appendix C Table 8 state that absolute DG rates at completing-Cy conditions are lower bounds for non-L1 models, because the stimuli are calibrated to the calibration model's prior. So 14% is a floor, not a value.
3. **Schema mismatch, in both directions.** Figure 6 is RAG-4; Tables 1–2 are 10-tool; **this project ran neither.** The paper claims DG changes by under 2 pp across schemas at completing-Cy conditions, yet its own calibration model reads 34% (Figure 6) against 67.0% (Table 1) at the same cell — a ~2× discrepancy at the exact point of comparison.

Accordingly, the relationship is stated **only** through the pre-committed templates, which are the only permitted verbs and carry their caveats inline by construction. Verbatim, as rendered by the verdict script:

> **Stark (T2).** "DG occurs on this surface (3/80, Wilson [1.3%, 10.5%], lower bound > 0) at a rate below the nearest published floor for this model (≥14% — different condition by definition, stated lower bound, schema we did not run). Direction: occurs, low. This is not a replication claim and not a contradiction claim."

> **Camouflaged (T3).** "DG occurs on this surface (7/80, Wilson [4.3%, 17.0%]) at a rate whose interval reaches the magnitude of the nearest published floor (≥14% — different condition by definition, stated lower bound, schema we did not run). Direction: comparable magnitude, hedged. This is not a replication claim and not a contradiction claim."

For completeness, the original N=20 stark row fired T0, whose recorded language is its own verdict on M1: *"Zero DG observed on this surface (0/20, Wilson [0%, 16.1%]) — an interval that reaches the floor's magnitude, so this row alone is uninformative against it (the D18 gap). Direction: at or below, hedged. This is not a replication claim and not a contradiction claim."* ("The D18 gap" is this project's ledger name for the sizing finding of §5.6, and it was written into the template before the extension ran.)

**No p-value is attached to any comparison with the paper, and no point comparison is made.** What the extension bought is a tighter interval on *our own* rate, and therefore a sharper directional template — nothing more.

One cross-study observation is offered as an explicitly-labelled **inference, not a headline and not a comparison of rates**. The paper's `synthetic_Y` cell fabricates Y's *name* while holding the completing information constant, and the paper attributes the resulting increase to information content rather than to entity-label recognition: *"The model attributes evidence based on information content, not Y's entity-label recognition."* Our design sits **level with `synthetic_Y` on the name axis** (every name here is fabricated) and **off every paper cell on the evidence axis** (the evidence is fabricated too, so there is no prior to complete). If entity-label recognition alone drove the effect, a design that removes recognition entirely would be expected to sit in the paper's high regime; ours does not. That points the same way as the paper's own explanation. It is a *structural* observation about which axis our design occupies — not a statement that our rate agrees or disagrees with any published rate, which §6 has just finished establishing is not a legitimate thing to say. It compares across different domains, corpora, detectors and schemas, and no amount of N makes those commensurable. It is a reading, not a measurement.

---

## 7. Discussion

**The mechanism is real, demonstrable, and cheap to catch — if you have ownership.** Ten answers — eight from the extension, two (camouflaged p14 and p18) carried from M1's own wave — in which the model filled every evidence slot of a question about X with Y's tokens, cited a genuinely retrieved document, and never mentioned Y. Faithfulness and citation proxies passed all ten. That is the paper's blindness claim, reproduced with a stronger instrument than the original: not a judge's assessment that attribution went wrong, but an exact set-membership fact.

**The rate is low here, and that is a claim about this condition, not about the phenomenon.** Both intervals are single-digit to mid-teens percent. The condition is unusually hostile to the failure: names are fabricated so nothing is recognizable, evidence is fabricated so no prior can be completed, and the conservative `discriminated` rule sends every answer that so much as names Y out of the DG count. Reported DG is a floor by construction, twice over.

**The most instructive result is the reversal.** M0 read 0/36 and M1 read 0/20 on the stark surface, and the project concluded that capable models were choosing not to deceive. The measurements were sound. The conclusion was not licensed by the N, and the project's own sizing audit said so *before* the extension ran. When the extension ran, the same surface with the same construction produced DG at [1.3%, 10.5%]. "DG ≈ 0 on this surface" turned out to be a statement about N, not about the surface — and, per §5.7, partly a statement about which pairs were in the sample.

That is the generalizable lesson, and it is uncomfortable in a useful way: **a null needs its own power argument, and "we hit our pre-committed N" is not one if the N was sized for a different quantity.** A clean-trial-yield funnel answers "how many trials will survive?" — a perfectly good question — and says nothing about "what effect could this detect?" The two were conflated here, in a project whose explicit contract is that nulls are headlines. The failure mode is not exotic; it is what happens when the sizing step is competent at the wrong question.

**What the nulls that survived still mean.** Three are load-bearing and none is buried. `DG-any = 0/160` says the models did not grab indiscriminately: under four filler documents, not one third-party token entered an answer, so what is measured is specifically the on-theme completing pull. The stark paired gate is NULL, and §5.4 explains why that is a conservative instrument disagreeing with a less conservative one rather than a contradiction. And `llama-3.1-8b-instruct` and `gemma-3-12b-it` remain at 0/20 with a 16.1% Wilson upper — which, after §5.6, must be read as **untested at N=80, not shown clean**. Their nulls are exactly the kind this paper has just finished dismantling.

**The un-validatable residual.** Whether what we measured is *the same phenomenon* the target paper measures at its `prior_completing` cell cannot be settled from inside this design. Judge-free detection requires fabricated evidence; the paper's completing axis requires evidence the model already believes; those are mutually exclusive, and the exclusion is structural rather than a budget problem. Every comparison in §6 is directional for that reason and stays directional however much data is collected. A reproduction can be honest about a gap it cannot close; it cannot close it by writing more carefully.

---

## 8. Threats to validity and limitations

- **Stage heterogeneity (§5.7) is the principal limitation.** Engagement at the adversarial cell runs 35% on M1's pairs against 55–65% on the extension's; the stages are not exchangeable and the combined row pools them. Reported, not adjusted for. The reversal in §5.3 is **not** attributable to N alone.
- **Repeat draws are not stable at `temperature = 0.0`, and provider routing is unpinned.** The extension committed 10 duplicate trials of byte-identical prompts (smoke and wave both ran `absent × completing` on p21–p25): **3 differ in answer text, 2 change label**, and 2 report different `prompt_tokens` for the same prompt — which prompt construction cannot produce, so those calls reached different backends. The same condition is visible in M1's data (30 duplicates: 8 text differences, 2 label flips), so it is pre-existing rather than introduced. Three consequences, stated rather than smoothed over: the pre-registration's premise that re-sampling the same pairs could yield nothing new is **false**, and re-sampling would have avoided the heterogeneity above; repeat-draw noise is a second live source of stage-to-stage variation; and **no committed rate in this repository is exactly reproducible by re-running its wave.** Pinning provider routing is the durable fix, is a design change, and belongs to a future pre-registration rather than a retrofit into a frozen one.
- **One model at power.** Only `qwen-2.5-7b` was extended — the sole roster model with any published anchor. Nothing here transfers to the other two, which stay at 0/20 with an uninformative 16.1% upper bound.
- **Bundled camouflage levers and no cross-surface test.** JSON rendering, constant titles and k=4 fillers moved together; the surfaces' intervals overlap; no test was pre-registered and none was run.
- **The constant-title tell**, stated before the run rather than discovered after: five byte-identical titles at a five-document cell are themselves a synthetic-benchmark signal that may reinforce refusal, so a camouflaged null could not have been distinguished from the stark one on that axis.
- **The filler population changed between stages**, as the pre-registration stated in advance: extension trials draw fillers from 80 pairs, the original camouflaged trials drew from 20. The original trials were never re-assembled.
- **DG-Y is impossible by construction at `absent × null_control`**, so the paired Newcombe delta is effectively a one-sample test (§5.4).
- **The queried entity is fabricated**, which the target paper never varies — its X is always a real drug. This is the deepest design difference and the source of the §6 residual.
- **A conservative label rule** makes every reported DG rate a floor: any mention of Y's name, however incidental, scores `discriminated` instead.
- **The corpus is small and self-authored**, one domain (API/library documentation), one question template, one generator. Nothing here speaks to real retrieval, real corpora, or production traffic.
- **A frozen-record hazard, found by review and fixed.** Growing the shared corpus re-scoped a constant the earlier milestones' scripts read, so leaving their bytes untouched is exactly what would have changed their behaviour — one script would have run 480 trials instead of 120, and the verdict writers would have rewritten published records with fidelity counts from a corpus those milestones never ran on. The scripts are now pinned to their own N and every verdict writer refuses to run once the shared pool has moved. Frozen means the recorded behaviour is preserved, not that the bytes are inviolable while the behaviour drifts.

---

## 9. Reproducibility

**Everything except the model calls runs offline and free.** The corpus is regenerated deterministically from `SEED = 20260715`; the detectors, assembler and statistics are pure functions with unit tests and no network; the fidelity gate and both dry-runs execute against hand-labeled and synthetic answers with no API key present.

```bash
uv sync
uv run pytest                              # all pure-logic tests, no network
uv run python m1c.py fidelity              # the detector fidelity gate
```

Reproducing the measurement requires an `OPENROUTER_API_KEY` in `.env` and re-running the waves — subject to the §8 caveat that repeat draws are not stable, so a re-run will not reproduce a committed rate exactly. The verdict scripts additionally **refuse to run** once the shared corpus pool has moved, so a published record cannot be silently rewritten.

**Recorded costs.** M0 ≈$0.009 (cap $0.60); M1 $0.017735 (cap $0.45); M1C $0.044642 (cap $0.10, itemized: gen-docs $0.023814, smoke $0.000233 + $0.000615, waves $0.005088 + $0.014892). Project total ≈**$0.072** against a <$5 target. Every wave ran under a hard ceiling on *measured* spend, checked before each call.

**The figures in this paper** are rendered by a committed, deterministic, headless script:

```bash
uv run docs/paper/derived_contrasts.py             # asserts, then writes derived_contrasts.json
uv run --with matplotlib docs/paper/figures.py     # renders the six PNGs
```

`derived_contrasts.py` re-derives — through the repository's own `stats.py` — every Wilson interval and both Newcombe deltas the paper quotes, plus the two statistics that exist in this repository only as prose (the per-stage engagement shares of §5.7 and the sizing table of §5.6), and **asserts each equals the recorded value before writing anything**. It writes nothing at all if any assertion fails. `figures.py` computes exactly one thing — a rate as a recorded numerator over a recorded denominator — and prints every plotted number to stdout so the figures can be checked against the tables above without opening a PNG. Neither script performs smoothing, interpolation, fitting, pooling the repository did not perform, or any test.

**Primary record.** `data/m1c_verdict.json` (M1C, rendered once), `data/m1a_verdict.json` / `data/m1b_verdict.json` / `data/m1_surface_contrast.json` (M1), `data/m0_verdict.json` (M0), the per-trial wave logs `data/m1c{a,b}_wave.jsonl` / `data/m1{a,b}_wave.jsonl` / `data/pilot.jsonl`, the spend ledgers, and the generation logs. Design and pre-commitments: `docs/KICKOFF.md`, `docs/M0-BRIEF.md`, `docs/M1-BRIEF.md`, `docs/M1C-BRIEF.md`. Decision ledger: `Decisions.md` (D1–D27).

---

## 10. References

**[1]** Caruzzo, Yoo, and Kim. arXiv **2607.09349**, v1, 2026-07-10. Sections and appendices cited above: §3 (the DG definition), §4 and Appendix A (Cy definitions and the `synthetic_Y` / `prior_completing` construction), §5.2 (the lower-bound statement), §5.3 and Table 11 (the label-substitution experiment), Table 1 (calibration-model per-cell rates), Table 2 (cross-model peak rates), and Appendix C with Figure 6 (per-cell matrices for all 13 models, RAG-4 schema). Re-checked 2026-08-03 and 2026-08-04: still v1, **no code released**.

*Citation note, per this project's honesty contract: this repository records the target paper's arXiv identifier, author surnames, version and date, and the sections it read — but it does not record the paper's title. It is cited here exactly as recorded, and no title has been supplied.*

**[2]** This project's own prior milestones and their pre-commitments are cited throughout by their in-repository paths rather than as external works. No other external source is used, and no result in this paper depends on one.

---

*All statistics in this paper are lifted from committed files in this repository or, where the source is prose, re-derived through the repository's own statistics module and asserted equal to the recorded value before use. No measurement was taken for this write-up; no model was called. Where a quantity is not recorded — a DG rate conditioned on engagement, any test between the two stages, any test between the two surfaces, any p-value against a cell of [1] — this paper says so and does not supply one.*
