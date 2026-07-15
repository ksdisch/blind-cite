"""Controlled-retrieval assembler (M0-BRIEF D4): cell composition + determinism."""
import pytest

from assemble import CELLS, assemble

PAIR = {"pair_id": "p99",
        "x": {"name": "Vexalith"}, "y": {"name": "Vexonor"}}
DOCS = {"x": "X-DOC", "y_completing": "Y-COMPLETING", "y_null": "Y-NULL"}


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
