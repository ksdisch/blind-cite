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
