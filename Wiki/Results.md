# Results

## Purpose
Every milestone's headline numbers in one place, with the pre-registered prediction beside the observed outcome. Synthesizes across `docs/M0-BRIEF.md`, `docs/M1-BRIEF.md` and the three machine-rendered verdict files, none of which hold the whole picture on their own. For anyone who needs the project's measured record without reading two briefs and three JSON files.

## Key understanding

### The measured record

**Fact** (`data/m0_verdict.json`, `data/m1a_verdict.json`, `data/m1b_verdict.json` — all rendered mechanically by the verdict scripts):

| | M0 fit-pilot | M1a — stark | M1b — camouflaged |
|---|---|---|---|
| pairs × cells × models | 12 × 4 × 3 = 144 | 20 × 2 × 3 = 120 | 20 × 2 × 3 = 120 |
| calls ok | 144/144 | 120/120 | 120/120 |
| clean per gated cell | — (pilot, ungated) | 20/20 all models | 20/20 all models |
| **DG-Y at absent×completing** | **0/36** | **0/60** | **2/60** |
| DG-Y at absent×null_control | 0/36 | 0/60 | 0/60 |
| discriminated at absent×completing | 18/36 | 30/60 (7/8/15) | 15/60 (5/1/9) |
| correct-refusal at absent×completing | 18/36 | 30/60 | 43/60 |
| vague / confabulation | 0 / 0 | 0 / 0 | 0 / 0 |
| DG-any (fillers) | n/a (no fillers) | 0/120 | 0/120 |
| fidelity gate | 16/16 | 288/288 | 288/288 |
| verdict | **FIT** | **NULL** (well-powered) | **NULL** (well-powered) |
| spend | ≈$0.009 | — | — (M1 total $0.0177) |

**Fact** (`data/m1a_verdict.json`, `data/m1b_verdict.json`): per-model Wilson 95% intervals on DG at the adversarial cell are [0.0%, 16.1%] for every model/arm except `qwen-2.5-7b` camouflaged, which is [2.8%, 30.1%] on 2/20. Pooled M1a 0/60 → [0.0%, 6.0%] (descriptive only; models are not exchangeable).

### Prediction vs. outcome

**Fact** (`docs/M0-BRIEF.md` Pilot outcome addendum, written 2026-07-15 — *before* M1 ran): "as designed, M1 would very likely render a well-powered NULL." **Observed:** exactly that, on all three subjects, at both surfaces. The pre-registration held.

**Fact** (`docs/M1-BRIEF.md` D1): Option A's stated expected outcome was "DG 0/20 (or near) per model → NULL, well-powered", with the headline bound "DG ≤ 16.1% (95% Wilson upper)". **Observed:** 0/20 per model, bound 16.1%. The number written in the brief before the run is the number the run produced.

**Inference** (from D3 and the M1b result): Option C's stated payoff was that *every* outcome would be a clean headline. The realized branch is DG≈0 at both surfaces.

**Contradiction — corrected 2026-08-03, see [Paper-Mapping](Paper-Mapping.md).** An earlier version of this page (and the README) compared our 0/20 against "66.3% DG for Qwen2.5-7B" as though the two were the same condition. They are not: Table 2 of the paper reports 66.3% as that model's **peak cell only — `absent × synthetic_Y`** — and the paper publishes **no** per-cell breakdown for any non-calibration model. The correct cell-matched anchor is the calibration model's Table 1 (`absent × prior_completing` = 67.0%, `absent × synthetic_Y` = 73.1%, `absent × null_control` = 26.5%), which is a different model from any on our roster. The claim "paper-contradicting for cheap models" was therefore not supported at the cell level and has been withdrawn.

### The flagship artifact

**Fact** (`data/m1b_wave.jsonl`, pairs p14 and p18, model `qwen/qwen-2.5-7b-instruct`): two answers score `DG` — every one of the four evidence slots filled with Y's tokens, attributed to X *by name*, Y never mentioned, a genuinely retrieved doc cited. On both, the mechanical **faithfulness proxy PASSES and the citation proxy PASSES**. This is the blindness contrast the project exists to render: standard checks see nothing; token ownership sees everything.

**Inference:** n=2 is an existence proof, not a rate. The gate reports NULL for that model (Newcombe +0.100 [−0.077, +0.301], straddles 0) and the artifact is reported as a demonstration of the *mechanism*, never as a measured DG frequency.

### The surface factor

**Fact** (`data/m1_surface_contrast.json`): stark 0/20 vs camouflaged 2/20 for `qwen-2.5-7b`; 0/20 vs 0/20 for both others. **Inference:** every DG in the project appeared only at the camouflage surface and only on the paper's kin model — consistent with the M1-BRIEF E3 fidelity-gap reading, and far too small to support it. The cross-surface delta straddles 0.

### Why DG-any reads zero and the split was still required

**Fact** (`data/m1b_verdict.json`): under k=4 off-theme fillers, DG-any is 0/120 — no model at either cell pulled a single third-party token. **Inference:** the detector split (see [Detector-Design](Detector-Design.md)) therefore never had to separate anything in practice, but was not optional: without it those trials could only have been scored `confabulation`, and the claim "no model grabbed filler evidence" would have been unavailable to make.

## Sources
- [`data/m0_verdict.json`](../data/m0_verdict.json), [`data/m1a_verdict.json`](../data/m1a_verdict.json), [`data/m1b_verdict.json`](../data/m1b_verdict.json), [`data/m1_surface_contrast.json`](../data/m1_surface_contrast.json) — machine-rendered verdicts, the primary record
- [`data/m1b_wave.jsonl`](../data/m1b_wave.jsonl) — the two DG answer texts behind the flagship contrast
- [`docs/M0-BRIEF.md`](../docs/M0-BRIEF.md) — D7/D8 pre-commitments, Pilot outcome addendum (the M1 prediction)
- [`docs/M1-BRIEF.md`](../docs/M1-BRIEF.md) — D1–D4 pre-commitments, "The pick", "M1 outcome" addendum
- [`Decisions.md`](../Decisions.md) — D3 (FIT), D6 (Option C), D7–D11 (M1 run and verdict)

## Uncertainties & contradictions
- **Unresolved:** whether the 2 DG answers reflect a real camouflage effect or sampling noise. n=2 cannot distinguish them, and the pre-committed gate declines to try.
- **Unresolved:** an M1b null cannot be distinguished from M0's on the constant-title axis — five byte-identical titles are themselves a synthetic-benchmark tell that may reinforce the refusal ceiling. Stated in `docs/M1-BRIEF.md` D2 *before* the run, not discovered after.
- **Unresolved:** the camouflage levers (JSON rendering, fillers, constant title) were bundled; no attribution among them is possible from this data.
- **Unresolved:** DG-Y is impossible by construction at absent×null_control (the Y-null doc has zero tokens), so the Newcombe delta is effectively a one-sample test of DG(completing) > 0. Stated in the brief so the gate is not oversold.

## Related pages
- [Why-The-Null](Why-The-Null.md) — what the nulls mean and what they do not rule out
- [Detector-Design](Detector-Design.md) — how each number above is produced mechanically
- [History](History.md) — the chronology these results sit in

## Relevance to current work
This is the evidence base for the open call in `PROJECT.md`: whether v1 closes at M1 (D11, **Proposed**) or the null gets pushed on via a documented escalation. It is also the table a write-up (`/research-paper`) would be built from — every number here is traceable to a committed file.

_Last reviewed: 2026-08-03_
