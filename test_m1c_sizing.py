"""test_m1c_sizing.py — pins docs/M1C-BRIEF.md D2's sizing table to stats.wilson.

The pre-registration's power table is asserted here so it cannot drift from the
function that defines it (PR #11 review F1/F8: one hand-built row was wrong and
no committed derivation existed to catch it). Pure logic, no network.
"""
from stats import wilson

FLOOR = 0.14


def band(k: int, n: int) -> str:
    """Template band for k events in n trials (docs/M1C-BRIEF.md D4)."""
    lo, hi = wilson(k, n)
    if k == 0:
        return "T1" if hi < FLOOR else "T0"
    if hi < FLOOR:
        return "T2"
    if lo > FLOOR:
        return "T4"
    return "T3"


def test_zero_k_uppers():
    # "0/N Wilson upper" column of the D2 table
    for n, upper in [(20, 0.161), (24, 0.138), (60, 0.060), (80, 0.046), (120, 0.031)]:
        assert abs(wilson(0, n)[1] - upper) < 0.0005, n


def test_smallest_n_clearing_the_floor_is_24():
    assert wilson(0, 23)[1] >= FLOOR
    assert wilson(0, 24)[1] < FLOOR


def test_band_boundaries():
    # "T2 band" and "T3 starts at" columns of the D2 table
    for n, t2_max, t3_first in [(60, 3, 4), (80, 5, 6), (120, 9, 10)]:
        assert band(t2_max, n) == "T2", n
        assert band(t3_first, n) == "T3", n
    # at N=20 and N=24 the T2 band is empty: k=1 already reaches the floor
    assert band(1, 20) == "T3"
    assert band(1, 24) == "T3"


def test_zero_k_bands():
    # T0 (zero with an interval reaching the floor) fires only at the original
    # N=20 rows; every candidate combined/extension N gives a real T1
    assert band(0, 20) == "T0"
    for n in (24, 60, 80, 120):
        assert band(0, n) == "T1", n


def test_point_estimates():
    # the parenthesized k/N percentages of the D2 table (the column PR #11
    # review F1 caught wrong; asserted per its F13)
    for k, n, pct in [(1, 20, 5.0), (1, 24, 4.2), (4, 60, 6.7), (6, 80, 7.5), (10, 120, 8.3)]:
        assert abs(100 * k / n - pct) < 0.05, (k, n)


def test_bands_partition_every_reachable_k():
    # D4: exactly one template fires per data row
    for n in (20, 24, 60, 80, 120):
        for k in range(0, n + 1):
            assert band(k, n) in {"T0", "T1", "T2", "T3", "T4"}


def test_sensitivity_case_is_t4():
    # D2: sized against ~28% → expected k ≈ 22/80 sits entirely above the floor
    lo, _hi = wilson(22, 80)
    assert lo > FLOOR
    assert band(22, 80) == "T4"


def test_power_closed_form():
    # D2: Wilson lower bound > 0 iff k >= 1, so P(lo > 0) = 1 - (1-p)^N exactly
    assert wilson(0, 80)[0] == 0.0
    assert wilson(1, 80)[0] > 0.0
    assert abs((1 - (1 - 0.10) ** 80) - 0.9998) < 0.0001
    assert abs((1 - (1 - 0.05) ** 80) - 0.9835) < 0.0001
