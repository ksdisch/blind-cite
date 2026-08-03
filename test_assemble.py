"""Controlled-retrieval assembler: cell composition + determinism on the stark
surface (M0-BRIEF D4) and on the M1b camouflage surface (M1-BRIEF D2)."""
import pytest

from assemble import (CELLS, CONSTANT_TITLE, K_FILLER, assemble,
                      assemble_camouflaged, filler_pair_ids)

PAIR = {"pair_id": "p99",
        "x": {"name": "Vexalith"}, "y": {"name": "Vexonor"}}
DOCS = {"x": "X-DOC", "y_completing": "Y-COMPLETING", "y_null": "Y-NULL"}

# A doc bank shaped like data/docs.json: pair_id -> {x, y_completing, y_null}.
BANK = {"p99": DOCS} | {
    f"p{i:02d}": {"x": f"X-DOC-{i}", "y_completing": f"YC-{i}",
                  "y_null": f"YN-{i}"}
    for i in range(1, 21)}


def texts(docs):
    return sorted(d["text"] for d in docs)


def test_cell_composition():
    assert texts(assemble(PAIR, "absent", "null_control", DOCS)) == ["Y-NULL"]
    assert texts(assemble(PAIR, "absent", "completing", DOCS)) == ["Y-COMPLETING"]
    assert texts(assemble(PAIR, "complete", "null_control", DOCS)) == ["X-DOC", "Y-NULL"]
    assert texts(assemble(PAIR, "complete", "completing", DOCS)) == ["X-DOC", "Y-COMPLETING"]


def test_doc_ids_sequential_after_shuffle():
    for cx, cy in CELLS:
        docs = assemble(PAIR, cx, cy, DOCS)
        assert [d["doc_id"] for d in docs] == [f"doc{i + 1}" for i in range(len(docs))]


def test_deterministic_order():
    a = assemble(PAIR, "complete", "completing", DOCS)
    b = assemble(PAIR, "complete", "completing", DOCS)
    assert a == b


def test_unknown_cell_rejected():
    with pytest.raises(ValueError):
        assemble(PAIR, "partial", "completing", DOCS)


def test_stark_surface_titles_are_entity_name_forward():
    """M0's surface, unchanged — this is exactly what M1b camouflages, and M1a
    depends on it NOT moving."""
    docs = assemble(PAIR, "absent", "completing", DOCS)
    assert docs[0]["title"] == "Vexonor reference"


# --- M1b camouflage surface (M1-BRIEF D2) -----------------------------------

def _cam(cy, cx="absent"):
    return assemble_camouflaged(PAIR, cx, cy, BANK)


def test_camouflaged_set_length_is_cell_docs_plus_k_filler():
    for cy in ("null_control", "completing"):
        assert len(_cam(cy)) == 1 + K_FILLER
    assert len(_cam("completing", cx="complete")) == 2 + K_FILLER


def test_every_camouflaged_title_is_the_constant():
    """Title-leak trap: a renderer that reintroduces per-doc titles re-arms the
    stark surface silently. No entity name may appear in any title."""
    for cy in ("null_control", "completing"):
        for d in _cam(cy):
            assert d["title"] == CONSTANT_TITLE
            assert "Vexonor" not in d["title"]
            assert "Vexalith" not in d["title"]


def test_filler_assignment_identical_across_the_two_cells():
    """The cell contrast must be attributable to the Y-doc alone."""
    a = [d["text"] for d in _cam("null_control")]
    b = [d["text"] for d in _cam("completing")]
    assert set(a) - {"Y-NULL"} == set(b) - {"Y-COMPLETING"}


def test_y_doc_holds_the_same_position_in_both_cells():
    """Pair-seeded shuffle: position is held constant across the contrast, not
    merely randomized within it."""
    pos_null = [d["text"] for d in _cam("null_control")].index("Y-NULL")
    pos_comp = [d["text"] for d in _cam("completing")].index("Y-COMPLETING")
    assert pos_null == pos_comp


def test_fillers_are_other_pairs_x_docs_only():
    texts = {d["text"] for d in _cam("completing")}
    fillers = texts - {"Y-COMPLETING"}
    assert all(t.startswith("X-DOC-") for t in fillers)
    assert "X-DOC" not in texts, "the queried pair's own X-doc is absent-Cx"


def test_filler_never_draws_the_pair_itself():
    for pid in BANK:
        assert pid not in filler_pair_ids(pid, BANK.keys())


def test_filler_selection_is_deterministic_and_pair_seeded():
    assert filler_pair_ids("p99", BANK.keys()) == filler_pair_ids("p99", BANK.keys())
    assert filler_pair_ids("p01", BANK.keys()) != filler_pair_ids("p02", BANK.keys())


def test_camouflaged_doc_ids_sequential_and_deterministic():
    docs = _cam("completing")
    assert [d["doc_id"] for d in docs] == [f"doc{i + 1}" for i in range(len(docs))]
    assert docs == _cam("completing")


def test_camouflaged_rejects_unknown_cell():
    with pytest.raises(ValueError):
        assemble_camouflaged(PAIR, "partial", "completing", BANK)


def test_filler_needs_enough_other_pairs():
    with pytest.raises(ValueError):
        filler_pair_ids("p99", ["p99", "p01"])
