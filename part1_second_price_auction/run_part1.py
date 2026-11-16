"""Part 1 entry point: second-price sealed-bid auction (sections A, B and C).

Usage:  python3 part1_second_price_auction/run_part1.py [--auctions N] [--independent] [--seed S]
Writes tables to results/ and plots to figures/ (both inside this folder).
"""
import argparse
import os

import numpy as np

from src import config
from src.experiments import (bid_sweep_fixed_rivals, bid_sweep_random_rivals,
                             table_fixed_rivals, table_random_rivals)
from src.plots import save_fixed_rival_plots, save_random_rival_plots

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
FIGURES = os.path.join(HERE, "figures")


def report(text, filename):
    print(text + "\n")
    with open(os.path.join(RESULTS, filename), "w") as f:
        f.write(text + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--auctions", type=int, default=config.N_AUCTIONS, help="auctions simulated per bid")
    ap.add_argument("--independent", action="store_true",
                    help="fresh rival draws for every bid instead of common random numbers")
    ap.add_argument("--seed", type=int, default=config.SEED)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    crn = not args.independent
    os.makedirs(RESULTS, exist_ok=True)

    # A — one rival with random values
    a1 = bid_sweep_random_rivals(1, args.auctions, rng, crn)
    report(table_random_rivals(a1, "Part 1A - one rival (bidder 2), random values"), "A_one_rival_random_values.txt")
    save_random_rival_plots(a1, 1, os.path.join(FIGURES, "A_one_rival_random_values"),
                            "Part 1A: second-price, 1 rival - average utility of bidder 1 vs its bid")

    # B — one rival with fixed bids
    b1 = bid_sweep_fixed_rivals(config.FIXED_BIDS_ONE_RIVAL, rng)
    report(table_fixed_rivals(b1, "Part 1B - one rival, bid fixed at 0.1 / 0.4 / 0.9"), "B_one_rival_fixed_bids.txt")
    save_fixed_rival_plots(b1, config.FIXED_BIDS_ONE_RIVAL, os.path.join(FIGURES, "B_one_rival_fixed_bids"),
                           "Part 1B: rival bid fixed - utility of bidder 1 (red dot = truthful b = v)")

    # C — repeat A and B with two rivals (bidders 2 and 3, same strategy)
    a2 = bid_sweep_random_rivals(2, args.auctions, rng, crn)
    report(table_random_rivals(a2, "Part 1C (A repeated) - two rivals (bidders 2, 3), random values"),
           "C1_two_rivals_random_values.txt")
    save_random_rival_plots(a2, 2, os.path.join(FIGURES, "C1_two_rivals_random_values"),
                            "Part 1C: second-price, 2 rivals - average utility of bidder 1 vs its bid")

    b2 = bid_sweep_fixed_rivals(config.FIXED_BIDS_TWO_RIVALS, rng)
    report(table_fixed_rivals(b2, "Part 1C (B repeated) - two rivals, fixed bids"), "C2_two_rivals_fixed_bids.txt")
    save_fixed_rival_plots(b2, config.FIXED_BIDS_TWO_RIVALS, os.path.join(FIGURES, "C2_two_rivals_fixed_bids"),
                           "Part 1C: two rivals with fixed bids - utility of bidder 1 (red dot = b = v)")


if __name__ == "__main__":
    main()
