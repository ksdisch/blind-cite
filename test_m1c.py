"""Dry-run of the M1C gate and the D4 rendering on synthetic answers, plus the
pre-committed constants (docs/M1C-BRIEF.md).

Same discipline as test_m1.py one milestone on: nothing here touches the
network, and the scenarios run crafted answers through the real assemblers, the
real renderers and the real classifier, so what is tested is the actual scoring
and rendering path rather than a stub of it. The band/template partition itself
lives in test_m1c_sizing.py.
"""
import json

import pytest

from corpus import load_corpus
from detectors import verify_doc
from m1c import (ARM_CELL, BASE_CELL, CAP_GEN_DOCS, CAP_M1C_TOTAL, CAP_SMOKE,
                 CAP_WAVE, EXTENSION_PAIR_IDS, M1C_CELLS, MODEL, N_EXTENSION,
                 N_ORIGINAL, N_CLEAN_REQUIRED_M1C, ORIGINAL_PAIR_IDS, TEMPLATES,
                 _load, dryrun_scenarios, render_template, scope_counts,
                 surface_verdict, synthetic_doc_bank, synthetic_rows)


# --- the dry-run itself -------------------------------------------------------

@pytest.mark.parametrize(
    "scenario", dryrun_scenarios(),
    ids=[s[0].split(" —")[0] for s in dryrun_scenarios()])
def test_dryrun_scenario_renders_its_pre_committed_verdict_and_band(scenario):
    (_, arm, dg_o, dg_e, vague, errors, misattr,
     want_verdict, want_band) = scenario
    sv = surface_verdict(
        synthetic_rows(arm, ORIGINAL_PAIR_IDS, dg_o),
        synthetic_rows(arm, EXTENSION_PAIR_IDS, dg_e, vague=vague,
                       errors=errors, misattributed=misattr))
    assert sv["verdict"] == want_verdict
    assert sv["rows"]["combined"]["band"] == want_band


def test_synthetic_docs_satisfy_the_real_verifier_contracts():
    """The stand-in docs must be structurally the real thing, or the dry-run
    proves nothing about the paid path — including for the 60 new pairs."""
    corpus = load_corpus()
    bank = synthetic_doc_bank(corpus)
    assert len(bank) == corpus["n_pairs"] == 80
    for pair in corpus["pairs"]:
        entry = bank[pair["pair_id"]]
        for doc_type in ("x", "y_completing", "y_null"):
            assert verify_doc(entry[doc_type], doc_type, pair) == [], \
                f"{pair['pair_id']}/{doc_type}"


# --- the scopes (D4's three rows) --------------------------------------------

def test_the_two_scopes_partition_the_corpus():
    assert len(ORIGINAL_PAIR_IDS) == N_ORIGINAL == 20
    assert len(EXTENSION_PAIR_IDS) == N_EXTENSION == 60
    assert not (ORIGINAL_PAIR_IDS & EXTENSION_PAIR_IDS)
    assert len(ORIGINAL_PAIR_IDS | EXTENSION_PAIR_IDS) == N_CLEAN_REQUIRED_M1C


def test_combined_row_is_exactly_original_plus_extension():
    """The pooling has to be additive, or "combined" means something the brief
    did not pre-register."""
    original = synthetic_rows("b", ORIGINAL_PAIR_IDS, 2)
    extension = synthetic_rows("b", EXTENSION_PAIR_IDS, 4)
    sv = surface_verdict(original, extension)
    rows = sv["rows"]
    for cell in (BASE_CELL, ARM_CELL):
        assert (rows["combined"]["clean"][cell]
                == rows["original"]["clean"][cell]
                + rows["extension_only"]["clean"][cell])
        assert (rows["combined"]["dg"][cell]
                == rows["original"]["dg"][cell]
                + rows["extension_only"]["dg"][cell])


def test_every_rendering_carries_all_three_rows():
    sv = surface_verdict(synthetic_rows("a", ORIGINAL_PAIR_IDS, 0),
                         synthetic_rows("a", EXTENSION_PAIR_IDS, 0))
    assert set(sv["rows"]) == {"original", "extension_only", "combined"}
    for r in sv["rows"].values():
        assert r["band"] in TEMPLATES
        assert r["statement"]


def test_disagreeing_rows_carry_both_statements_extension_only_first():
    """D1: the disagreement is reported, never averaged away."""
    sv = surface_verdict(synthetic_rows("b", ORIGINAL_PAIR_IDS, 0),
                         synthetic_rows("b", EXTENSION_PAIR_IDS, 4))
    assert sv["rows"]["extension_only"]["band"] == "T3"
    assert sv["rows"]["combined"]["band"] == "T2"
    assert sv["template_disagreement"] is True
    assert sv["statements_to_carry"] == ["extension_only", "combined"]


def test_agreeing_rows_carry_the_combined_statement_only():
    sv = surface_verdict(synthetic_rows("a", ORIGINAL_PAIR_IDS, 0),
                         synthetic_rows("a", EXTENSION_PAIR_IDS, 0))
    assert sv["rows"]["extension_only"]["band"] == sv["rows"]["combined"]["band"]
    assert sv["template_disagreement"] is False
    assert sv["statements_to_carry"] == ["combined"]


# --- the power gate: M1's threshold is NOT inherited (D3) --------------------

def _rows(cell, label, n, dg=False):
    return [{"pair_id": f"px{i}", "cell": cell, "model": MODEL, "ok": True,
             "scored": {"label": label, "dg": dg, "dg_any": False,
                        "faithfulness": "PASS", "citation": "PASS"}}
            for i in range(n)]


def _at(clean_base, clean_arm, dg_arm=0):
    """A surface whose combined scope holds exactly these clean counts."""
    original = (_rows(BASE_CELL, "correct-refusal", clean_base)
                + _rows(ARM_CELL, "DG", dg_arm, dg=True)
                + _rows(ARM_CELL, "correct-refusal", clean_arm - dg_arm))
    return surface_verdict(original, [])


def test_seventy_nine_clean_is_underpowered_however_large_the_effect():
    """The failure mode D3 exists for: M1's fixed N_CLEAN_REQUIRED = 20 would
    have called this powered and rendered a verdict sized for nothing."""
    sv = _at(79, 79, dg_arm=40)
    assert sv["verdict"] == "UNDERPOWERED"
    assert sv["powered"] is False
    assert sv["newcombe_delta_combined"]["excludes_zero"] is True
    assert sv["shortfall"] == {BASE_CELL: 1, ARM_CELL: 1}


def test_exactly_eighty_clean_is_powered():
    assert _at(80, 80, dg_arm=40)["verdict"] == "DG-EFFECT"


def test_power_requires_both_gated_cells():
    assert _at(80, 79, dg_arm=40)["verdict"] == "UNDERPOWERED"
    assert _at(79, 80, dg_arm=40)["verdict"] == "UNDERPOWERED"


def test_a_powered_null_reports_its_wilson_upper():
    sv = _at(80, 80, dg_arm=0)
    assert sv["verdict"] == "NULL"
    w = sv["rows"]["combined"]["primary"]["wilson"]
    assert w["lo"] == 0.0 and 0.045 < w["hi"] < 0.047   # 0/80 -> 4.6%


def test_shortfall_is_stated_not_merely_flagged():
    sv = _at(40, 30)
    assert sv["shortfall"] == {BASE_CELL: 40, ARM_CELL: 50}


# --- the templates (D4 / D21) -------------------------------------------------

FORBIDDEN = ["consistent with", "contradicts", "contradict the",
             "replicates", "p-value", "p =", "p<", "p <"]


@pytest.mark.parametrize("t", sorted(TEMPLATES))
def test_no_template_uses_a_forbidden_verb(t):
    """D4/D21: no p-value against any paper cell, no consistent-with /
    contradicts / replicates verb, no point comparison."""
    text = TEMPLATES[t].lower()
    for phrase in FORBIDDEN:
        assert phrase not in text, (t, phrase)


@pytest.mark.parametrize("t", sorted(TEMPLATES))
def test_every_template_carries_its_caveats_inline(t):
    """The PR #10 review-F9 failure mode: a downstream rendering that drops the
    three qualifications deciding the verb. They cannot be dropped if they are
    inside the only permitted string."""
    text = TEMPLATES[t]
    assert "not a replication claim" in text
    assert "not a contradiction claim" in text
    if t != "T0":
        assert "different condition by definition" in text
        assert "lower bound" in text
        assert "schema we did not run" in text


def test_rendered_statements_fill_their_own_row_numbers():
    t, s = render_template(6, 80)
    assert t == "T3"
    assert "6/80" in s and "3.5%" in s and "15.4%" in s
    t0, s0 = render_template(0, 20)
    assert t0 == "T0"
    assert "0/20" in s0 and "16.1%" in s0
    assert "N=80" not in s0   # PR #11 review F12: no hardcoded N survives


@pytest.mark.parametrize("k,n", [(0, 20), (0, 80), (2, 80), (6, 80), (22, 80)])
def test_no_rendered_statement_has_an_unfilled_placeholder(k, n):
    """One (k, n) per band, so every template string is actually rendered."""
    t, s = render_template(k, n)
    assert "{" not in s and "}" not in s, t
    assert f"{k}/{n}" in s


# --- log ingestion ------------------------------------------------------------

def test_load_restricts_to_the_model_and_the_pair_scope(tmp_path):
    p = tmp_path / "wave.jsonl"
    p.write_text("".join(json.dumps(r) + "\n" for r in [
        {"pair_id": "p01", "cell": ARM_CELL, "model": MODEL, "ok": True},
        {"pair_id": "p21", "cell": ARM_CELL, "model": MODEL, "ok": True},
        {"pair_id": "p02", "cell": ARM_CELL, "model": "other/model", "ok": True},
    ]))
    assert {r["pair_id"] for r in _load(p)} == {"p01", "p21"}
    assert {r["pair_id"] for r in _load(p, ORIGINAL_PAIR_IDS)} == {"p01"}
    assert {r["pair_id"] for r in _load(p, EXTENSION_PAIR_IDS)} == {"p21"}


def test_load_prefers_the_ok_row_and_never_rerolls_a_scored_one(tmp_path):
    p = tmp_path / "wave.jsonl"
    p.write_text("".join(json.dumps(r) + "\n" for r in [
        {"pair_id": "p21", "cell": ARM_CELL, "model": MODEL, "ok": False,
         "error": "boom"},
        {"pair_id": "p21", "cell": ARM_CELL, "model": MODEL, "ok": True,
         "answer": "first"},
        {"pair_id": "p21", "cell": ARM_CELL, "model": MODEL, "ok": True,
         "answer": "second"},
    ]))
    rows = _load(p)
    assert len(rows) == 1 and rows[0]["answer"] == "first"


def test_the_committed_m1_logs_supply_the_original_rows():
    """The combined estimand pools M1's recorded trials, so they have to be
    readable at this model and this scope. These are M1's published numbers
    (Decisions.md D10), not a pre-verdict aggregation of M1C data."""
    from m1c import M1_WAVE_PATH
    for arm, dg_expected in (("a", 0), ("b", 2)):
        rows = _load(M1_WAVE_PATH[arm], ORIGINAL_PAIR_IDS)
        cells = scope_counts(rows)
        assert cells[BASE_CELL]["clean"] == 20
        assert cells[ARM_CELL]["clean"] == 20
        assert cells[ARM_CELL]["dg"] == dg_expected


def test_vague_is_excluded_from_the_clean_denominator():
    cells = scope_counts(_rows(ARM_CELL, "DG", 5, dg=True)
                         + _rows(ARM_CELL, "vague", 3))
    assert cells[ARM_CELL]["n"] == 8
    assert cells[ARM_CELL]["clean"] == 5 and cells[ARM_CELL]["dg"] == 5


def test_errors_are_counted_but_never_clean():
    rows = _rows(ARM_CELL, "DG", 4, dg=True) + [
        {"pair_id": "pe", "cell": ARM_CELL, "model": MODEL, "ok": False,
         "error": "boom"}]
    cells = scope_counts(rows)
    assert cells[ARM_CELL]["n"] == 5 and cells[ARM_CELL]["n_err"] == 1
    assert cells[ARM_CELL]["clean"] == 4


def test_cells_outside_the_m1c_factorial_are_ignored():
    rows = _rows(ARM_CELL, "DG", 1, dg=True) + _rows("completexcompleting",
                                                     "DG", 1, dg=True)
    cells = scope_counts(rows)
    assert set(cells) == {BASE_CELL, ARM_CELL}
    assert cells[ARM_CELL]["n"] == 1


# --- pre-committed constants (D1, D3, D6) ------------------------------------

def test_scope_is_one_model_and_both_surfaces():
    assert MODEL == "qwen/qwen-2.5-7b-instruct"
    assert M1C_CELLS == [("absent", "null_control"), ("absent", "completing")]


def test_n_clean_required_is_eighty_not_m1s_twenty():
    from m1 import N_CLEAN_REQUIRED as M1_THRESHOLD
    assert N_CLEAN_REQUIRED_M1C == 80
    assert M1_THRESHOLD == 20
    assert N_CLEAN_REQUIRED_M1C != M1_THRESHOLD


def test_caps_are_the_brief_d6_ceiling():
    assert CAP_M1C_TOTAL == 0.10
    assert CAP_GEN_DOCS + CAP_SMOKE * 2 + sum(CAP_WAVE.values()) > CAP_M1C_TOTAL


def test_open_meter_clamps_to_what_remains_of_the_total(tmp_path, monkeypatch):
    import m1c
    monkeypatch.setattr(m1c, "SPEND_PATH", tmp_path / "spend.json")
    assert m1c.open_meter(0.06).cap == 0.06
    m1c.record_spend("gen-docs", None, 0.08)
    assert m1c.open_meter(0.06).cap == pytest.approx(0.02)
    m1c.record_spend("wave", "a", 0.02)
    with pytest.raises(SystemExit):
        m1c.open_meter(0.02)


def test_budget_exceeded_escapes_run_trial_instead_of_becoming_an_error_row():
    import client
    import m1c
    pair = {"pair_id": "p21", "question": "q",
            "x": {"name": "A", "tokens": {}}, "y": {"name": "B", "tokens": {}}}
    docs_all = {"p21": {"x": "x", "y_completing": "yc", "y_null": "yn"}}
    with pytest.raises(client.BudgetExceeded):
        m1c._run_trial("a", pair, "absent", "completing", docs_all, None,
                       client.CostMeter(0.0))


def test_ordinary_call_failures_still_become_error_rows(monkeypatch):
    import client
    import m1c

    def boom(*a, **k):
        raise ConnectionError("transient")

    monkeypatch.setattr(client, "chat", boom)
    pair = {"pair_id": "p21", "question": "q",
            "x": {"name": "A", "tokens": {}}, "y": {"name": "B", "tokens": {}}}
    row = m1c._run_trial("a", pair, "absent", "completing",
                         {"p21": {"x": "x", "y_completing": "yc", "y_null": "yn"}},
                         None, client.CostMeter(1.0))
    assert row["ok"] is False and row["error"].startswith("ConnectionError")


def test_usable_docs_excludes_partially_generated_pairs(tmp_path, monkeypatch):
    import m1c
    p = tmp_path / "docs.json"
    p.write_text(json.dumps({
        "p21": {"x": "a", "y_completing": "b", "y_null": "c"},
        "p22": {"x": "a", "y_completing": "b"},              # y_null failed
        "p23": {"x": "a", "y_completing": "b", "y_null": ""},  # empty
    }))
    monkeypatch.setattr(m1c, "DOCS_PATH", p)
    assert set(m1c._usable_docs()) == {"p21"}


# --- pooling preconditions (D5) ----------------------------------------------

def test_pooling_precondition_rejects_a_drifted_m1_doc(tmp_path, monkeypatch):
    import m1c
    real = json.loads(m1c.DOCS_M1_PATH.read_text())
    tampered = dict(real)
    tampered["p01"] = {**real["p01"], "x": "REWRITTEN"}
    with pytest.raises(SystemExit):
        m1c._assert_pooling_preconditions(tampered, "test")


def test_pooling_precondition_passes_on_the_committed_tree():
    import m1c
    m1c._assert_pooling_preconditions(when="test")


# --- frozen-record protection, carried forward (PR #12 review F2's note) -----

def test_m1c_scope_is_pinned_not_read_from_the_live_pool():
    """M1C's own scope is a pre-registered fact. Reading `corpus.N_PAIRS` here
    would let a later milestone's corpus growth redefine what "the extension"
    means — the exact coupling that broke `m1.py` when M1C grew the pool."""
    import corpus
    import m1c
    assert m1c.N_PAIRS_M1C == 80
    assert N_EXTENSION == 60 and N_ORIGINAL == 20
    assert max(EXTENSION_PAIR_IDS) == "p80"
    corpus.N_PAIRS  # still 80 today; the point is that nothing above reads it


def test_m1c_verdict_refuses_to_rewrite_itself_against_a_grown_corpus(monkeypatch):
    import corpus
    import m1c
    monkeypatch.setattr(corpus, "N_PAIRS", 120)
    with pytest.raises(SystemExit):
        m1c.cmd_verdict(None)


def test_the_published_m1c_verdict_re_derives_from_the_committed_logs():
    """PR #12 review F5, taken up here because the guard above makes
    re-rendering impossible after a future corpus growth: the published
    artifact must stay derivable from the logs it was rendered from. A pure
    re-derivation, no network — and not a second "look", since these numbers
    are already published (D24)."""
    import m1c
    published = json.loads(m1c.VERDICT_PATH.read_text())["surfaces"]
    for arm in sorted(m1c.ARMS):
        derived = surface_verdict(
            _load(m1c.M1_WAVE_PATH[arm], ORIGINAL_PAIR_IDS),
            _load(m1c.WAVE_PATH[arm], EXTENSION_PAIR_IDS))
        assert derived == published[arm], arm
