"""Dry-run of the M0 verdict logic on synthetic pilot rows — the verdict
machinery must be trusted before it renders on paid data (lineage discipline)."""
from assemble import CELLS, cell_id
from m0 import apply_triggers, funnel, m1_sizing


def _row(model, cell, label, grounded=True, ok=True):
    r = {"model": model, "cell": cell, "ok": ok, "pair_id": "px"}
    if ok:
        r["scored"] = {"label": label, "grounded": grounded}
    return r


def _model_rows(model, per_cell_labels):
    """per_cell_labels: {cell_id: [12 labels]}"""
    rows = []
    for (cx, cy) in CELLS:
        cid = cell_id(cx, cy)
        for label in per_cell_labels[cid]:
            grounded = label in ("DG", "discriminated", "correct-answer")
            rows.append(_row(model, cid, label, grounded=grounded))
    return rows


HEALTHY = {
    "absentxnull_control": ["correct-refusal"] * 8 + ["confabulation"] * 4,
    "absentxcompleting": ["DG"] * 7 + ["discriminated"] * 3 + ["correct-refusal"] * 2,
    "completexnull_control": ["correct-answer"] * 11 + ["vague"] * 1,
    "completexcompleting": ["correct-answer"] * 10 + ["DG"] * 2,
}


def test_healthy_model_survives():
    f = funnel(_model_rows("healthy", HEALTHY))
    v = apply_triggers(f)["healthy"]
    assert v["survives"] and not v["kills"] and not v["flags"]


def test_capability_cliff_killed_by_k1():
    labels = dict(HEALTHY)
    labels["completexnull_control"] = ["vague"] * 5 + ["confabulation"] * 7
    v = apply_triggers(funnel(_model_rows("cliff", labels)))["cliff"]
    assert not v["survives"]
    assert any(k.startswith("K1") for k in v["kills"])


def test_vague_model_killed_by_k2():
    labels = {cid: ["vague"] * 8 + ["correct-answer"] * 4
              for cid in [cell_id(*c) for c in CELLS]}
    v = apply_triggers(funnel(_model_rows("mumbler", labels)))["mumbler"]
    assert any(k.startswith("K2") for k in v["kills"])


def test_error_heavy_model_killed_by_k3():
    rows = _model_rows("flaky", HEALTHY)
    rows += [_row("flaky", "absentxcompleting", None, ok=False)] * 13
    v = apply_triggers(funnel(rows))["flaky"]
    assert any(k.startswith("K3") for k in v["kills"])


def test_right_reason_null_flagged_not_killed():
    labels = dict(HEALTHY)
    labels["absentxcompleting"] = (["correct-refusal"] * 7
                                   + ["discriminated"] * 4 + ["DG"] * 1)
    v = apply_triggers(funnel(_model_rows("skeptic", labels)))["skeptic"]
    assert v["survives"]
    assert any(f.startswith("K4") for f in v["flags"])


def test_m1_sizing_from_measured_funnel():
    f = funnel(_model_rows("healthy", HEALTHY))
    sizing = m1_sizing(f, ["healthy"])
    # absent cells are fully clean (no vague) -> 20 pairs needed
    assert sizing["healthy"]["absentxcompleting"] == 20
    assert sizing["pairs_needed"] == 20


def test_all_vague_cell_yields_no_sizing():
    labels = dict(HEALTHY)
    labels["absentxnull_control"] = ["vague"] * 12
    f = funnel(_model_rows("m", labels))
    sizing = m1_sizing(f, ["m"])
    assert sizing["m"]["absentxnull_control"] is None
