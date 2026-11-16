"""Experiment settings for Part 2 (first-price sealed-bid auction, n bidders)."""
import numpy as np

# Bidder 1 bids k * v.  Step 0.01 so the equilibrium fractions 1/2, ~2/3, 3/4 are on the grid.
K_GRID = np.round(np.arange(10, 201) / 100.0, 2)  # 0.10, 0.11, ..., 2.00

# Numbers of bidders to study
N_BIDDERS = [2, 3, 4]

# k values printed in the result tables
TABLE_K = [0.1, 0.25, 0.5, 0.67, 0.75, 0.8, 1.0, 1.25, 1.5, 2.0]

N_AUCTIONS = 100_000  # auctions simulated per (n, k)
SEED = 7


def equilibrium_k(n):
    """Symmetric Bayes-Nash equilibrium bid fraction for n bidders with U[0,1] values."""
    return (n - 1) / n
