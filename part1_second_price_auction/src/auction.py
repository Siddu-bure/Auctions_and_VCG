"""Second-price auction model: rival bids, bidder 1's utility, closed-form expectation."""
import numpy as np

from .config import STRATEGIES, STRATEGY_MAX_BID


def highest_rival_bid(strategy, n_rivals, n_auctions, rng):
    """Draw rival values ~ U[0,1], apply the strategy, return the top rival bid per auction."""
    values = rng.uniform(0.0, 1.0, size=(n_auctions, n_rivals))
    bids = STRATEGIES[strategy](values, rng)
    return bids.max(axis=1)


def utility(v, b, top_rival, rng):
    """Bidder 1 (value v, bid b) wins if b beats the top rival bid and pays that bid.
    Utility = v - top_rival if it wins, else 0.  Ties are broken uniformly at random."""
    win = b > top_rival
    tie = b == top_rival
    if np.any(tie):
        win = win | (tie & (rng.random(top_rival.shape) < 0.5))
    return np.where(win, v - top_rival, 0.0)


def expected_utility_exact(v, b, strategy, n_rivals):
    """E[u] = integral_0^min(b, M) (v - x) f(x) dx, where the top rival bid is the max of
    n iid U[0, M] bids with density f(x) = n x^(n-1) / M^n.  Used to check the simulation."""
    M = STRATEGY_MAX_BID[strategy]
    hi = min(b, M)
    n = n_rivals
    return (v * hi ** n - n / (n + 1) * hi ** (n + 1)) / M ** n
