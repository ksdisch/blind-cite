"""Detector fidelity (M0-BRIEF D6/D7): extraction edge cases, the doc
verifier, and the committed hand-labeled gate — 100% required before any paid
run."""
import json
from pathlib import Path

import pytest

from detectors import classify, extract_tokens, verify_doc

HANDLABELED = json.loads(
    (Path(__file__).parent / "data" / "handlabeled.json").read_text())


# --- extraction edges -------------------------------------------------------

def test_extracts_all_four_categories():
    text = ("Call vxl_resume_stream() with vxl.checkpoint_guard; "
            "VXL-E203 since version 2.7.4.")
    assert extract_tokens(text) == {
        "vxl_resume_stream", "vxl.checkpoint_guard", "VXL-E203", "2.7.4"}


def test_method_parens_and_bare_are_same_token():
    assert extract_tokens("vxn_restart_transfer()") == \
        extract_tokens("vxn_restart_transfer")


def test_version_v_prefix_canonicalizes():
    assert extract_tokens("shipped in v3.9.2 today") == {"3.9.2"}


def test_version_maximal_match_not_substring():
    assert extract_tokens("in version 3.9.21 of it") == {"3.9.21"}


def test_no_match_inside_longer_identifiers():
    assert extract_tokens("call myvxl_resume_stream please") == set()
    assert extract_tokens("vxl_resume_stream_extra") == set()


def test_ip_like_quad_is_not_a_version():
    assert extract_tokens("served from 10.0.3.4 always") == set()


# --- doc verifier (D5) ------------------------------------------------------

@pytest.fixture(scope="module")
def pair():
    return HANDLABELED["pair"]


def test_fixture_docs_pass_their_contracts(pair):
    docs = HANDLABELED["docs"]
    assert verify_doc(docs["x_doc"], "x", pair) == []
    assert verify_doc(docs["y_completing"], "y_completing", pair) == []
    assert verify_doc(docs["y_null"], "y_null", pair) == []


def test_verifier_rejects_forbidden_name(pair):
    leaky = HANDLABELED["docs"]["y_completing"] + " Vexalith users take note."
    assert any("forbidden name" in v
               for v in verify_doc(leaky, "y_completing", pair))


def test_verifier_rejects_stray_token_in_null_doc(pair):
    leaky = HANDLABELED["docs"]["y_null"] + " Try abc_load_file() sometime."
    assert any("extra token-shaped" in v
               for v in verify_doc(leaky, "y_null", pair))


def test_verifier_rejects_missing_token(pair):
    partial = HANDLABELED["docs"]["y_completing"].replace("VXN-E415", "an error")
    assert any("missing tokens" in v
               for v in verify_doc(partial, "y_completing", pair))


# --- the hand-labeled gate --------------------------------------------------

def _case_docs(case):
    return [{"doc_id": f"doc{i + 1}", "text": HANDLABELED["docs"][key]}
            for i, key in enumerate(case["docs"])]


@pytest.mark.parametrize(
    "case", HANDLABELED["cases"], ids=[c["id"] for c in HANDLABELED["cases"]])
def test_hand_labeled(case, pair):
    got = classify(case["answer"], pair, _case_docs(case))
    for key, want in case["expect"].items():
        assert got[key] == want, (
            f"{case['id']}: {key} = {got[key]!r}, expected {want!r} "
            f"(rationale: {case['rationale']})")


# --- the M1 detector split (M1-BRIEF D2 amended) ----------------------------
#
# misattributed-other = (T & R) - X - Y   |   confabulation = T - X - Y - R
# The two partition M0's `unowned`; the rung sits below discriminated and above
# confabulation. These unit tests pin the boundary the fidelity set exercises
# end-to-end in data/handlabeled_m1.json.

FILLER = ("The Kroaris library batches ledger writes. Call kro_batch_ledger() "
          "with kro.tiered_fence enabled; Kroaris raises KRO-E311 on overflow. "
          "Added in Kroaris version 5.2.0.")
OWNERS = {"kro_batch_ledger": {"name": "Kroaris", "pair_id": "pf1", "role": "x"},
          "kro.tiered_fence": {"name": "Kroaris", "pair_id": "pf1", "role": "x"},
          "KRO-E311": {"name": "Kroaris", "pair_id": "pf1", "role": "x"},
          "5.2.0": {"name": "Kroaris", "pair_id": "pf1", "role": "x"}}


def _docs_with_filler():
    return [{"doc_id": "doc1", "text": HANDLABELED["docs"]["y_null"]},
            {"doc_id": "doc2", "text": FILLER}]


def test_retrieved_third_party_token_is_misattributed_not_confabulation(pair):
    """The whole reason the split is required: under M0's pair-scoped rule this
    answer would score `confabulation` and the faithfulness proxy would be
    contradicted by its own soundness argument."""
    got = classify("Call kro_batch_ledger() to do this [doc2].", pair,
                   _docs_with_filler(), OWNERS)
    assert got["label"] == "misattributed-other"
    assert got["dg_any"] is True and got["confab"] is False
    assert got["misattributed_other_tokens"] == ["kro_batch_ledger"]
    assert got["confabulated_tokens"] == []
    assert got["faithfulness"] == "PASS"  # it IS in a retrieved doc
    assert got["other_owner_named"] is False


def test_misattributed_records_owner_named(pair):
    got = classify("Kroaris provides kro_batch_ledger() [doc2].", pair,
                   _docs_with_filler(), OWNERS)
    assert got["label"] == "misattributed-other"
    assert got["other_owner_named"] is True
    assert got["other_owner_names"] == ["Kroaris"]


def test_unretrieved_token_is_confabulation_even_if_globally_owned(pair):
    """Ownership does not excuse a token the retrieval never supplied — the
    model could not have read it."""
    got = classify("Call kro_batch_ledger() to do this.", pair,
                   [{"doc_id": "doc1", "text": HANDLABELED["docs"]["y_null"]}],
                   OWNERS)
    assert got["label"] == "confabulation"
    assert got["confab"] is True and got["dg_any"] is False
    assert got["faithfulness"] == "FAIL"


def test_dg_y_outranks_misattributed_other(pair):
    docs = [{"doc_id": "doc1", "text": HANDLABELED["docs"]["y_completing"]},
            {"doc_id": "doc2", "text": FILLER}]
    got = classify("Use vxn_restart_transfer() and kro.tiered_fence [doc1].",
                   pair, docs, OWNERS)
    assert got["label"] == "DG"          # precedence 1 still wins
    assert got["dg"] is True and got["dg_any"] is True
    assert got["misattributed_other_tokens"] == ["kro.tiered_fence"]


def test_split_partitions_m0_unowned_exactly(pair):
    """No token may fall through the precedence table."""
    docs = _docs_with_filler()
    answer = ("Try kro_batch_ledger() and also abc_made_up() with "
              "xyz.invented_flag [doc2].")
    got = classify(answer, pair, docs, OWNERS)
    assert (set(got["misattributed_other_tokens"])
            | set(got["confabulated_tokens"])) == set(got["unowned_tokens"])
    assert not (set(got["misattributed_other_tokens"])
                & set(got["confabulated_tokens"]))


def test_owners_map_is_optional(pair):
    """The split is pure set algebra; only owner *naming* needs the map."""
    got = classify("Call kro_batch_ledger() [doc2].", pair, _docs_with_filler())
    assert got["label"] == "misattributed-other"
    assert got["other_owner_names"] == [] and got["other_owner_named"] is False


# --- M0 non-regression: the split must not move any recorded M0 result ------

def test_m0_pilot_rescores_identically():
    """M1-BRIEF D2 claims 'under M0's no-filler design unowned & R is empty, so
    the narrowed confabulation coincides with M0's and M0's recorded results are
    untouched'. This re-scores all 144 committed M0 trials against the frozen M0
    fixtures and holds that claim to it — the guard on which M0's FIT verdict
    stays re-verifiable from the working tree."""
    from assemble import assemble

    root = Path(__file__).parent
    corpus = {p["pair_id"]: p for p in
              json.loads((root / "data" / "corpus_m0.json").read_text())["pairs"]}
    docs_all = json.loads((root / "data" / "docs_m0.json").read_text())
    rows = [json.loads(line) for line
            in (root / "data" / "pilot.jsonl").read_text().splitlines()]

    n_checked = 0
    for r in rows:
        if not r.get("ok"):
            continue
        n_checked += 1
        pair = corpus[r["pair_id"]]
        cx, cy = r["cell"].split("x", 1)
        docs = assemble(pair, cx, cy, docs_all[r["pair_id"]])
        got = classify(r["answer"], pair, docs)
        for key, want in r["scored"].items():
            assert got[key] == want, (
                f"{r['pair_id']}/{r['cell']}/{r['model']}: {key} moved — "
                f"committed {want!r}, now {got[key]!r}")
    assert n_checked == 144
