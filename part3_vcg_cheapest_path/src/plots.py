"""Plotting for Part 3: the network, misreport sweeps for chosen edges, and all edges."""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .graph import NODE_POS, TRUE_COST
from .vcg import truthful_index

BLUE, RED = "#1f77b4", "#d62728"


def save_network(path, payment, filename):
    """Draw Figure 7.3 with the VCG-chosen path in red and payments in the labels."""
    fig, ax = plt.subplots(figsize=(8, 5))
    for e, c in TRUE_COST.items():
        (x1, y1), (x2, y2) = NODE_POS[e[0]], NODE_POS[e[1]]
        on = e in path
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", lw=3 if on else 1.3, color=RED if on else "grey",
                                    shrinkA=17, shrinkB=17, mutation_scale=16))
        label = f"{e}: cost {c}" + (f"\npaid {payment[e]:g}" if on else "")
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my, label, fontsize=9, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=RED if on else "lightgrey"))
    for node, (x, y) in NODE_POS.items():
        ax.add_patch(plt.Circle((x, y), 0.14, color="#f0f0f0", ec="black", zorder=3))
        ax.text(x, y, node, ha="center", va="center", fontsize=13, weight="bold", zorder=4)
    ax.set_xlim(-0.4, 3.4)
    ax.set_ylim(-0.4, 2.4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Figure 7.3 network - VCG chooses ABEF (red); payments shown on chosen edges")
    fig.tight_layout()
    fig.savefig(filename, dpi=130)
    plt.close(fig)


def _draw_sweep(ax, edge, where, reports, utilities, chosen):
    ax.step(reports, utilities, where="mid", color=BLUE, lw=2)
    ax.plot(reports, utilities, "o", color=BLUE, ms=4)
    ax.axvline(TRUE_COST[edge], color=RED, ls=":", lw=1.5, label=f"true cost = {TRUE_COST[edge]}")
    ax.axhline(0, color="black", lw=0.5)
    for i in range(1, len(reports)):  # shade where the chosen path switches
        if chosen[i] != chosen[i - 1]:
            ax.axvspan(reports[i - 1], reports[i], color="#cccccc", alpha=0.4)
            ax.text(reports[i], utilities.max() + 0.25, f"{chosen[i - 1]} → {chosen[i]}",
                    fontsize=8, ha="center")
    ax.set_ylim(min(utilities.min(), 0) - 0.5, utilities.max() + 0.8)
    ax.set_title(f"Edge {edge} ({where}): utility vs declared cost")
    ax.set_xlabel("declared cost")
    ax.set_ylabel("utility = payment − true cost (if used)")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)


def save_sweep(edge, where, reports, utilities, chosen, filename):
    fig, ax = plt.subplots(figsize=(7, 4.8))
    _draw_sweep(ax, edge, where, reports, utilities, chosen)
    fig.tight_layout()
    fig.savefig(filename, dpi=130)
    plt.close(fig)


def save_all_edges(reports, sweeps, filename):
    fig, ax = plt.subplots(figsize=(9, 5))
    for e, (u, _) in sweeps.items():
        ax.plot(reports, u - u[truthful_index(e, reports)], marker=".", label=e)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xlabel("declared cost")
    ax.set_ylabel("utility change vs truthful report")
    ax.set_title("VCG path auction: no edge gains by misreporting (all curves ≤ 0)")
    ax.legend(ncol=4)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(filename, dpi=130)
    plt.close(fig)
