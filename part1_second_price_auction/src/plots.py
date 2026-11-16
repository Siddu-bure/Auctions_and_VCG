"""Plotting for Part 1: a 3x3 overview grid plus one PNG per (value, scenario) combination."""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .auction import expected_utility_exact
from .config import BIDS, STRATEGIES, VALUES

BLUE, RED, GREY = "#1f77b4", "#d62728", "#888888"


def _slug(text):
    return "".join(ch if ch.isalnum() else "_" for ch in str(text)).strip("_").replace("__", "_")


def _style(ax, ylabel="average utility"):
    ax.axhline(0, color="black", lw=0.5)
    ax.grid(alpha=0.3)
    ax.set_xlabel("bidder 1's bid b")
    ax.set_ylabel(ylabel)


def _draw_random(ax, u, v, strategy, n_rivals):
    exact = [expected_utility_exact(v, b, strategy, n_rivals) for b in BIDS]
    ax.plot(BIDS, u, color=BLUE, lw=2, label="simulated")
    ax.plot(BIDS, exact, color=GREY, lw=1, ls="--", label="exact")
    ax.axvline(v, color=RED, ls=":", lw=1.5, label=f"b = v = {v}")
    ax.plot(BIDS[np.argmax(u)], u.max(), "o", color=RED)
    ax.set_title(f"v = {v}, rivals: {strategy}\nargmax b = {BIDS[np.argmax(u)]:.2f}, "
                 f"max E[u] = {u.max():.4f}", fontsize=10)
    _style(ax)


def _draw_fixed(ax, u, v, rivals):
    ax.plot(BIDS, u, color=BLUE, lw=2, label="utility")
    ax.axvline(v, color=RED, ls=":", lw=1.5, label=f"b = v = {v}")
    ax.plot(v, u[np.isclose(BIDS, v)][0], "o", color=RED)
    shown = rivals[0] if len(rivals) == 1 else rivals
    ax.set_title(f"v = {v}, rival bid(s) = {shown}", fontsize=10)
    _style(ax, "utility")


def save_random_rival_plots(results, n_rivals, out_dir, title):
    """Grid of all 9 combinations + 9 individual files in out_dir/individual/."""
    os.makedirs(os.path.join(out_dir, "individual"), exist_ok=True)
    fig, axes = plt.subplots(3, 3, figsize=(14, 11))
    for r, v in enumerate(VALUES):
        for c, strategy in enumerate(STRATEGIES):
            _draw_random(axes[r, c], results[(v, strategy)], v, strategy, n_rivals)

            f1, ax1 = plt.subplots(figsize=(6, 4.2))
            _draw_random(ax1, results[(v, strategy)], v, strategy, n_rivals)
            ax1.legend(fontsize=8)
            f1.tight_layout()
            f1.savefig(os.path.join(out_dir, "individual", f"v{v}_{_slug(strategy)}.png"), dpi=120)
            plt.close(f1)
    axes[0, 0].legend(fontsize=8)
    fig.suptitle(title, fontsize=13)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "all_9_plots.png"), dpi=130)
    plt.close(fig)


def save_fixed_rival_plots(results, fixed_rival_bids, out_dir, title):
    os.makedirs(os.path.join(out_dir, "individual"), exist_ok=True)
    fig, axes = plt.subplots(3, len(fixed_rival_bids), figsize=(14, 11))
    for r, v in enumerate(VALUES):
        for c, rivals in enumerate(fixed_rival_bids):
            _draw_fixed(axes[r, c], results[(v, rivals)], v, rivals)

            f1, ax1 = plt.subplots(figsize=(6, 4.2))
            _draw_fixed(ax1, results[(v, rivals)], v, rivals)
            ax1.legend(fontsize=8)
            f1.tight_layout()
            f1.savefig(os.path.join(out_dir, "individual", f"v{v}_rivals_{_slug(rivals)}.png"), dpi=120)
            plt.close(f1)
    fig.suptitle(title, fontsize=13)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "all_9_plots.png"), dpi=130)
    plt.close(fig)
