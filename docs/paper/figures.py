"""figures.py — render the paper's figures from the committed record.

Run:  uv run --with matplotlib docs/paper/figures.py     (from the repo root)

Deterministic and headless (matplotlib Agg): same data in, same PNGs out on any
re-run. No model, no network, no dependency added to the project manifest.

READS (all committed, read-only):
  data/m1c_verdict.json
  docs/paper/derived_contrasts.json   (written by docs/paper/derived_contrasts.py,
                                       which asserts every value in it against the
                                       committed record before writing anything)
WRITES:
  docs/paper/fig1-primary-estimand{,-dark}.png
  docs/paper/fig2-label-composition{,-dark}.png
  docs/paper/fig3-sizing{,-dark}.png

The figures
-----------
fig1  Primary estimand. DG-Y rate at `absent x completing` on
      qwen/qwen-2.5-7b-instruct, with its recorded Wilson 95% interval, at each
      of the three pre-committed scopes (original N=20 / extension-only N=60 /
      combined N=80), one panel per surface. The 14% reference magnitude and the
      pre-committed template each row fired are marked.
fig2  Outcome-label composition at the same cell: the share of clean trials
      scoring DG / discriminated / correct-refusal, per surface per scope. This
      is the D25 stage-heterogeneity picture — the engagement (non-refusal)
      share recorded for each stage is printed in the right margin.
fig3  Pre-registered sizing. The Wilson 95% upper bound on an observed 0/N, at
      the five combined-N values tabulated in docs/M1C-BRIEF.md D2, against the
      same 14% reference magnitude. The two N values this project actually ran
      are emphasised.

What this script computes, and what it does not
-----------------------------------------------
COMPUTES exactly one thing: a rate as `k / n`, from a recorded numerator over a
recorded denominator (the shares in fig2 and the point estimates in fig1). Every
other plotted value — every interval endpoint, every count, every Wilson upper
bound, every engagement percentage, the 14% floor, the template band — is lifted
verbatim from a committed file, via derived_contrasts.json where that file
asserts it against the record first.

DOES NOT compute: smoothing, interpolation, fitted or trend lines, error bars of
its own (fig1 plots the RECORDED Wilson intervals, not intervals this script
derived), pooling across any cell the repo did not pool, re-binning, or any value
read off an existing image. fig3's five points are drawn as discrete bars and are
deliberately NOT connected by a line: the repo records those five N values and no
curve between them.

Every plotted number is printed to stdout below, so the figures can be checked
against the paper's tables without opening a PNG.

Chart conventions follow the global `dataviz` skill: categorical slots assigned
in fixed order and validated with its `validate_palette.js` (3 slots, all-pairs,
both modes: ALL CHECKS PASS; the light-mode aqua contrast WARN is relieved by the
count tables the paper prints beside every figure). Light and dark variants are
separately stepped from the same ramps, not an automatic flip.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

ARM = "absentxcompleting"
SCOPES = [("original", "original  N=20"),
          ("extension_only", "extension-only  N=60"),
          ("combined", "combined  N=80")]
SURFACES = [("a", "Stark surface"), ("b", "Camouflaged surface")]
LABEL_ORDER = ["DG", "discriminated", "correct-refusal"]

# dataviz reference palette. Light | dark steps of the same ramps.
THEMES = {
    "light": dict(
        surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
        grid="#e1e0d9", baseline="#c3c2b7",
        s1="#2a78d6", s2="#eb6834", s3="#1baf7a", deemph="#b8b7b0",
    ),
    "dark": dict(
        surface="#1a1a19", ink="#ffffff", ink2="#c3c2b7", muted="#898781",
        grid="#2c2c2a", baseline="#383835",
        s1="#3987e5", s2="#d95926", s3="#199e70", deemph="#565654",
    ),
}
LABEL_SLOT = {"DG": "s1", "discriminated": "s2", "correct-refusal": "s3"}


def load() -> tuple[dict, dict]:
    with open(ROOT / "data" / "m1c_verdict.json") as fh:
        verdict = json.load(fh)
    with open(HERE / "derived_contrasts.json") as fh:
        derived = json.load(fh)
    return verdict, derived


def style(ax, t: dict) -> None:
    ax.set_facecolor(t["surface"])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=t["muted"], labelsize=9, length=0)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_color(t["ink2"])


# --------------------------------------------------------------------------- 1
def fig1(verdict: dict, derived: dict, mode: str) -> Path:
    t = THEMES[mode]
    floor = derived["floor_pct"]
    fig, axes = plt.subplots(2, 1, figsize=(9.2, 5.6), dpi=180, sharex=True)
    fig.patch.set_facecolor(t["surface"])

    for ax, (s, sname) in zip(axes, SURFACES):
        style(ax, t)
        colour = t["s1"] if s == "a" else t["s2"]
        ax.set_xlim(-0.4, 32)
        ax.set_ylim(-0.7, 2.7)
        ax.invert_yaxis()
        ax.xaxis.grid(True, color=t["grid"], linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)

        ax.axvline(floor, color=t["muted"], linewidth=1.5, zorder=1)

        ticks, ticklabels = [], []
        for i, (scope, scope_label) in enumerate(SCOPES):
            d = derived["primary"][f"{s}:{scope}"]
            ax.hlines(i, d["wilson_lo_pct"], d["wilson_hi_pct"],
                      color=colour, linewidth=2, zorder=3)
            ax.plot(d["rate_pct"], i, "o", markersize=8, color=colour,
                    markeredgecolor=t["surface"], markeredgewidth=2, zorder=4)
            ticks.append(i)
            ticklabels.append(f"{scope_label}   {d['k']}/{d['n']}")
            ax.annotate(d["band"], xy=(1.015, i),
                        xycoords=("axes fraction", "data"),
                        va="center", ha="left", fontsize=9,
                        color=t["ink"] if scope == "combined" else t["ink2"],
                        fontweight="bold" if scope == "combined" else "normal")
            if scope == "combined":
                ax.annotate(
                    f"[{d['wilson_lo_pct']:.1f}%, {d['wilson_hi_pct']:.1f}%]",
                    xy=(d["wilson_hi_pct"] + 0.8, i), va="center", ha="left",
                    fontsize=9, color=t["ink"])
        ax.set_yticks(ticks)
        ax.set_yticklabels(ticklabels)
        ax.set_title(sname, loc="left", fontsize=11, color=t["ink"],
                     fontweight="bold", pad=8)

    axes[0].annotate(f"{floor:.0f}%  nearest published cell\n(reference magnitude only)",
                     xy=(floor + 0.5, -0.62), fontsize=8.5, color=t["muted"],
                     va="top", ha="left")
    axes[0].annotate("template", xy=(1.015, -0.62),
                     xycoords=("axes fraction", "data"), fontsize=8.5,
                     color=t["muted"], va="top", ha="left")
    axes[1].set_xlabel("DG-Y rate at absent × completing (%), with the recorded "
                       "Wilson 95% interval", fontsize=9.5, color=t["ink2"])

    handles = [Line2D([0], [0], color=t["s1"], lw=2, marker="o", markersize=8,
                      markeredgecolor=t["surface"], markeredgewidth=2,
                      label="stark surface"),
               Line2D([0], [0], color=t["s2"], lw=2, marker="o", markersize=8,
                      markeredgecolor=t["surface"], markeredgewidth=2,
                      label="camouflaged surface")]
    leg = fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False,
                     fontsize=9, bbox_to_anchor=(0.5, -0.005))
    for txt in leg.get_texts():
        txt.set_color(t["ink2"])

    fig.tight_layout(rect=(0, 0.05, 0.90, 1))
    out = HERE / f"fig1-primary-estimand{'-dark' if mode == 'dark' else ''}.png"
    fig.savefig(out, facecolor=t["surface"], bbox_inches="tight")
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- 2
def fig2(verdict: dict, derived: dict, mode: str) -> Path:
    t = THEMES[mode]
    fig, ax = plt.subplots(figsize=(9.2, 4.6), dpi=180)
    fig.patch.set_facecolor(t["surface"])
    style(ax, t)
    ax.set_facecolor(t["surface"])

    rows = []  # (y, surface, scope)
    y = 0.0
    for s, sname in SURFACES:
        for scope, scope_label in SCOPES:
            rows.append((y, s, scope, scope_label))
            y += 1.0
        y += 0.6  # air between the two surface blocks

    gap = 0.14  # ≈2px of surface at this figure width — the separating spacer
    ticks, ticklabels = [], []
    for yy, s, scope, scope_label in rows:
        rec = derived["labels"][f"{s}:{scope}"]
        n = rec["n"]
        left = 0.0
        for name in LABEL_ORDER:
            count = rec["counts"].get(name, 0)
            if count == 0:
                continue
            width = 100.0 * count / n
            ax.barh(yy, width - gap, left=left + gap / 2, height=0.46,
                    color=t[LABEL_SLOT[name]], zorder=3)
            left += width
        ticks.append(yy)
        ticklabels.append(scope_label)
        eng = derived["engagement"].get(f"{s}:{scope}")
        ax.annotate(f"{eng['engagement_pct']:.0f}%" if eng else "—",
                    xy=(1.015, yy), xycoords=("axes fraction", "data"),
                    va="center", ha="left", fontsize=9,
                    color=t["ink"] if eng else t["muted"])

    ax.set_yticks(ticks)
    ax.set_yticklabels(ticklabels)
    ax.set_ylim(rows[-1][0] + 0.9, -0.9)
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0", "25%", "50%", "75%", "100%"])
    ax.xaxis.grid(True, color=t["grid"], linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel("share of clean trials at absent × completing", fontsize=9.5,
                  color=t["ink2"])

    for yy, s, _scope, _lbl in rows[:1]:
        pass
    ax.annotate("Stark surface", xy=(0, rows[0][0] - 0.75), fontsize=11,
                color=t["ink"], fontweight="bold", va="center")
    ax.annotate("Camouflaged surface", xy=(0, rows[3][0] - 0.75), fontsize=11,
                color=t["ink"], fontweight="bold", va="center")
    ax.annotate("engagement", xy=(1.015, rows[0][0] - 0.75),
                xycoords=("axes fraction", "data"), fontsize=8.5,
                color=t["muted"], va="center", ha="left")

    handles = [Patch(facecolor=t[LABEL_SLOT[n]], label=n) for n in LABEL_ORDER]
    leg = fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False,
                     fontsize=9, bbox_to_anchor=(0.5, -0.01))
    for txt in leg.get_texts():
        txt.set_color(t["ink2"])

    fig.tight_layout(rect=(0, 0.06, 0.88, 1))
    out = HERE / f"fig2-label-composition{'-dark' if mode == 'dark' else ''}.png"
    fig.savefig(out, facecolor=t["surface"], bbox_inches="tight")
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- 3
def fig3(verdict: dict, derived: dict, mode: str) -> Path:
    t = THEMES[mode]
    floor = derived["floor_pct"]
    sizing = derived["sizing_zero_k_upper_pct"]
    ns = sorted(int(k) for k in sizing)
    ran = {20, 80}  # the two N values this project actually ran

    fig, ax = plt.subplots(figsize=(7.6, 4.2), dpi=180)
    fig.patch.set_facecolor(t["surface"])
    style(ax, t)

    xs = list(range(len(ns)))
    for x, n in zip(xs, ns):
        pct = sizing[str(n)]
        ax.bar(x, pct, width=0.28,
               color=t["s1"] if n in ran else t["deemph"], zorder=3)
        if n in ran:
            ax.annotate(f"{pct:.1f}%", xy=(x, pct + 0.45), ha="center",
                        fontsize=9.5, color=t["ink"], fontweight="bold")

    ax.axhline(floor, color=t["muted"], linewidth=1.5, zorder=4)
    ax.annotate(f"{floor:.0f}%  nearest published cell (reference magnitude only)",
                xy=(1.7, floor + 0.45), ha="left", fontsize=8.5,
                color=t["muted"], zorder=5)

    ax.set_xticks(xs)
    ax.set_xticklabels([f"N={n}" for n in ns])
    ax.set_ylim(0, 18.5)
    ax.set_yticks([0, 5, 10, 15])
    ax.set_yticklabels(["0", "5%", "10%", "15%"])
    ax.yaxis.grid(True, color=t["grid"], linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel("combined N per gated cell per surface", fontsize=9.5,
                  color=t["ink2"])
    ax.set_ylabel("Wilson 95% upper bound on an observed 0/N", fontsize=9.5,
                  color=t["ink2"])

    handles = [Patch(facecolor=t["s1"], label="N this project ran"),
               Patch(facecolor=t["deemph"], label="candidate N, not run")]
    leg = ax.legend(handles=handles, loc="upper right", frameon=False,
                    fontsize=9)
    for txt in leg.get_texts():
        txt.set_color(t["ink2"])

    fig.tight_layout()
    out = HERE / f"fig3-sizing{'-dark' if mode == 'dark' else ''}.png"
    fig.savefig(out, facecolor=t["surface"], bbox_inches="tight")
    plt.close(fig)
    return out


def report(derived: dict) -> None:
    """Print every plotted number, so a reviewer can check the figures against
    the paper's tables without opening a PNG."""
    print("\n=== fig1 — primary estimand (plotted values) ===")
    print(f"{'surface':<13}{'scope':<16}{'k/n':<9}{'point %':>9}"
          f"{'Wilson lo %':>13}{'Wilson hi %':>13}{'template':>11}")
    for s, _ in SURFACES:
        for scope, _ in SCOPES:
            d = derived["primary"][f"{s}:{scope}"]
            print(f"{d['surface']:<13}{d['scope']:<16}"
                  f"{str(d['k']) + '/' + str(d['n']):<9}{d['rate_pct']:>9.1f}"
                  f"{d['wilson_lo_pct']:>13.1f}{d['wilson_hi_pct']:>13.1f}"
                  f"{d['band']:>11}")
    print(f"reference line: {derived['floor_pct']:.0f}%")

    print("\n=== fig2 — label composition (plotted values) ===")
    print(f"{'surface':<13}{'scope':<16}{'n':>4}   counts -> share %")
    for s, _ in SURFACES:
        for scope, _ in SCOPES:
            rec = derived["labels"][f"{s}:{scope}"]
            n = rec["n"]
            parts = []
            for name in LABEL_ORDER:
                c = rec["counts"].get(name, 0)
                parts.append(f"{name} {c} ({100.0 * c / n:.1f}%)")
            eng = derived["engagement"].get(f"{s}:{scope}")
            eng_s = f"engagement {eng['engagement_pct']:.0f}%" if eng else "engagement —"
            print(f"{rec['surface']:<13}{rec['scope']:<16}{n:>4}   "
                  f"{'; '.join(parts)}   [{eng_s}]")

    print("\n=== fig3 — sizing (plotted values) ===")
    print(f"{'N':<8}{'0/N Wilson upper %':>20}   emphasis")
    for n in sorted(int(k) for k in derived["sizing_zero_k_upper_pct"]):
        pct = derived["sizing_zero_k_upper_pct"][str(n)]
        print(f"N={n:<6}{pct:>20.1f}   {'ran' if n in (20, 80) else 'not run'}")
    print(f"reference line: {derived['floor_pct']:.0f}%")


def main() -> int:
    verdict, derived = load()
    written = []
    for mode in ("light", "dark"):
        written += [fig1(verdict, derived, mode),
                    fig2(verdict, derived, mode),
                    fig3(verdict, derived, mode)]
    report(derived)
    print("\nwrote:")
    for p in written:
        print(f"  {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
