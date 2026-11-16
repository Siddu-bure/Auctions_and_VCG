"""Part 2 entry point: first-price auction where bidder 1 deviates to k*v (n = 2, 3, 4).

Usage:  python3 part2_first_price_auction/run_part2.py [--auctions N] [--seed S]
Writes tables to results/ and plots to figures/ (both inside this folder).
"""
import argparse
import os

import numpy as np

from src import config
from src.experiments import sweep_k, table_for_n
from src.plots import save_all

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
FIGURES = os.path.join(HERE, "figures")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--auctions", type=int, default=config.N_AUCTIONS, help="auctions per (n, k)")
    ap.add_argument("--seed", type=int, default=config.SEED)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    os.makedirs(RESULTS, exist_ok=True)

    res = {}
    for n in config.N_BIDDERS:
        res[n] = sweep_k(n, args.auctions, rng)
        text = table_for_n(n, res[n])
        print(text + "\n")
        with open(os.path.join(RESULTS, f"first_price_n{n}.txt"), "w") as f:
            f.write(text + "\n")

    save_all(res, FIGURES)


if __name__ == "__main__":
    main()
