> **Plain-English rewrite.**
> **Paper:** *Deceptive grounding is measurable without a judge — and a null at N=20 did not survive a pre-registered extension to N=80*
> **Source project:** blind-cite (reproduction #5 in the forge-gap → decay-pin → lossy-wall → ghost-patch lineage)
> **Source file:** [`docs/paper/blind-cite-paper.md`](../paper/blind-cite-paper.md)
> **Generated:** 2026-08-04
>
> This mirrors the original 1:1 — same headings, same paragraph order, nothing merged, dropped, added, or reordered. Only the wording changes: field jargon is translated on first use and then used consistently. Tables are carried verbatim and each is followed by an *"In plain words"* line; the three figures keep their original images with rewritten captions; the references section is carried untouched. The original contains **no display equations**, so there are no named-form blocks. Four passages are reproduced **verbatim and are deliberately not rewritten**, because the original project fixed their wording in advance and re-phrasing them would break that commitment: the two reporting-template statements in §6, the template quotation in the paragraph after them, and the sample model answer in §5.5.

---

# Deceptive grounding is measurable without a judge — and a null at N=20 did not survive a pre-registered extension to N=80

**A reproduction of one-entity-answered-with-another-entity's-evidence in look-it-up-then-answer systems, done on cheap models, with no model acting as grader, under rules committed to in advance**

*blind-cite · reproduction #5 in the forge-gap → decay-pin → lossy-wall → ghost-patch lineage · measurement phase closed 2026-08-04*

---

## Abstract

Deceptive grounding (DG) is a failure of look-it-up-then-answer systems (**retrieval-augmented generation**, or RAG): an answer that is supposed to be about a queried thing X instead takes a *different* thing Y's evidence and presents it as X's — while every statement in it genuinely does appear in the documents that were fetched, which is exactly why the standard automated checks for made-up content and for correct citing cannot see it. The failure is described in arXiv 2607.09349 (Caruzzo, Yoo, Kim), which detects it by having another language model act as a grader, and which ships no code. We reproduce and measure one narrow slice of it on three cheap open-weight models, and we replace that grader with exact ground-truth ownership of identifying strings over a **made-up** collection of documents about invented sibling libraries whose evidence strings are unique across the whole collection — so "which thing does this evidence belong to?" is a string-matching fact rather than a model's opinion. A first fit-check run (M0) established that the models really do base their answers on the fetched documents, at the maximum possible rate (12 out of 12 per model in every condition where grounding was possible), and measured DG at **0 out of 36** in the hostile condition. A run with the rules fixed in advance, at N=20 per gated condition per model (M1), returned a no-effect (NULL) verdict at two different ways of presenting the documents, with DG at 0/20 everywhere except `qwen-2.5-7b` in the camouflaged presentation (2/20). We then put on record that this N had been derived from how many *clean trials* the run would yield, and never from a calculation of what size of effect the run could detect — and we ran a written-down-in-advance extension (M1C), this time sized to be able to detect something, out to a combined **N=80** per gated condition per presentation on `qwen-2.5-7b`, analysed exactly once, with the reporting wording frozen beforehand. DG happens at **both** presentations: stark **3/80, Wilson 95% range [1.3%, 10.5%]**; camouflaged **7/80, [4.3%, 17.0%]**. The stark presentation, the one measured at 0/20, now has a lower end above zero — the measurement stands, the conclusion "DG ≈ 0" does not. On all **ten** DG answers, the mechanical does-the-documents-back-it check and the did-it-cite-properly check **both PASS (10/10 and 10/10)**. Total measured spend: about $0.072.

---

> **The framing, stated up front.** This is a reproduction, not a discovery. The failure itself, its name, the grid of conditions used to study it, and the reason anyone cares all belong to the original paper; what belongs to us is a way of detecting it that needs no model-grader, a measurement done at hobby scale on cheap models, and an honest account of what such a measurement can and cannot support. The document collection is **made up from end to end** — both the things being asked about and every piece of evidence about them — and the hostile condition is **built deliberately**, by withholding the queried thing's own documentation. Both facts do real work in the argument, and both are restated anywhere a result depends on them. Every number below is taken from a file committed in this repository; where a number was never recorded, the paper says so instead of estimating it.

---

## 1. Introduction

A look-it-up-then-answer system can fail in a way its own testing setup is structurally unable to notice. Ask about library X; fetch a document about library Y; get back a fluent, confident answer that fills every slot of the question about X with Y's method names, Y's config flags, Y's error codes, Y's version number — and that cites the document it all came from. A does-the-documents-back-it check (a **faithfulness** check) asks "is every claim supported by a fetched document?" and gets *yes*. A citation check asks "does the cited document exist, and does it contain these strings?" and gets *yes*. The one question neither of them asks is **whose evidence this is**.

The original paper names this deceptive grounding and reports it across thirteen models. It detects DG using a language model as grader (Kimi-K2.5, reported at 97.0% precision and 98.7% recall against a set of human-labelled examples), and it releases no code. Both of those facts shaped this reproduction. A model-as-grader is precisely the instrument that this project lineage's honesty rules forbid, and because no code exists, an independent implementation is the only implementation there can be.

The move that makes the detector purely mechanical is to give up realism in one specific place. If the document collection is **made up** — sibling libraries that do not exist, each owning four globally unique, identifier-shaped strings that appear nowhere else — then a string in an answer can only have got there by being copied out of a fetched document, and "whose evidence is this?" collapses into an exact set-membership lookup. Working out who evidence belongs to stops being a judgement call. On the narrow question it answers, that is a *stronger* instrument than the original paper's, and §6 is explicit about the price: making up the evidence moves our experimental condition off the original paper's grid of conditions entirely, and no amount of extra data brings it back.

The contribution is narrow, and is stated as such:

1. **A DG detector that needs no model-grader**, plus the document-collection construction that makes it sound, with per-trial mechanical checking that the manipulation actually happened.
2. **A measured rate with a range around it**, on one model at two ways of presenting documents, from a run whose design was registered in advance and sized to be able to detect something: stark 3/80 [1.3%, 10.5%], camouflaged 7/80 [4.3%, 17.0%].
3. **The blindness contrast turned into a concrete artifact** — ten answers on which both standard checks pass and only evidence-ownership catches the failure.
4. **A methodological finding about the project itself**: its own committed-in-advance N had been sized for how many clean trials it would produce rather than for what it could detect, and the no-effect result it produced did not survive the pre-registered extension that this audit prompted. This paper reports that reversal against itself in the same detail as the positive result — including the reason, in §5.7, that the number of trials is not the only thing that changed between the two stages, so the reversal is not put down to the number of trials alone.

---

## 2. Background: the claim, and which part of it we reproduce

### 2.1 The target claim

arXiv 2607.09349 (Caruzzo, Yoo, Kim), version 1, dated 2026-07-10, defines a response as showing deceptive grounding when (1) it contains claims that in the fetched documents belong to some other thing Y, not the queried X, (2) those claims are presented as evidence about X, and (3) every factual claim is supported by the fetched documents — which is what makes it invisible to standard does-the-documents-back-it checks. That three-part definition, written down almost word for word in this project's M0 brief before any measurement was taken, is the definition our detector implements.

The original paper's grid of conditions crosses Cx (how much of the queried thing's own evidence is available) ∈ {absent, partial, complete} with Cy (what document about the alternate thing is present) ∈ {null_control, class_proximate, context_adjacent, prior_completing, synthetic_Y}. We reproduce a cut-down 2×2 version: **Cx ∈ {absent, complete} × Cy ∈ {null_control, completing}**. The hostile condition — the only one where DG is even possible, by construction — is `absent × completing`: the queried thing's documentation is withheld, and the one on-topic document available answers the question's exact shape *for the other thing, labelled as the other thing's*.

### 2.2 What we deliberately do not reproduce

No model acting as grader, at any point in scoring. No tool-calling machinery matching the original paper's exact formats. No frontier or medical models, no production-scale measurement, no learned retriever. The original paper's harness was never available to import, and would have been reference-only if it had been.

One dropped arm is worth a note, because it was proposed, approved, and then retired *before any code was written or any money spent*: a `synthetic_Y` positive control. That condition in the original paper makes up Y's **name** while keeping the completing information unchanged, and the paper puts the resulting effect down to the information half rather than the name half. Our collection already makes up every name; it cannot hold "information that matches an existing belief about X" fixed, because there are no existing beliefs for it to match. The arm is degenerate for this collection — not, as this project's decision log first recorded, redundant because we "already perform the manipulation." The reasoning was corrected in place.

---

## 3. Method

### 3.1 The fabricated corpus (manufactured, and labeled as such)

`corpus.py` generates the document collection reproducibly from `SEED = 20260715`. Each pair is two sibling made-up libraries — X (the one asked about) and Y (the alternate) — sharing one task theme, each owning exactly four identifier strings, one per category:

| category | shape (word-boundaried regex) | example |
|---|---|---|
| method | `[a-z]{3}_[a-z]{3,10}_[a-z]{3,10}` (optional trailing `()`) | `xff_rotate_transfer` |
| flag | `[a-z]{3}\.[a-z]{3,10}_[a-z]{3,10}` | `xff.pinned_collar` |
| error | `[A-Z]{3}-E[0-9]{3}` | `XFF-E494` |
| version | `[0-9]+\.[0-9]+\.[0-9]+` | `4.8.19` |

*In plain words: every library owns exactly four made-up strings — a method name, a config flag, an error code, and a version number — and each one is built to a fixed pattern so a simple pattern-match can find them in an answer.*

Generation enforces, and unit-tests, the properties the detector depends on: every string unique across the whole collection, no string contained inside another, no library name contained inside another, and word stems unique per library. Because the names and stems are invented, **no string can get into an answer except by being copied out of a fetched document** — which is the single assumption underneath all four detectors.

Each pair carries one question that demands exactly those four categories: *"In the ⟨X⟩ library, which method ⟨does task⟩, which config flag enables it, which error code signals ⟨failure⟩, and which version introduced it?"* Y's completing document answers that same shape **for Y, labelled as Y's**.

The collection grew twice, and both times the growth **preserved the random seed and only appended** (only the pools of themes and name prefixes were extended, and because `build_corpus` draws from the random number generator in pair order, earlier pairs come out bit-for-bit identical): 12 pairs at M0, 20 at M1, 80 at M1C. Each growth first pinned the earlier pairs as committed reference files and asserted they were byte-for-byte unchanged before writing anything.

### 3.2 Document generation and mechanical verification

Documents are drafted by a fixed model that is never on the roster being tested and is never graded (`openai/gpt-4o-mini`), and are accepted only if they pass a pure string-matching checker:

| document | verifier contract |
|---|---|
| X-doc | all 4 X tokens ≥1×, X name ≥2×, zero Y tokens, zero Y name, **no other token-shaped strings** |
| Y-completing | all 4 Y tokens ≥1×, Y name ≥2×, zero X tokens, **zero X name anywhere**, no other token-shaped strings |
| Y-null | Y name ≥2×, **zero token-shaped strings of any kind**, zero X name |

*In plain words: X's own document must contain all four of X's strings and X's name at least twice, and not a trace of Y. Y's completing document is the mirror image, and must never mention X's name at all. Y's null document mentions Y but contains no identifier-shaped strings whatsoever. Any document containing a stray identifier that isn't one of the four owned ones is rejected.*

"No other token-shaped strings" carries real weight: a single stray identifier in a document would corrupt both the made-up-content detector and the does-the-documents-back-it check. "Zero X name anywhere" in Y's document is the clause that rules out an alternative explanation — the document must never itself suggest the mislabelling; **the mis-attribution has to be something the model does on its own.** Rejected drafts are thrown away and the rejection rate is reported.

### 3.3 Controlled retrieval and the two surfaces

Retrieval here is deterministic assembly, not search: each (pair, condition) maps to an exact list of documents, with the order shuffled by a random number generator seeded on the pair and condition, so document position cannot skew things.

| cell | retrieved documents |
|---|---|
| absent × null_control | Y-null doc |
| **absent × completing** | **Y-completing doc** *(the adversarial cell)* |
| complete × null_control | X-doc + Y-null doc |
| complete × completing | X-doc + Y-completing doc |

*In plain words: in the two "absent" conditions X's own documentation is withheld, so only a Y document is available — and in the hostile one that Y document is built to answer the question's shape. In the two "complete" conditions X's own documentation is there too, so a correct answer is available.*

Two ways of presenting the documents are measured as a factor in their own right:

- **Stark** — plain prose, with one title naming the thing for each document (`"⟨Name⟩ reference"`), and a single Y document. This is the design committed to at M0 and run without changes.
- **Camouflaged** — a JSON tool-result rendering in which the thing's identity appears only inside the body text, with **one and the same title on every document** (`"API documentation excerpt"`), plus **four off-topic filler documents** taken from other pairs' X documents. Which fillers a trial gets is seeded on the pair alone, so it is *identical across the two conditions* and any difference between conditions stays attributable to the Y document.

The prompt is the same contract on both: answer only from the supplied documentation, cite `[docN]` for every fact, and say the documentation does not cover it otherwise.

### 3.4 The four detectors — regex and set membership, no judge anywhere

Write $T$ for the identifier-shaped strings pulled out of the answer, $R$ for the strings that appear in at least one fetched document, and *X-owned* / *Y-owned* for exact lookups scoped to that pair:

1. **DG detector** — `≥1 Y-owned token AND Y's name absent from the answer`. That is: the answer uses at least one string that belongs to Y, and never names Y.
2. **Confabulation / misattribution split** — $\text{misattributed-other (DG-any)} = (T \cap R) - \text{X-owned} - \text{Y-owned}$, meaning strings that did come from some fetched document but belong to neither X nor Y; and $\text{confabulation} = T - \text{X-owned} - \text{Y-owned} - R$, meaning strings that belong to neither and came from no fetched document at all. The split became mandatory the moment filler documents entered the design: without it, every filler string appearing in an answer would have been labelled as made-up content, breaking the soundness argument by construction. The two sets divide the earlier definition up exactly, so nothing slips through the precedence table, and in a design with no fillers they collapse back into it — which was verified rather than asserted, by re-scoring all 144 committed M0 rows and getting byte-identical results.
3. **Faithfulness proxy** (the does-the-documents-back-it check) — PASS if and only if every identifier-shaped string in the answer appears in *some* fetched document. **This passes on DG by construction**, which is the entire point.
4. **Citation proxy** — PASS if and only if the answer carries at least one `[docN]` marker, every cited document was actually fetched, and every string appears in at least one **cited** document. This also passes on DG.

Each trial gets exactly one label, chosen by a fixed order of precedence: **DG** → **discriminated** → **misattributed-other** → **confabulation** → **correct-answer** → **correct-refusal** → **vague**.

The `discriminated` rung is deliberately strict, and it is why every DG rate in this paper is a **floor**: an answer that fills all four evidence slots with Y's strings but mentions Y's name anywhere — even in passing, even as an aside — is scored `discriminated`, not DG. Reported DG is only what gets through that rule.

### 3.5 Statistics and pre-commitment discipline

Every quantity a gate is checked against is a proportion, so every range is a Wilson score interval (z = 1.96) for a single condition, with a Newcombe square-and-add interval for the difference between two conditions; a claim whose range straddles zero is not made. Both are written by hand in `stats.py` with no external statistics library, and unit-tested.

The discipline surrounding them matters most to this paper's conclusions:

- **Gates written as code and committed before any paid call was made**, with a full dry run against synthetic responses and a roughly-5-trial smoke test per arm before every paid wave.
- **Being under-powered reports itself.** A gate that fails to reach its committed-in-advance number of clean trials reports UNDERPOWERED, and states the shortfall, rather than returning a verdict.
- **For M1C specifically: a pre-registration.** The number of trials, the conditions, the primary quantity being estimated, the secondary gate, and the exact reporting wording were all frozen in `docs/M1C-BRIEF.md` before anything was built; the verdict script was run **once**, after the whole wave; and the brief committed in advance that there would be **no further extension whatever the result turned out to be**. Per-trial labels are written as each trial runs, because the top-up loop needs to know clean-versus-vague, so the blinding is a matter of procedure rather than mechanism: no rate is added up before the verdict, and no decision about a wave or about N keys off a DG label.
- **Five reporting templates (T0–T4), fixed word for word in advance**, and selected mechanically by where the Wilson range falls relative to a reference magnitude. They are the only permitted way of describing the relationship to the original paper, and each carries its caveats inside its own text so no later rendering can drop them. They are pinned by a test that evaluates the five conditions independently of the function that renders them, and requires exactly one to hold, for every reachable count at every planned N.

---

## 4. Experimental setup

**Models.** Three cheap general-purpose instruction-following models on OpenRouter, all at `temperature=0`, `max_tokens=400`, no reasoning mode: `qwen/qwen-2.5-7b-instruct` (the only model on the roster with any published number to point at), `meta-llama/llama-3.1-8b-instruct`, and `google/gemma-3-12b-it`. Two swaps against the roster proposed in the kickoff were forced by which model identifiers were actually available, and are recorded as deviations. Document generator: `openai/gpt-4o-mini`, fixed, and never graded.

**Milestones.**

| | M0 — fit-pilot | M1 — two surfaces | M1C — pre-registered extension |
|---|---|---|---|
| date | 2026-07-15 | 2026-08-03 | 2026-08-04 |
| corpus | 12 pairs | 20 pairs | 80 pairs |
| models | all 3 | all 3 | `qwen-2.5-7b` only |
| design | 4 cells | 2 gated cells × 2 surfaces | 2 gated cells × 2 surfaces |
| trials | 144 | 240 | 240 (new) |
| purpose | grounding precondition + detector fit | DG existence + blindness contrast | power-sized estimate, one look |

*In plain words: three stages, each on a larger collection of documents than the last. The first checked that the whole setup works at all; the second looked for DG across all three models at two presentations; the third went back to the single model with a published reference point and ran a version sized to be able to detect something, looking at the result only once.*

**The precondition, and why it is checked first.** A low DG rate tells you nothing if the models cannot do look-it-up-then-answer at all, or if they are so suspicious that they refuse everything. M0 therefore measured *grounding* separately from DG, and committed in advance to triggers for killing or swapping a model: a can't-do-the-task kill (K1) if a model fails to ground even when X's own documentation is present, an unparseable-output kill (K2), an API-health kill (K3), and — explicitly **not** a kill — K4, a "robust-low-DG (right reason)" flag — a low DG rate arrived at for the right reason — for a model that grounds perfectly well and yet refuses or calls out the mismatch in the hostile condition. A DG result of zero only means anything once K1 has passed.

---

## 5. Results

### 5.1 M0 — the precondition holds, and DG is 0/36

Verdict **FIT**. Detector accuracy against a hand-labelled set covering every label class and the tricky boundary cases: **16/16**. Generator rejections: **0/36** — every document was accepted on the first try. **144/144** calls succeeded. Zero vague answers and zero made-up content anywhere.

Grounding did not merely clear the bar, it maxed out: **12/12 correct answers** in both conditions where X's own documentation was present, for all three models, and **12/12 correct refusals** at `absent × null_control`. All three models tripped the K4 flag.

**DG in the hostile condition: 0/36** — every single one of those 36 trials was either a `correct-refusal` (18) or `discriminated` (18). One texture worth recording: of those 18 discriminated answers, 11 were *loud* (naming both libraries and explicitly contrasting them) and 7 were *quiet* — filling all four evidence slots with Y's strings, with Y's name somewhere in the prose being the only giveaway. One llama answer filled every slot with Y's evidence and then added a note saying it had "corrected" X's name to Y's "as it seems to be a typo": the pull toward completing evidence that the original paper describes, minus the concealment.

M0's own write-up, produced before M1 ran, predicted that M1 as designed would "very likely render a well-powered NULL." It got the verdict right and the second half wrong, in a way §5.6 makes precise.

### 5.2 M1 — a NULL gate at both surfaces, at N=20

Both arms ran: 240/240 calls succeeded on the first pass, none errored, none vague, no made-up content, and detector accuracy was **288/288** across both verdicts. Total M1 spend was **$0.017735** against a $0.45 ceiling.

| model | stark DG | stark Wilson 95% | camouflaged DG | camouflaged Wilson 95% |
|---|---|---|---|---|
| `qwen-2.5-7b-instruct` | 0/20 | [0.0%, 16.1%] | **2/20** | [2.8%, 30.1%] |
| `llama-3.1-8b-instruct` | 0/20 | [0.0%, 16.1%] | 0/20 | [0.0%, 16.1%] |
| `gemma-3-12b-it` | 0/20 | [0.0%, 16.1%] | 0/20 | [0.0%, 16.1%] |
| **arm verdict** | **NULL** | | **NULL** | |

*In plain words: at 20 trials each, only one model produced any DG at all, and only in the camouflaged presentation — two answers out of twenty. Every other box was a flat zero, and the ranges around those zeros run up to 16.1%, so they do not rule much out. Both arms were scored as no-effect.*

Engagement was there rather than absent — `discriminated` came in at 7/20, 8/20 and 15/20 in the hostile condition on the stark presentation — so this was reproducing M0's K4 pattern at a larger number of trials, not measuring models that simply refused to play. The paired Newcombe difference for qwen camouflaged was +0.100 [−0.077, +0.301], which straddles zero; the gate read NULL, and 2/20 was reported as proof the thing can happen, explicitly not as a rate.

**`DG-any = 0/120`.** With four filler documents in play, no model in either condition pulled a single third-party string into an answer. The detector split that made this claim sayable never actually had to separate anything in practice — and was still necessary, because without it those trials could only have been scored as made-up content, and the claim would not have been available to make.

### 5.3 M1C — the primary estimand at the pre-registered N

240 new trials on `qwen-2.5-7b` (60 extension pairs × 2 gated conditions × 2 presentations), pooled with M1's 20 per gated condition per presentation. **240/240 calls succeeded on the first pass** — no top-up needed, none errored, none vague, no made-up content. Detector accuracy **1068/1068** over the 80-pair collection. Document generation: 180 attempts, **0 rejections**. Both presentations hold **80/80 clean** trials per gated condition, so the committed-in-advance threshold of 80 was met exactly and neither presentation reports UNDERPOWERED. Measured spend **$0.044642 / $0.10**. The original rows re-derive M1's published verdicts exactly, which is the ingestion check the combined estimate depends on.

The primary quantity being estimated is the DG-Y rate in the `absent × completing` condition, per presentation, with a Wilson 95% range, reported at all three committed-in-advance scopes — the original 20 trials are never replaced and the extension-only 60 are never hidden:

| surface | scope | DG-Y | Wilson 95% | template |
|---|---|---|---|---|
| stark | original (N=20) | 0/20 | [0.0%, 16.1%] | T0 |
| stark | extension-only (N=60) | 3/60 | [1.7%, 13.7%] | T2 |
| **stark** | **combined (N=80)** | **3/80** | **[1.3%, 10.5%]** | **T2** |
| camouflaged | original (N=20) | 2/20 | [2.8%, 30.1%] | T3 |
| camouflaged | extension-only (N=60) | 5/60 | [3.6%, 18.1%] | T3 |
| **camouflaged** | **combined (N=80)** | **7/80** | **[4.3%, 17.0%]** | **T3** |

*In plain words: the same measurement shown three ways for each presentation — the original small run on its own, the new trials on their own, and everything pooled. On the stark presentation the original run saw nothing and the new trials saw three; pooled, that is 3 out of 80, with a range whose bottom sits above zero. On the camouflaged presentation it is 7 out of 80. The last column names which of the five pre-written statements each row triggers.*

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../paper/fig1-primary-estimand-dark.png">
  <img alt="Forest plot of the DG-Y rate in the absent × completing condition, showing the recorded Wilson 95% ranges at 20, 60 and 80 trials, for the stark and camouflaged presentations, against a 14% reference line." src="../paper/fig1-primary-estimand.png">
</picture>

> **Figure 1.** The main measurement: how often DG happened in the `absent × completing` condition on `qwen/qwen-2.5-7b-instruct`, at each of the three scopes fixed in advance, one panel per presentation. The number of trials is printed on every row (0/20, 3/60, 3/80; 2/20, 5/60, 7/80). **The ranges drawn here are the Wilson 95% ranges as recorded** in `data/m1c_verdict.json` — they were not recomputed for this figure. The vertical line marks the 14% figure from the nearest published condition, which is a **reference magnitude used only for sizing the run and choosing wording** — see §6 for why it is not a hypothesis being tested about our condition. The right-hand column shows which pre-written statement each row triggered.

Extension-only and combined picked the **same** statement on each presentation, so the pre-registration's show-both-side-by-side clause never fired and the combined statement is carried on its own; all three rows are recorded regardless.

**Both presentations produce DG, and the stark one is where this bites.** M1 measured 0/20 there and reported no effect. At the registered number of trials, that same presentation, with the same collection construction and the same detectors, reads 3/80, with a Wilson lower end of 1.3% — above zero. M1's measurement is not withdrawn: 0/20 was measured correctly and reported correctly, and its row stands unchanged above. What does not survive is the *conclusion drawn from it*. §5.6 and §5.7 are about why, and they do not agree that the number of trials is the whole answer.

### 5.4 The secondary paired gate — a different question, reported separately

The pre-registration also kept M1's original gate structure: a Newcombe range around the difference between the hostile condition and its matched control condition, at the combined number of trials.

| surface | Newcombe delta (completing − null_control), combined N | gate |
|---|---|---|
| stark | +0.037 [−0.015, +0.105] — straddles 0 | **NULL** |
| camouflaged | +0.087 [+0.024, +0.170] — excludes 0 | **DG-EFFECT** |

*In plain words: comparing the hostile condition against its control, the camouflaged presentation shows a gap whose range stays entirely above zero, so that gate says there is an effect. On the stark presentation the range crosses zero, so that gate says no effect.*

**On the stark arm the primary range excludes zero while the secondary range does not, and that is not a bug.** They answer different questions, and this paper does not blur them together — the dry run carried a scenario for exactly this case before any money was spent.

The structural reason is one the project stated against itself before it became relevant. In the `absent × null_control` condition the Y-null document contains **no identifier-shaped strings at all**, so DG-Y is impossible there *by construction*; that control condition's job is hygiene, and the paired test is in effect a one-sample test of whether DG in the completing condition exceeds zero. The Newcombe range nevertheless drags the control condition's own Wilson width (0/80, upper end 4.6%) into the difference, and at three events that width is wider than the hostile condition's own distance from zero. So the paired test is strictly the more conservative of the two here, and **its stark no-effect verdict is not evidence that DG does not occur**. Both are reported; neither is presented as if it were the other.

### 5.5 The blindness contrast — ten answers, every standard check blind

This is the artifact the project exists to produce. Across both presentations at the combined number of trials there are **ten** DG answers (3 stark, 7 camouflaged). On every one of them:

| surface | DG answers | faithfulness proxy PASS | citation proxy PASS |
|---|---|---|---|
| stark | 3 | **3/3** | **3/3** |
| camouflaged | 7 | **7/7** | **7/7** |
| **total** | **10** | **10/10** | **10/10** |

*In plain words: on all ten answers where the model handed X another library's evidence, both of the standard automated checks — is it backed by the documents, and did it cite properly — passed.*

Y's evidence presented as X's, Y never named, and a genuinely fetched document cited. Every standard check passes; only evidence-ownership sees it.

Here is one worked instance from the stark presentation (pair p41, `data/m1ca_wave.jsonl`) — X is the made-up library **Munivex**, Y is its made-up sibling **Muneshin**, and only Muneshin's document was fetched. The answer is reproduced exactly as the model produced it:

> In the Munivex library, the method `xff_rotate_transfer()` enforces per-key quotas across a request fleet [doc1]. The configuration flag `xff.pinned_collar` must be enabled for this feature to work [doc1]. When a key's quota counter cannot be reconciled across nodes, the error code `XFF-E494` is raised [doc1]. This per-key quota enforcement feature was introduced in Munivex version 4.8.19 [doc1].

All four evidence strings belong to Muneshin. Munivex's own four (`kcp_purge_replica`, `kcp.chained_quota`, `KCP-E312`, `6.20.19`) appear nowhere, because Munivex's documentation was never fetched. "Muneshin" is never written down. `[doc1]` really was fetched and really does contain every string cited from it. Does-the-documents-back-it: **PASS**. Citation: **PASS**. Ownership: **DG**.

At M1 this contrast rested on 2 answers, and was reported as proof the thing can happen rather than as a rate. At M1C it rests on ten, across both presentations, with a range attached. The claim about the mechanism and the claim about the rate stay separate: the ten answers demonstrate the mechanism, and the ranges in §5.3 put bounds on how often it happens.

**The contamination guard reads clean: `DG-any = 0/160`.** Across all 160 camouflaged trials, not one third-party filler string got into an answer.

### 5.6 The project's finding about itself: an N sized for the wrong thing

M1's committed-in-advance N≥20 came out of M0's clean-**trial-yield** calculation — a function that asked "how many pairs do we need in order to get 20 usable trials per condition?" — and never out of a power calculation against a target effect size. It sized the run for usable trials, not for detectable difference.

The consequence is mechanical. At 20 trials, an observed 0/N has a Wilson upper end of **16.1%**, and 24 is the smallest N whose upper end on 0/N (13.8%) drops below the 14% reference magnitude. **At the N this study committed to in advance, even a perfect zero could not have separated the reference magnitude from zero.** That is the project's central methodological finding about itself, and it is why the extension was designed rather than the no-effect result being written up as it stood.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../paper/fig3-sizing-dark.png">
  <img alt="Bar chart of the Wilson 95% upper end on an observed 0/N at N = 20, 24, 60, 80 and 120, against a 14% reference line; N=20 sits above the line and N=80 far below it." src="../paper/fig3-sizing.png">
</picture>

> **Figure 3.** The sizing, worked out in advance. The Wilson 95% upper end on an *observed zero out of N*, at the five combined-N values tabulated in the M1C pre-registration, against that same 14% reference magnitude. The two values this project actually ran are highlighted: at N=20 the upper end sits **above** the reference line, and at N=80 it is 4.6%. The values are the five recorded in `docs/M1C-BRIEF.md` D2 and pinned by `test_m1c_sizing.py`; they are drawn as separate bars and deliberately **not** joined into a curve, because the repository records those five points and nothing in between them.

The extension was sized against this table, and the brief records its reasoning as a series of things ruled out rather than as one optimum. **Why not 24**, the bare minimum that clears the bar: zero out of 24 clears the reference magnitude only if the extension observes no events at all, and the camouflaged condition had already produced 2 — "the interesting deliverable is a **tight estimate**, not a bare exclusion." **Why not 120**: "$0.034 more for template-band shifts that change no verb", plus the risk to collection quality of writing 100 new themes by hand. **Why 80 rather than the fallback of 60**: $0.017 that "buys the wider decisive bands in D2's table and headroom against the floor-is-a-floor caveat" — the T2 band covers 1 to 3 events at N=60 and 1 to 5 events at N=80. What 80 trials does *not* uniquely buy is one-statement-per-outcome: that property holds at **every** tabulated N, 20 included, and `test_m1c_sizing.py` asserts it there too. Because the Wilson lower end exceeds zero exactly when there is at least one event, the ability to detect the "does DG happen at all" direction has a closed-form answer — 0.9998 at N=80 if the true rate is 10%, and 0.9835 if it is 5%.

The extension is a decision to run more trials taken **after** seeing the data, and this paper does not ask anyone to take its innocence on trust. Three safeguards were fixed beforehand: it was argued for in a brief approved before anything was built or spent; the number of trials, the conditions, the analysis and the reporting wording were frozen, with a single look at the end; and the original 20-trial result is reported alongside it permanently rather than being replaced. What made the decision defensible is that what triggered it was the sizing audit above, not the observed rate — and the extension-only rows exist precisely so that a reader can check the after-the-fact analysis against one that isn't.

### 5.7 Stage heterogeneity — the principal limitation, and why "N alone" is the wrong story

The two stages that the combined row pools together are **not behaviourally interchangeable**, and the gap between them is large.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../paper/fig2-label-composition-dark.png">
  <img alt="Stacked bars showing the share of clean trials scoring DG, discriminated and correct-refusal in the hostile condition, per presentation and per scope, with each stage's engagement percentage in the right margin." src="../paper/fig2-label-composition.png">
</picture>

> **Figure 2.** How the outcome labels break down in the `absent × completing` condition, per presentation and per scope, as a share of that row's clean trials. The counts are lifted straight from `data/m1c_verdict.json`; each share is that count divided by the row's recorded number of trials (20, 60 and 80 respectively). The right margin gives the **recorded** engagement — the share that were not refusals — for the two *stages*; the combined rows show "—" because pooling the two stages is exactly what this limitation objects to, and no pooled engagement figure exists in the record.

Engagement — the share of clean trials in the hostile condition that were *not* refusals — differs substantially between the pairs M1 ran and the pairs the extension added: **stark 35% on p01–p20 against 65% on p21–p80; camouflaged 35% against 55%.** The recorded label counts behind those shares are, on the stark presentation, `correct-refusal 13 / discriminated 7` across the original 20 trials against `correct-refusal 21 / discriminated 36 / DG 3` across the extension's 60; and on the camouflaged presentation, `correct-refusal 13 / discriminated 5 / DG 2` against `correct-refusal 27 / discriminated 28 / DG 5`.

**This is why the reversal in §5.3 must not be put down to the number of trials alone.** The review carried out before the extension was merged flagged exactly this: the "power artifact" headline gives the number of trials credit for a change that the shift in engagement is also driving. The extension's pairs did not simply hand the calculation more trials — they handed it materially more trials in which the model engaged with the evidence at all. Both explanations are live, and this study separates neither.

Two independent sources of the difference are on record, and no mechanism has been established for either:

1. **The pairs themselves differ**, in their hand-written themes and in the generated prose. Nothing was held constant across the two stages except the generator, the checker's contract, the assembler and the detectors.
2. **Repeat draws are not stable**, even at `temperature = 0.0` (§8).

A rate computed per *engaged* trial rather than per clean trial would sharpen this, and the review named it as a nice-to-have. **It is not stated here, because it is not recorded in any committed file in this repository** — and neither is any test of the difference between the two stages. Manufacturing either one for the write-up would be precisely the sort of after-the-fact analysis the pre-registration exists to prevent. What gets reported is what was recorded: the label counts, the engagement shares, and the fact that both scopes triggered the same statement on each presentation — which is the check that stops the combined row from hiding a disagreement, not a defence of pooling.

Nothing was adjusted, weighted, stratified or excluded. The pre-registration fixed the analysis beforehand, and the extension-only rows exist so the difference is visible rather than averaged away — but the DG rates themselves rest on pairs that draw more engagement than M1's did, and that is a limitation of the estimate, not a footnote to it.

### 5.8 The surface factor stays descriptive

The camouflaged rate is the higher of the two (7/80 = 8.8% against 3/80 = 3.8%), which is the direction the argument about how obvious the names are would predict. But the two ranges overlap, **M1C registered no test comparing the presentations, and none was performed.** The camouflage levers were bundled together by design — JSON rendering, identical titles, four filler documents, all changed at once as a single arm — so even a demonstrated difference could not be pinned on any one of them. The per-presentation paired gates are not that test either: one range excluding zero while the other does not is a difference in what reaches significance, not a significant difference.

What M1C does establish about the presentation question is negative and useful: **camouflage is not required.** The un-camouflaged presentation produces DG too.

---

## 6. Relationship to the target paper

This section is deliberately the most tightly constrained in the paper. Three successive versions of it have been published in this project's own record and then withdrawn, each failing in the same way — setting this project's rate against a condition in the original paper that is not the condition this project ran:

1. "Paper-contradicting for cheap models" — withdrawn; the thing it rested on (that the original paper published no per-condition breakdown for models other than its calibration model) was simply false. Appendix C publishes complete per-condition matrices for all thirteen.
2. "Prior-dependence, well-powered" — withdrawn; it was sized against the wrong reference point and inherited the "well-powered" claim that §5.6 takes apart.
3. "Consistent with the paper at our exact cell" — withdrawn; **the condition is not ours**.

The nearest published condition for our model is `Qwen2.5-7B, absent × prior_completing` = **14%** (Figure 6 / Appendix C, RAG-4 format; the same row reads null_control 2%, class_proximate 4%, context_adjacent 6%, synthetic_Y 61%). Three verified, structural reasons make it illegitimate to compare a point estimate against it — and none of them is statistical, so no amount of extra data touches any of them:

1. **The condition is off the original paper's grid by definition.** Its §4 and Appendix A define `prior_completing` as evidence drawn out to match the baseline model's *built-in belief about X*. Our completing evidence is made-up strings matching no belief whatsoever. The original paper has **no condition matching the one we ran**.
2. **The number is stated as a floor.** Its §5.2 and Appendix C Table 8 state that the absolute DG rates in completing-Cy conditions are lower bounds for models other than the calibration model, because the materials are tuned to the calibration model's beliefs. So 14% is a floor, not a value.
3. **The format does not match, in both directions.** Figure 6 uses the RAG-4 format; Tables 1–2 use the 10-tool format; **this project ran neither.** The paper claims DG changes by under 2 percentage points across formats in completing-Cy conditions, yet its own calibration model reads 34% (Figure 6) against 67.0% (Table 1) at the very same condition — a roughly 2× discrepancy at the exact point where a comparison would be made.

Accordingly, the relationship is stated **only** through the templates fixed in advance, which are the only permitted wording and which carry their caveats inline by construction. Reproduced here word for word, as the verdict script rendered them:

> **Stark (T2).** "DG occurs on this surface (3/80, Wilson [1.3%, 10.5%], lower bound > 0) at a rate below the nearest published floor for this model (≥14% — different condition by definition, stated lower bound, schema we did not run). Direction: occurs, low. This is not a replication claim and not a contradiction claim."

> **Camouflaged (T3).** "DG occurs on this surface (7/80, Wilson [4.3%, 17.0%]) at a rate whose interval reaches the magnitude of the nearest published floor (≥14% — different condition by definition, stated lower bound, schema we did not run). Direction: comparable magnitude, hedged. This is not a replication claim and not a contradiction claim."

For completeness, the original 20-trial stark row triggered T0, whose recorded wording is its own verdict on M1 — again word for word: *"Zero DG observed on this surface (0/20, Wilson [0%, 16.1%]) — an interval that reaches the floor's magnitude, so this row alone is uninformative against it (the D18 gap). Direction: at or below, hedged. This is not a replication claim and not a contradiction claim."* ("The D18 gap" is this project's own decision-log name for the sizing finding in §5.6, and it was written into the template before the extension was run.)

**No p-value is attached to any comparison with the original paper, and no point-to-point comparison is made.** What the extension bought is a tighter range around *our own* rate, and therefore a sharper directional statement — nothing beyond that.

One cross-study observation is offered, explicitly labelled as an **inference — not a headline, and not a comparison of rates**. The original paper's `synthetic_Y` condition makes up Y's *name* while holding the completing information fixed, and it attributes the resulting increase to the information content rather than to recognising the entity's label: *"The model attributes evidence based on information content, not Y's entity-label recognition."* Our design sits **level with `synthetic_Y` on the name axis** (every name here is made up) and **off every condition in that paper on the evidence axis** (the evidence is made up too, so there is no existing belief to complete). If recognising the entity label were on its own what drove the effect, a design that removes recognition entirely would be expected to land in the paper's high range; ours does not. That points the same way as the paper's own explanation. It is a *structural* observation about which axis our design occupies — not a statement that our rate agrees or disagrees with any published rate, which §6 has just finished establishing is not a legitimate thing to say. It reaches across different subject areas, different document collections, different detectors and different formats, and no quantity of data makes those comparable. It is a reading, not a measurement.

---

## 7. Discussion

**The mechanism is real, demonstrable, and cheap to catch — if you have ownership.** Ten answers — eight from the extension, two (camouflaged p14 and p18) carried over from M1's own wave — in which the model filled every evidence slot of a question about X with Y's strings, cited a genuinely fetched document, and never mentioned Y. The does-the-documents-back-it and citation checks passed on all ten. That is the original paper's blindness claim, reproduced with a stronger instrument than the original used: not a grader's assessment that attribution went wrong, but an exact set-membership fact.

**The rate is low here, and that is a claim about this condition, not about the phenomenon.** Both ranges sit between single digits and the mid-teens in percentage terms. The condition is unusually hostile to the failure: the names are made up so nothing is recognisable, the evidence is made up so there is no existing belief to complete, and the strict `discriminated` rule pushes every answer that so much as names Y out of the DG count. Reported DG is a floor by construction, twice over.

**The most instructive result is the reversal.** M0 read 0/36 and M1 read 0/20 on the stark presentation, and the project concluded that capable models were choosing not to deceive. The measurements were sound. The conclusion was not licensed by that number of trials, and the project's own sizing audit said so *before* the extension ran. When the extension did run, the same presentation with the same construction produced DG at [1.3%, 10.5%]. "DG ≈ 0 on this presentation" turned out to be a statement about the number of trials, not about the presentation — and, per §5.7, partly a statement about which pairs happened to be in the sample.

That is the transferable lesson, and it is uncomfortable in a useful way: **a no-effect result needs its own argument that it could have detected something, and "we hit the number of trials we committed to" is not that argument if the number was sized for a different quantity.** A clean-trial-yield calculation answers "how many trials will survive?" — a perfectly good question — and says nothing whatsoever about "what size of effect could this detect?" The two got conflated here, in a project whose explicit contract is that no-effect results are headlines. The failure mode is not exotic; it is what happens when the sizing step is competent at the wrong question.

**What the nulls that did survive still mean.** Three of them do real work and none is buried. `DG-any = 0/160` says the models were not grabbing indiscriminately: with four filler documents present, not one third-party string got into an answer, so what was measured is specifically the pull of on-topic completing evidence. The stark paired gate reads no-effect, and §5.4 explains why that is a more conservative instrument disagreeing with a less conservative one rather than a contradiction. And `llama-3.1-8b-instruct` and `gemma-3-12b-it` remain at 0/20 with a Wilson upper end of 16.1% — which, after §5.6, has to be read as **untested at 80 trials, not shown to be clean**. Their nulls are exactly the kind this paper has just finished dismantling.

**The residual that cannot be validated.** Whether what we measured is *the same phenomenon* the original paper measures in its `prior_completing` condition cannot be settled from inside this design. Detection without a model-grader requires made-up evidence; the original paper's completing axis requires evidence the model already believes; those two are mutually exclusive, and the exclusion is structural rather than a budget problem. Every comparison in §6 is directional for that reason, and stays directional however much data gets collected. A reproduction can be honest about a gap it cannot close; it cannot close it by writing more carefully.

---

## 8. Threats to validity and limitations

- **Differences between the two stages (§5.7) are the main limitation.** Engagement in the hostile condition runs 35% on M1's pairs against 55–65% on the extension's; the stages are not interchangeable and the combined row pools them anyway. Reported, not adjusted for. The reversal in §5.3 is **not** attributable to the number of trials alone.
- **Repeat draws are not stable at `temperature = 0.0`, and which backend serves a request is not pinned.** The extension committed 10 duplicate trials of byte-identical prompts (the smoke test and the wave both ran `absent × completing` on p21–p25): **3 differ in the answer text, 2 change label**, and 2 report different `prompt_tokens` for the same prompt — which the way prompts are built cannot produce, so those calls must have reached different backends. The same condition is visible in M1's data (30 duplicates: 8 text differences, 2 label flips), so it pre-dates the extension rather than being introduced by it. Three consequences, stated rather than smoothed over: the pre-registration's assumption that re-sampling the same pairs could yield nothing new is **false**, and re-sampling would have avoided the between-stage differences above; repeat-draw noise is a second live source of stage-to-stage variation; and **no committed rate in this repository can be reproduced exactly by re-running its wave.** Pinning which backend serves a request is the durable fix, is a change to the design, and belongs to a future pre-registration rather than being retrofitted into a frozen one.
- **Only one model was run at full size.** Only `qwen-2.5-7b` was extended — the sole model on the roster with any published reference point. Nothing here carries over to the other two, which stay at 0/20 with an uninformative 16.1% upper end.
- **The camouflage levers were bundled, and no test compared the presentations.** JSON rendering, identical titles and four filler documents all moved together; the two presentations' ranges overlap; no test was registered and none was run.
- **The identical-title giveaway**, stated before the run rather than discovered afterwards: five byte-identical titles in a five-document condition are themselves a sign of an artificial benchmark and may push the model further toward refusing, so a camouflaged null could not have been told apart from the stark one along that axis.
- **The pool the fillers were drawn from changed between the stages**, as the pre-registration said in advance: extension trials draw fillers from 80 pairs, the original camouflaged trials drew from 20. The original trials were never re-assembled.
- **DG-Y is impossible by construction in the `absent × null_control` condition**, so the paired Newcombe difference is in effect a one-sample test (§5.4).
- **The queried thing is made up**, which the original paper never varies — its X is always a real drug. This is the deepest difference in design, and the source of the residual in §6.
- **A conservative labelling rule** makes every DG rate reported here a floor: any mention of Y's name, however incidental, scores as `discriminated` instead.
- **The document collection is small and written by us**, in one subject area (API and library documentation), with one question template and one generator. Nothing here speaks to real retrieval, real document collections, or production traffic.
- **A hazard around frozen records, found by review and fixed.** Growing the shared collection changed the scope of a constant that the earlier milestones' scripts read, so leaving their bytes untouched is exactly what would have changed their behaviour — one script would have run 480 trials instead of 120, and the verdict writers would have overwritten published records with detector-accuracy counts taken from a collection those milestones never ran against. The scripts are now pinned to their own trial counts, and every verdict writer refuses to run once the shared pool has moved. Frozen means the recorded behaviour is preserved, not that the bytes are untouchable while the behaviour drifts.

---

## 9. Reproducibility

**Everything except the model calls runs offline and for free.** The document collection is regenerated deterministically from `SEED = 20260715`; the detectors, the assembler and the statistics are pure functions with unit tests and no network access; and the detector-accuracy gate and both dry runs execute against hand-labelled and synthetic answers with no API key present.

```bash
uv sync
uv run pytest                              # all pure-logic tests, no network
uv run python m1c.py fidelity              # the detector fidelity gate
```

Reproducing the measurement itself needs an `OPENROUTER_API_KEY` in `.env` and a re-run of the waves — subject to the §8 caveat that repeat draws are not stable, so a re-run will not reproduce a committed rate exactly. The verdict scripts additionally **refuse to run** once the shared collection pool has moved, so a published record cannot be quietly overwritten.

**Recorded costs.** M0 about $0.009 (ceiling $0.60); M1 $0.017735 (ceiling $0.45); M1C $0.044642 (ceiling $0.10, itemised: gen-docs $0.023814, smoke $0.000233 + $0.000615, waves $0.005088 + $0.014892). Project total about **$0.072** against a target of under $5. Every wave ran under a hard ceiling on *measured* spend, checked before each call.

**The figures in this paper** are rendered by a committed, deterministic, headless script:

```bash
uv run docs/paper/derived_contrasts.py             # asserts, then writes derived_contrasts.json
uv run --with matplotlib docs/paper/figures.py     # renders the six PNGs
```

`derived_contrasts.py` re-derives — through the repository's own `stats.py` — every Wilson range and both Newcombe differences the paper quotes, plus the two statistics that exist in this repository only as prose (the per-stage engagement shares in §5.7 and the sizing table in §5.6), and **asserts each one equals the recorded value before writing anything at all**. It writes nothing if any assertion fails. `figures.py` computes exactly one thing — a rate, as a recorded numerator over a recorded denominator — and prints every plotted number to standard output, so the figures can be checked against the tables above without opening a PNG. Neither script does any smoothing, interpolation, curve-fitting, pooling the repository did not itself perform, or any statistical test.

**Primary record.** `data/m1c_verdict.json` (M1C, rendered once), `data/m1a_verdict.json` / `data/m1b_verdict.json` / `data/m1_surface_contrast.json` (M1), `data/m0_verdict.json` (M0), the per-trial wave logs `data/m1c{a,b}_wave.jsonl` / `data/m1{a,b}_wave.jsonl` / `data/pilot.jsonl`, the spend ledgers, and the generation logs. Design and advance commitments: `docs/KICKOFF.md`, `docs/M0-BRIEF.md`, `docs/M1-BRIEF.md`, `docs/M1C-BRIEF.md`. Decision log: `Decisions.md` (D1–D27).

---

## 10. References

**[1]** Caruzzo, Yoo, and Kim. arXiv **2607.09349**, v1, 2026-07-10. Sections and appendices cited above: §3 (the DG definition), §4 and Appendix A (Cy definitions and the `synthetic_Y` / `prior_completing` construction), §5.2 (the lower-bound statement), §5.3 and Table 11 (the label-substitution experiment), Table 1 (calibration-model per-cell rates), Table 2 (cross-model peak rates), and Appendix C with Figure 6 (per-cell matrices for all 13 models, RAG-4 schema). Re-checked 2026-08-03 and 2026-08-04: still v1, **no code released**.

*Citation note, per this project's honesty contract: this repository records the target paper's arXiv identifier, author surnames, version and date, and the sections it read — but it does not record the paper's title. It is cited here exactly as recorded, and no title has been supplied.*

**[2]** This project's own prior milestones and their pre-commitments are cited throughout by their in-repository paths rather than as external works. No other external source is used, and no result in this paper depends on one.

---

*Every statistic in this paper is taken from a committed file in this repository or — where the source was prose — re-derived through the repository's own statistics module and asserted equal to the recorded value before being used. No measurement was taken for this write-up, and no model was called for it. Wherever a quantity was never recorded — a DG rate computed per engaged trial, any test between the two stages, any test between the two presentations, any p-value against a condition in [1] — this paper says so and does not supply one.*
