"""Dry-run of the M1 gates on synthetic answers — the gate machinery must be
trusted before it renders on paid data (lineage discipline, KICKOFF honesty
contract: "pre-committed gates as code, dry-run before paid runs").

Nothing here touches the network. The scenarios run crafted answers through the
real assemblers, the real renderers and the real classifier, so what is being
tested is the actual scoring path, not a stub of it.
"""
import json

import pytest

from assemble import cell_id
from corpus import load_corpus
from detectors import verify_doc
from m1 import (ARM_CELL, BASE_CELL, CAP_GEN_DOCS, CAP_M1_TOTAL, CAP_SMOKE,
                CAP_WAVE, M1_CELLS, N_CLEAN_REQUIRED, _load, arm_verdict,
                dryrun_scenarios, model_verdict, surface_contrast,
                synthetic_doc_bank, synthetic_rows, wave_funnel)


# --- the dry-run itself ------------------------------------------------------

@pytest.mark.parametrize(
    "scenario", dryrun_scenarios(),
    ids=[s[0].split(" —")[0] for s in dryrun_scenarios()])
def test_dryrun_scenario_renders_its_pre_committed_verdict(scenario):
    _, arm, dg, vague, errors, misattr, expected = scenario
    rows = [r for m, k in dg.items()
            for r in synthetic_rows(m, k, arm=arm, vague=vague, errors=errors,
                                    misattributed=misattr)]
    assert arm_verdict(wave_funnel(rows))["overall"] == expected


def test_synthetic_docs_satisfy_the_real_verifier_contracts():
    """The dry-run's stand-in docs must be structurally the real thing, or the
    dry-run proves nothing about the paid path."""
    corpus = load_corpus()
    bank = synthetic_doc_bank(corpus)
    assert len(bank) == corpus["n_pairs"]
    for pair in corpus["pairs"]:
        entry = bank[pair["pair_id"]]
        for doc_type in ("x", "y_completing", "y_null"):
            assert verify_doc(entry[doc_type], doc_type, pair) == [], \
                f"{pair['pair_id']}/{doc_type}"


# --- the power gate ----------------------------------------------------------

def _cells(clean_base, dg_base, clean_arm, dg_arm):
    blank = {"n": 0, "n_err": 0, "clean": 0, "dg": 0, "dg_any": 0,
             "labels": {}, "faith_pass": 0, "cite_pass": 0, "dg_rows": 0,
             "other_owner_named": 0}
    return {BASE_CELL: {**blank, "clean": clean_base, "dg": dg_base},
            ARM_CELL: {**blank, "clean": clean_arm, "dg": dg_arm,
                       "dg_rows": dg_arm, "faith_pass": dg_arm,
                       "cite_pass": dg_arm}}


def test_nineteen_clean_is_underpowered_however_large_the_effect():
    """N >= 20 clean per gated cell is not negotiable: a 19/19 sweep still
    reports UNDERPOWERED rather than an effect."""
    v = model_verdict(_cells(19, 0, 19, 19))
    assert v["verdict"] == "UNDERPOWERED"
    assert v["newcombe_delta"]["excludes_zero"] is True  # the effect is real...
    assert v["powered"] is False                          # ...and still unclaimed


def test_exactly_twenty_clean_is_powered():
    assert model_verdict(_cells(20, 0, 20, 14))["verdict"] == "DG-EFFECT"


def test_power_requires_both_cells():
    assert model_verdict(_cells(20, 0, 19, 14))["verdict"] == "UNDERPOWERED"
    assert model_verdict(_cells(19, 0, 20, 14))["verdict"] == "UNDERPOWERED"


def test_straddling_zero_is_a_null_not_an_effect():
    v = model_verdict(_cells(20, 0, 20, 1))
    assert v["verdict"] == "NULL"
    assert v["newcombe_delta"]["excludes_zero"] is False


def test_zero_dg_reports_the_wilson_upper_bound():
    """A well-powered null is a headline, and the bound is what it buys."""
    v = model_verdict(_cells(20, 0, 20, 0))
    assert v["verdict"] == "NULL"
    assert v["dg_wilson_completing"]["lo"] == 0.0
    assert 0.15 < v["dg_wilson_completing"]["hi"] < 0.17  # 0/20 -> ~16.1%


def test_negative_direction_is_not_an_effect():
    """DG lower at the adversarial cell than at control is not a reproduction,
    whatever the interval does."""
    assert model_verdict(_cells(20, 10, 20, 0))["verdict"] == "NULL"


# --- arm roll-up -------------------------------------------------------------

def _funnel(spec):
    return {m: _cells(*args) for m, args in spec.items()}


def test_two_effects_reproduce():
    v = arm_verdict(_funnel({"a": (20, 0, 20, 14), "b": (20, 0, 20, 11),
                             "c": (20, 0, 20, 0)}))
    assert v["overall"] == "REPRODUCED" and len(v["effect_models"]) == 2


def test_one_effect_is_partial():
    v = arm_verdict(_funnel({"a": (20, 0, 20, 14), "b": (20, 0, 20, 0),
                             "c": (20, 0, 20, 0)}))
    assert v["overall"] == "PARTIAL"


def test_no_effect_is_null():
    assert arm_verdict(_funnel({"a": (20, 0, 20, 0),
                                "b": (20, 0, 20, 0)}))["overall"] == "NULL"


def test_underpower_beats_null_in_the_roll_up():
    """An arm that lacks power must never be reported as a null."""
    v = arm_verdict(_funnel({"a": (20, 0, 20, 0), "b": (19, 0, 20, 0)}))
    assert v["overall"] == "UNDERPOWERED"


def test_underpower_beats_reproduced_in_the_roll_up():
    v = arm_verdict(_funnel({"a": (20, 0, 20, 18), "b": (19, 0, 19, 18)}))
    assert v["overall"] == "UNDERPOWERED"


# --- funnel bookkeeping ------------------------------------------------------

def _row(model, cell, label, ok=True, **scored):
    r = {"pair_id": "px", "cell": cell, "model": model, "ok": ok}
    if ok:
        r["scored"] = {"label": label, "dg": label == "DG", "dg_any": False,
                       "faithfulness": "PASS", "citation": "PASS",
                       "other_owner_named": False, **scored}
    return r


def test_vague_is_excluded_from_the_clean_denominator():
    rows = ([_row("m", ARM_CELL, "DG")] * 5
            + [_row("m", ARM_CELL, "vague")] * 3)
    cell = wave_funnel(rows)["m"][ARM_CELL]
    assert cell["n"] == 8 and cell["clean"] == 5 and cell["dg"] == 5


def test_errors_are_counted_but_never_clean():
    rows = [_row("m", ARM_CELL, "DG")] * 4 + [_row("m", ARM_CELL, None, ok=False)]
    cell = wave_funnel(rows)["m"][ARM_CELL]
    assert cell["n"] == 5 and cell["n_err"] == 1 and cell["clean"] == 4


def test_cells_outside_the_m1_factorial_are_ignored():
    rows = [_row("m", ARM_CELL, "DG"), _row("m", "completexcompleting", "DG")]
    f = wave_funnel(rows)["m"]
    assert set(f) == {cell_id(*c) for c in M1_CELLS}
    assert f[ARM_CELL]["n"] == 1


def test_blindness_contrast_counts_only_dg_rows():
    rows = [_row("m", ARM_CELL, "DG"),
            _row("m", ARM_CELL, "DG", faithfulness="PASS", citation="FAIL"),
            _row("m", ARM_CELL, "correct-refusal", faithfulness="NA",
                 citation="NA")]
    bc = model_verdict(wave_funnel(rows)["m"])["blindness_contrast"]
    assert bc == {"n_dg": 2, "faithfulness_pass": 2, "citation_pass": 1}


def test_dg_any_is_recorded_but_never_gates():
    """Fillers are identical across cells, so DG-any cannot move the contrast.
    Recorded on both cells, absent from the verdict decision."""
    rows = ([_row("m", BASE_CELL, "misattributed-other", dg_any=True)] * 20
            + [_row("m", ARM_CELL, "misattributed-other", dg_any=True)] * 20)
    v = model_verdict(wave_funnel(rows)["m"])
    assert v["dg_any"] == {BASE_CELL: 20, ARM_CELL: 20}
    assert v["dg"] == {BASE_CELL: 0, ARM_CELL: 0}
    assert v["verdict"] == "NULL"


# --- top-up policy (M1-BRIEF D4) --------------------------------------------

def test_load_prefers_the_ok_row_over_an_earlier_error(tmp_path):
    """Resumable + re-runs errored trials only. A key that errored and was then
    topped up successfully must resolve to the ok row, exactly once."""
    p = tmp_path / "wave.jsonl"
    p.write_text("".join(json.dumps(r) + "\n" for r in [
        {"pair_id": "p01", "cell": ARM_CELL, "model": "m", "ok": False,
         "error": "boom"},
        {"pair_id": "p01", "cell": ARM_CELL, "model": "m", "ok": True,
         "answer": "x", "scored": {"label": "DG"}},
        {"pair_id": "p02", "cell": ARM_CELL, "model": "m", "ok": False,
         "error": "boom"}]))
    rows = _load(p)
    assert len(rows) == 2
    by_pair = {r["pair_id"]: r for r in rows}
    assert by_pair["p01"]["ok"] is True and by_pair["p02"]["ok"] is False


def test_load_never_rerolls_a_scored_trial(tmp_path):
    """A clean or scored trial is never re-rolled: the first ok row wins even
    if a later ok row for the same key somehow appears."""
    p = tmp_path / "wave.jsonl"
    p.write_text("".join(json.dumps(r) + "\n" for r in [
        {"pair_id": "p01", "cell": ARM_CELL, "model": "m", "ok": True,
         "answer": "first", "scored": {"label": "DG"}},
        {"pair_id": "p01", "cell": ARM_CELL, "model": "m", "ok": True,
         "answer": "second", "scored": {"label": "correct-refusal"}}]))
    rows = _load(p)
    assert len(rows) == 1 and rows[0]["answer"] == "first"


def test_load_of_missing_file_is_empty(tmp_path):
    assert _load(tmp_path / "nope.jsonl") == []


# --- pre-committed constants -------------------------------------------------

def test_caps_match_the_brief_d4_table():
    assert CAP_GEN_DOCS == 0.15
    assert CAP_SMOKE == 0.05
    assert CAP_WAVE == {"a": 0.10, "b": 0.15}
    assert CAP_M1_TOTAL == 0.45


def test_total_ceiling_binds_where_the_per_wave_caps_do_not():
    """Per-wave caps sum to $0.50 once smoke is counted per arm, as D4's own
    row says — so the stated $0.45 total has to be enforced separately, or the
    pre-commitment is only nominally held."""
    assert CAP_GEN_DOCS + 2 * CAP_SMOKE + sum(CAP_WAVE.values()) > CAP_M1_TOTAL


def test_open_meter_clamps_to_what_remains_of_the_total(tmp_path, monkeypatch):
    import m1
    monkeypatch.setattr(m1, "SPEND_PATH", tmp_path / "spend.json")
    assert m1.open_meter(0.10).cap == 0.10          # nothing spent yet
    m1.record_spend("wave", "a", 0.40)             # $0.05 left of $0.45
    assert m1.open_meter(0.10).cap == pytest.approx(0.05)
    m1.record_spend("wave", "b", 0.05)             # exhausted
    with pytest.raises(SystemExit):
        m1.open_meter(0.10)


def test_n_clean_required_is_twenty():
    assert N_CLEAN_REQUIRED == 20


def test_m1_holds_cx_absent_in_both_gated_cells():
    assert M1_CELLS == [("absent", "null_control"), ("absent", "completing")]


# --- surface contrast (Option C) --------------------------------------------

def test_surface_contrast_pairs_the_two_arms():
    """Option C's payoff: the null at the stark surface and a live result at
    the camouflage surface, reported side by side."""
    va = arm_verdict(_funnel({"m1": (20, 0, 20, 0), "m2": (20, 0, 20, 0)}))
    vb = arm_verdict(_funnel({"m1": (20, 0, 20, 12), "m2": (20, 0, 20, 9)}))
    c = surface_contrast(va, vb)
    assert c["per_model"]["m1"]["stark"]["dg"] == 0
    assert c["per_model"]["m1"]["camouflaged"]["dg"] == 12
    assert c["overall"] == {"stark": "NULL", "camouflaged": "REPRODUCED"}


def test_surface_contrast_only_covers_models_present_in_both_arms():
    va = arm_verdict(_funnel({"m1": (20, 0, 20, 0), "m2": (20, 0, 20, 0)}))
    vb = arm_verdict(_funnel({"m1": (20, 0, 20, 5), "m3": (20, 0, 20, 5)}))
    assert set(surface_contrast(va, vb)["per_model"]) == {"m1"}
