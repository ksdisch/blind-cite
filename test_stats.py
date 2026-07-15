"""Wilson/Newcombe sanity (values cross-checked against the lineage suites)."""
import pytest

from stats import excludes_zero, newcombe_diff, wilson


def test_wilson_zero_of_twenty_reads_consistent_with_zero():
    lo, hi = wilson(0, 20)
    assert lo == 0.0
    assert 0.15 < hi < 0.17  # ~16%: "consistent with ~0%", never "proved 0%"


def test_wilson_edges_stay_in_unit_interval():
    for k, n in [(0, 1), (1, 1), (20, 20), (10, 20)]:
        lo, hi = wilson(k, n)
        assert 0.0 <= lo <= k / n <= hi <= 1.0


def test_wilson_no_data_is_the_whole_range():
    assert wilson(0, 0) == (0.0, 1.0)


def test_wilson_shrinks_toward_half():
    lo, hi = wilson(18, 20)
    assert (lo + hi) / 2 < 0.9  # centre pulled below the raw 90%


def test_newcombe_clear_effect_excludes_zero():
    d, lo, hi = newcombe_diff(2, 20, 16, 20)
    assert d == pytest.approx(0.7)
    assert excludes_zero(lo, hi)


def test_newcombe_no_effect_straddles_zero():
    d, lo, hi = newcombe_diff(10, 20, 11, 20)
    assert not excludes_zero(lo, hi)


def test_newcombe_sign_convention():
    d, lo, hi = newcombe_diff(16, 20, 2, 20)  # arm LOWER than base
    assert d == pytest.approx(-0.7)
    assert hi < 0.0 and excludes_zero(lo, hi)


def test_excludes_zero_boundary_is_not_a_claim():
    assert not excludes_zero(0.0, 0.5)
    assert not excludes_zero(-0.5, 0.0)
