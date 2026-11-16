"""Part 1 experiments (A: bid sweep vs random rivals, B: bid sweep vs fixed rival bids)
and the text tables summarising them."""
import numpy as np

from .auction import highest_rival_bid, utility
from .config import BIDS, STRATEGIES, VALUES


def bid_sweep_random_rivals(n_rivals, n_auctions, rng, common_random_numbers=True):
    """Experiment A.  Returns {(v, strategy): mean utility for every bid in BIDS}.

    With common_random_numbers the same n_auctions rival draws are re-used for every bid,
    so differences between bids reflect the bid itself rather than sampling noise."""
    results = {}
    for strategy in STRATEGIES:
        shared = highest_rival_bid(strategy, n_rivals, n_auctions, rng) if common_random_numbers else None
        for v in VALUES:
            mean_u = np.empty(len(BIDS))
            for i, b in enumerate(BIDS):
                top = shared if common_random_numbers else highest_rival_bid(strategy, n_rivals, n_auctions, rng)
                mean_u[i] = utility(v, b, top, rng).mean()
            results[(v, strategy)] = mean_u
    return results


def bid_sweep_fixed_rivals(fixed_rival_bids, rng):
    """Experiment B.  Returns {(v, rival_bids): utility for every bid in BIDS}."""
    results = {}
    for rivals in fixed_rival_bids:
        top = np.array([max(rivals)])
        for v in VALUES:
            results[(v, rivals)] = np.array([utility(v, b, top, rng)[0] for b in BIDS])
    return results


def utility_at_truth(u, v):
    return u[np.isclose(BIDS, v)][0]


def table_random_rivals(results, title):
    lines = [title, "=" * len(title),
             f"{'v':>4} {'rival strategy':>15} {'argmax b':>9} {'E[u] at b=v':>12} {'max E[u]':>9}"]
    for (v, strategy), u in results.items():
        lines.append(f"{v:>4} {strategy:>15} {BIDS[np.argmax(u)]:>9.2f} "
                     f"{utility_at_truth(u, v):>12.4f} {u.max():>9.4f}")
    lines.append("\nNote: for 'half value' rivals and v = 0.8 every b >= 0.5 is optimal (flat curve),"
                 "\nso argmax reports the first maximiser; b = v attains the same maximum.")
    return "\n".join(lines)


def table_fixed_rivals(results, title):
    lines = [title, "=" * len(title),
             f"{'v':>4} {'rival bid(s)':>14} {'u(b=v)':>8} {'max u':>8} {'b=v optimal?':>13}  optimal bids"]
    all_ok = True
    for (v, rivals), u in results.items():
        u_v = utility_at_truth(u, v)
        ok = bool(np.isclose(u_v, u.max()))
        all_ok &= ok
        opt = BIDS[np.isclose(u, u.max())]
        span = f"[{opt.min():.2f}, {opt.max():.2f}]" if len(opt) > 1 else f"{opt[0]:.2f}"
        lines.append(f"{v:>4} {str(rivals):>14} {u_v:>8.3f} {u.max():>8.3f} {str(ok):>13}  {span}")
    lines.append("\nRESULT: " + ("b = v is a best response in ALL cases" if all_ok
                                 else "FAILED: b = v is not optimal in some case"))
    return "\n".join(lines)
