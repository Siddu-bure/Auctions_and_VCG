"""First-price auction model: Monte Carlo simulation and closed-form check."""
import numpy as np

from .config import equilibrium_k


def simulate(n, k, n_auctions, rng):
    """Simulate n_auctions first-price auctions.  Bidder 1 bids k*v, bidders 2..n bid
    ((n-1)/n)*v, all values iid U[0,1].  Ties for the top bid are broken uniformly at random.

    Returns bidder 1's mean utility (+ standard error), its win probability, and how often /
    by how much the winner could have bid less and still won (winning bid > 2nd-highest bid)."""
    values = rng.uniform(0.0, 1.0, size=(n_auctions, n))
    bids = values * equilibrium_k(n)
    bids[:, 0] = k * values[:, 0]

    # sort each auction's bids; a random secondary key breaks exact ties
    order = np.lexsort((rng.random(bids.shape), bids), axis=1)
    rows = np.arange(n_auctions)
    winner = order[:, -1]
    winning_bid = bids[rows, winner]
    second_bid = bids[rows, order[:, -2]]

    bidder1_wins = winner == 0
    u1 = np.where(bidder1_wins, values[:, 0] - bids[:, 0], 0.0)
    gap = winning_bid - second_bid  # amount the winner could have saved
    return {
        "u1": u1.mean(),
        "u1_se": u1.std(ddof=1) / np.sqrt(n_auctions),
        "p_win": bidder1_wins.mean(),
        "frac_could_pay_less": (gap > 0).mean(),
        "frac_overpay_gt_1c": (gap > 0.01).mean(),
        "mean_left_on_table": gap.mean(),
    }


def exact_u1(n, k):
    """Closed-form E[u1].  P(bidder 1 wins | v) = min(1, a v)^(n-1) with a = k n / (n-1)."""
    a = k * n / (n - 1)
    if a <= 1:
        return (1 - k) * a ** (n - 1) / (n + 1)
    t = 1.0 / a  # for v > t bidder 1 always wins
    return (1 - k) * (t ** 2 / (n + 1) + (1 - t ** 2) / 2)
