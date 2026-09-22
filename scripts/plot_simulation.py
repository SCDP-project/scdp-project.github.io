"""Render the simulation chart (requires matplotlib).

Source: arXiv:2606.14535v1, Table 1, Meta-World difficulty groups.
Run from any directory: python scripts/plot_simulation.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def render_chart(mobile=False):
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "svg.fonttype": "none",
        "svg.hashsalt": "scdp-simulation",
    })
    groups = ["Easy", "Medium", "Hard", "Very Hard"]
    results = {
        "DP": [79.9, 36.1, 16.7, 46.0],
        "DP3": [92.3, 78.5, 60.3, 82.7],
        "SCDP (Ours)": [91.5, 83.0, 82.5, 89.7],
    }
    colors = ["#b6c3d7", "#798da9", "#2563eb"]
    fig, ax = plt.subplots(figsize=(3.8 if mobile else 6.2, 2.8))
    fig.subplots_adjust(left=0.10 if mobile else 0.08, right=0.99, top=0.79, bottom=0.12)
    x = np.arange(len(groups))
    for i, (method, values) in enumerate(results.items()):
        bars = ax.bar(x + (i - 1) * 0.24, values, width=0.21,
                      color=colors[i], label=method, zorder=3)
        if method == "SCDP (Ours)":
            ax.bar_label(bars, labels=[f"{v:.1f}" for v in values],
                         padding=4, fontsize=9 if mobile else 10, fontweight="bold", color=colors[i])
    ax.set_xticks(x, groups)
    ax.set_ylim(0, 105)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.grid(axis="y", color="#e0e7f1", linewidth=0.7, zorder=0)
    ax.tick_params(axis="both", length=0)
    ax.tick_params(axis="x", colors="#19263e", labelsize=10, pad=9)
    ax.tick_params(axis="y", colors="#627089", labelsize=9, pad=6)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.legend(loc="lower left", bbox_to_anchor=(-0.045, 1.13), ncol=3,
              frameon=False, fontsize=10, handlelength=1, handleheight=0.8,
              columnspacing=1.2 if mobile else 1.8, labelcolor="#19263e", borderaxespad=0)
    filename = "simulation-success-mobile.svg" if mobile else "simulation-success.svg"
    destination = (Path(__file__).resolve().parents[1]
                   / "static/images/scdp" / filename)
    fig.savefig(destination, transparent=True, metadata={
        "Date": None,
        "Title": "Success across Meta-World difficulty groups",
        "Description": (
            "arXiv:2606.14535v1, Table 1. Easy / Medium / Hard / Very Hard: "
            "DP 79.9 / 36.1 / 16.7 / 46.0%; "
            "DP3 92.3 / 78.5 / 60.3 / 82.7%; "
            "SCDP 91.5 / 83.0 / 82.5 / 89.7%."
        ),
    })
    plt.close(fig)
    print(destination)


if __name__ == "__main__":
    render_chart()
    render_chart(mobile=True)
