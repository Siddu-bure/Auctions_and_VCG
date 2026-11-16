"""Experiment settings for Part 1 (second-price sealed-bid auction)."""
import numpy as np

# Bidder 1's fixed private values (one experiment per value)
VALUES = [0.2, 0.5, 0.8]

# Bidder 1's bids swept on the horizontal axis: 0.00, 0.01, ..., 1.00
BIDS = np.round(np.arange(0, 101) / 100.0, 2)

# Rival strategies: map the rival's true values (array) to bids
STRATEGIES = {
    "truthful": lambda values, rng: values,
    "half value": lambda values, rng: values / 2.0,
    "random U[0,1]": lambda values, rng: rng.uniform(0.0, 1.0, size=values.shape),
}

# Upper bound of each strategy's bid distribution (used by the closed-form check)
STRATEGY_MAX_BID = {"truthful": 1.0, "half value": 0.5, "random U[0,1]": 1.0}

# Part B: fixed rival bids.  With two rivals only the highest bid matters, so these
# pairs give a highest rival bid of 0.1, 0.4 and 0.9 respectively.
FIXED_BIDS_ONE_RIVAL = [(0.1,), (0.4,), (0.9,)]
FIXED_BIDS_TWO_RIVALS = [(0.1, 0.1), (0.1, 0.4), (0.4, 0.9)]

N_AUCTIONS = 100_000  # auctions simulated per bid
SEED = 42
