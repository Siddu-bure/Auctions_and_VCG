"""Part 2 experiment: sweep bidder 1's bid fraction k for each n, and format result tables."""
import numpy as np

from .auction import exact_u1, simulate
from .config import K_GRID, TABLE_K, equilibrium_k


def sweep_k(n, n_auctions, rng):
    """List of simulation results, one per k in K_GRID."""
    return [simulate(n, k, n_auctions, rng) for k in K_GRID]


def table_for_n(n, results):
    u = np.array([r["u1"] for r in results])
    exact = np.array([exact_u1(n, k) for k in K_GRID])
    title = f"Part 2 - first-price auction, n = {n} bidders"
    lines = [
        title, "=" * len(title),
        f"equilibrium k = (n-1)/n = {equilibrium_k(n):.3f}",
        f"best k (simulated)      = {K_GRID[np.argmax(u)]:.2f}",
        f"best k (closed form)    = {K_GRID[np.argmax(exact)]:.2f}",
        "",
        f"{'k':>5} {'E[u1] sim':>10} {'± s.e.':>8} {'exact':>8} {'P(1 wins)':>10} "
        f"{'could pay less':>15} {'overpay>1c':>11} {'mean gap':>9}",
    ]
    for k in TABLE_K:
        i = int(np.argmin(np.abs(K_GRID - k)))
        r = results[i]
        lines.append(f"{K_GRID[i]:>5.2f} {r['u1']:>10.5f} {r['u1_se']:>8.5f} {exact[i]:>8.5f} "
                     f"{r['p_win']:>10.4f} {r['frac_could_pay_less']:>15.4f} "
                     f"{r['frac_overpay_gt_1c']:>11.4f} {r['mean_left_on_table']:>9.4f}")
    lines += [
        "",
        "Columns: could pay less = fraction of auctions where winning bid > 2nd-highest bid;",
        "         overpay>1c     = same, but by more than 0.01;",
        "         mean gap       = mean (winning bid - 2nd-highest bid), the money left on the table.",
    ]
    return "\n".join(lines)
