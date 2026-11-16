# Part 2 — First-price auction, n = 2, 3, 4

Run from the project root: `python3 part2_first_price_auction/run_part2.py`
(options: `--auctions N`, `--seed S`)

## Code (`src/`)
| file | what it does |
|---|---|
| `config.py` | k grid 0.10–2.00 in steps of 0.01, the values of n, sample size, seed, and the equilibrium fraction (n−1)/n |
| `auction.py` | `simulate()`: bidder 1 bids k·v and the other bidders bid ((n−1)/n)·v. It records bidder 1's utility and whether the winner could have paid less. `exact_u1()` gives the closed form |
| `experiments.py` | Runs the sweep over k for each n and builds the result tables |
| `plots.py` | Expected-utility plots and the "could have paid less" plots |
| `../run_part2.py` | Runs every n and writes `results/` and `figures/` |

## Outputs
| what | where |
|---|---|
| Table for each n (utility, win probability, could-pay-less fraction, mean gap) | `results/first_price_n2.txt`, `_n3.txt`, `_n4.txt` |
| Bidder 1's expected utility vs k, all n on one plot | `figures/expected_utility_all_n.png` |
| Same, one plot per n | `figures/per_bidder_count/expected_utility_n{2,3,4}.png` |
| Fraction of auctions where the winner could have paid less, and the mean amount | `figures/winner_could_pay_less.png` |

**Result:** the best k is the equilibrium value (n−1)/n. The winner could have paid less in 100 % of auctions. The answers are explained in the main [README](../README.md#part-2--first-price-auction-n-bidders).
