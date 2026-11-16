"""Plotting for Part 2."""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .auction import exact_u1
from .config import K_GRID, equilibrium_k

COLORS = {2: "#1f77b4", 3: "#ff7f0e", 4: "#2ca02c"}


def _expected_utility(ax, n, results):
    u = np.array([r["u1"] for r in results])
    ax.plot(K_GRID, u, color=COLORS[n], lw=2, label=f"n = {n} simulated")
    ax.plot(K_GRID, [exact_u1(n, k) for k in K_GRID], color="black", lw=0.8, ls="--")
    ax.axvline(equilibrium_k(n), color=COLORS[n], ls=":", lw=1)
    ax.plot(K_GRID[np.argmax(u)], u.max(), "o", color=COLORS[n])


def _finish(ax, title, ylabel):
    ax.axhline(0, color="black", lw=0.5)
    ax.set_xlabel("k  (bidder 1 bids k·v)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.3)


def save_all(res, out_dir):
    os.makedirs(os.path.join(out_dir, "per_bidder_count"), exist_ok=True)

    # 1. expected utility, all n together
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for n, results in res.items():
        _expected_utility(ax, n, results)
    _finish(ax, "Bidder 1's expected utility vs bid fraction k\n"
                "(black dashed = closed form, dotted = equilibrium k=(n-1)/n)", "expected utility")
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "expected_utility_all_n.png"), dpi=130)
    plt.close(fig)

    # 2. expected utility, one file per n
    for n, results in res.items():
        fig, ax = plt.subplots(figsize=(7, 4.5))
        _expected_utility(ax, n, results)
        _finish(ax, f"n = {n}: bidder 1's expected utility (equilibrium k = {equilibrium_k(n):.2f})",
                "expected utility")
        fig.tight_layout()
        fig.savefig(os.path.join(out_dir, "per_bidder_count", f"expected_utility_n{n}.png"), dpi=120)
        plt.close(fig)

    # 3. could the winner have paid less?
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    for n, results in res.items():
        ax1.plot(K_GRID, [r["frac_could_pay_less"] for r in results], color=COLORS[n], lw=2,
                 label=f"n = {n}: gap > 0")
        ax1.plot(K_GRID, [r["frac_overpay_gt_1c"] for r in results], color=COLORS[n], lw=1, ls="--",
                 label=f"n = {n}: gap > 0.01")
        ax2.plot(K_GRID, [r["mean_left_on_table"] for r in results], color=COLORS[n], lw=2, label=f"n = {n}")
    ax1.set_ylim(0.9, 1.005)
    _finish(ax1, "Fraction of auctions where the winner could have paid less", "fraction of auctions")
    _finish(ax2, "Mean money left on the table (winning bid − 2nd-highest bid)", "mean gap")
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "winner_could_pay_less.png"), dpi=130)
    plt.close(fig)
