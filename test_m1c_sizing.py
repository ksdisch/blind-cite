"""test_m1c_sizing.py — pins docs/M1C-BRIEF.md D2's sizing table to stats.wilson.

The pre-registration's power table is asserted here so it cannot drift from the
function that defines it (PR #11 review F1/F8: one hand-built row was wrong and
no committed derivation existed to catch it). Pure logic, no network.
"""
from m1c import FLOOR, band
from stats import wilson

# `band` is imported from the script that RENDERS the verdict, not re-declared
# here. A second copy would let the pin stay green while the rendering path
# drifted, which is the opposite of what D2/D4 claim this file guarantees.


def test_zero_k_uppers():
    # "0/N Wilson upper" column of the D2 table
    for n, upper in [(20, 0.161), (24, 0.138), (60, 0.060), (80, 0.046), (120, 0.031)]:
        assert abs(wilson(0, n)[1] - upper) < 0.0005, n


def test_smallest_n_clearing_the_floor_is_24():
    assert wilson(0, 23)[1] >= FLOOR
    assert wilson(0, 24)[1] < FLOOR


def test_band_boundaries():
    # "T2 band" and "T3 starts at" columns of the D2 table. Both endpoints of
    # the T2 band are pinned: the lower one (k=1) as well as the upper, so the
    # written band "k=1-3" / "k=1-5" / "k=1-9" is asserted end to end rather
    # than resting on monotonicity of the Wilson upper (PR #11 review F13).
    for n, t2_max, t3_first in [(60, 3, 4), (80, 5, 6), (120, 9, 10)]:
        assert band(1, n) == "T2", n
        assert band(t2_max, n) == "T2", n
        assert band(t3_first, n) == "T3", n
    # at N=20 and N=24 the T2 band is empty: k=1 already reaches the floor
    assert band(1, 20) == "T3"
    assert band(1, 24) == "T3"


def test_zero_k_bands():
    # T0 (zero with an interval reaching the floor) fires at the original N=20
    # rows; every planned combined/extension N gives a real T1.
    assert band(0, 20) == "T0"
    for n in (24, 60, 80, 120):
        assert band(0, n) == "T1", n


def test_t0_is_also_reachable_on_a_budget_truncated_row():
    """PR #11 review F15: T0 is not exclusive to the original N=20 rows. The
    D3 truncation path can land a row at N <= 23, and 23 still reaches the
    floor — which is why no template's text may claim otherwise."""
    assert band(0, 23) == "T0"
    assert band(0, 24) == "T1"


def test_point_estimates():
    # the parenthesized k/N percentages of the D2 table (the column PR #11
    # review F1 caught wrong; asserted per its F13)
    for k, n, pct in [(1, 20, 5.0), (1, 24, 4.2), (4, 60, 6.7), (6, 80, 7.5), (10, 120, 8.3)]:
        assert abs(100 * k / n - pct) < 0.05, (k, n)


def test_bands_partition_every_reachable_k():
    """D4: exactly one template fires per data row.

    The five conditions are transcribed from D4's prose and evaluated against
    `stats.wilson` directly, NOT by calling `band()` — asserting `band()`'s
    output is a member of the set of literals `band()` is written from proves
    nothing (PR #11 review F16). Written this way the test can disagree with
    `band()`, and does if either drifts from the brief.
    """
    for n in (20, 23, 24, 60, 80, 120):
        for k in range(0, n + 1):
            lo, hi = wilson(k, n)
            holds = {
                "T0": k == 0 and hi >= FLOOR,                 # k=0, CI reaches 14%
                "T1": k == 0 and hi < FLOOR,                  # k=0, upper below 14%
                "T2": k >= 1 and hi < FLOOR,                  # excludes 0, upper < 14%
                "T3": k >= 1 and lo <= FLOOR <= hi,           # CI contains 14%
                "T4": k >= 1 and lo > FLOOR,                  # lower bound > 14%
            }
            fired = [t for t, ok in holds.items() if ok]
            assert len(fired) == 1, (k, n, fired)             # exhaustive + exclusive
            assert band(k, n) == fired[0], (k, n, fired)


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
