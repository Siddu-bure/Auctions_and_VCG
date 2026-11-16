# Part 1 — Second-price sealed-bid auction

Run from the project root: `python3 part1_second_price_auction/run_part1.py`
(options: `--auctions N`, `--independent`, `--seed S`)

## Code (`src/`)
| file | what it does |
|---|---|
| `config.py` | Bidder 1 values {0.2, 0.5, 0.8}, the bid grid 0.00–1.00, the three rival strategies, the fixed rival bids, sample size and seed |
| `auction.py` | Auction model: draws the highest rival bid, computes bidder 1's utility (pays the highest rival bid), and gives the closed-form expected utility used to check the simulation |
| `experiments.py` | Experiment A (bid sweep against random rivals), experiment B (bid sweep against fixed rival bids), and the result tables |
| `plots.py` | A 3×3 grid of plots plus each of the 9 plots as its own file |
| `../run_part1.py` | Runs A, B and C and writes `results/` and `figures/` |

## Outputs
| question | table | figures |
|---|---|---|
| A — 1 rival, random values | `results/A_one_rival_random_values.txt` | `figures/A_one_rival_random_values/all_9_plots.png`, `individual/*.png` |
| B — 1 rival, bid fixed at 0.1 / 0.4 / 0.9 | `results/B_one_rival_fixed_bids.txt` | `figures/B_one_rival_fixed_bids/` |
| C — A repeated with 2 rivals | `results/C1_two_rivals_random_values.txt` | `figures/C1_two_rivals_random_values/` |
| C — B repeated with 2 rivals | `results/C2_two_rivals_fixed_bids.txt` | `figures/C2_two_rivals_fixed_bids/` |

Individual plot files are named `v<value>_<rival strategy>.png` or `v<value>_rivals_<fixed bids>.png`.

**Result:** in every case, bidding b = v gives the highest utility. The answers are explained in the main [README](../README.md#part-1--second-price-sealed-bid-auction).
