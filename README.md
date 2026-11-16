# Assignment 4 — Auctions and the VCG Mechanism

```
.
├── README.md                     ← overview, how to run, written answers (this file)
├── requirements.txt              ← numpy, matplotlib
├── run_all.sh                    ← runs all three parts
│
├── part1_second_price_auction/   ← Part 1: second-price auction (A, B, C)
│   ├── README.md                 ← what each file does, which output answers which question
│   ├── run_part1.py              ← entry point
│   ├── src/                      ← config.py · auction.py · experiments.py · plots.py
│   ├── results/                  ← one .txt table per question (same names as the figure folders)
│   └── figures/
│       ├── A_one_rival_random_values/     all_9_plots.png + individual/ (9 files)
│       ├── B_one_rival_fixed_bids/        all_9_plots.png + individual/ (9 files)
│       ├── C1_two_rivals_random_values/   all_9_plots.png + individual/ (9 files)
│       └── C2_two_rivals_fixed_bids/      all_9_plots.png + individual/ (9 files)
│
├── part2_first_price_auction/    ← Part 2: first-price auction, n = 2, 3, 4
│   ├── README.md
│   ├── run_part2.py
│   ├── src/                      ← config.py · auction.py · experiments.py · plots.py
│   ├── results/                  ← first_price_n2.txt · first_price_n3.txt · first_price_n4.txt
│   └── figures/                  ← expected_utility_all_n.png · winner_could_pay_less.png · per_bidder_count/
│
├── part3_vcg_cheapest_path/      ← Part 3: VCG cheapest path (Figure 7.3)
│   ├── README.md
│   ├── run_part3.py
│   ├── src/                      ← graph.py · vcg.py · plots.py
│   ├── results/                  ← 1_vcg_payments · 2_misreport_BE · 3_misreport_CE · 4_misreport_all_edges (.txt)
│   └── figures/                  ← same numbering (.png), plus the network drawing
│
└── REPORT.pdf                    ← the full report (team, method, results, answers)

(The textbook, Weiss (ed.) Multiagent Systems Ch. 7 — Figure 7.3 — is kept locally in reference/ and is not in the repo.)
```

**Run everything:** `pip install -r requirements.txt`, then `./run_all.sh`. This takes about 15 s, and seeds are fixed, so the output can be reproduced.
**Run one part:** `python3 part1_second_price_auction/run_part1.py` (and likewise `run_part2.py` and `run_part3.py`). Run `--help` to see the options.
Every part has the same layout: `run_partN.py`, which calls the modules in `src/`, writes tables to `results/` and plots to `figures/`.

---

## Part 1 — Second-price sealed-bid auction

**Setup:** Bidder 1's value is v ∈ {0.2, 0.5, 0.8}. Rival values are drawn from U[0,1]. The rival strategies are truthful, half of the value, or a random U[0,1] bid. Bidder 1 bids b = 0.00, 0.01, …, 1.00, with 100 000 auctions per bid. If bidder 1 wins it pays the highest rival bid, so its utility is v − (highest rival bid); if it loses, its utility is 0.

The same 100 000 rival draws are reused for every bid (common random numbers). Because of this, differences between the curves come from the bid and not from sampling noise. Use `--independent` to draw new samples for each bid instead. Each plot also shows the exact expected-utility curve as a dashed line, and the simulation lies on top of it.

### A. Do the plots help bidder 1 choose its strategy?
Yes. All 9 curves peak at **b = v**:

| v | truthful rival | half-value rival | random rival |
|---|---|---|---|
| 0.2 | argmax 0.20 | argmax 0.20 | argmax 0.20 |
| 0.5 | argmax 0.50 | argmax 0.50 (flat after 0.5) | argmax 0.50 |
| 0.8 | argmax 0.80 | flat for b ≥ 0.5, so b = 0.8 is also optimal | argmax 0.80 |

Bidding above v adds only wins where the rival bid is between v and b. In those wins bidder 1 pays more than its value, so its utility is negative. Bidding below v drops only wins where the rival bid is between b and v, and those were profitable. In the half-value case the rival never bids above 0.5, so once b ≥ 0.5 any higher bid gives the same result. The optimum does not depend on which strategy the rival uses, so bidder 1 does not need to know it: **bidding truthfully is the best choice**.

### B. Fixed rival bids {0.1, 0.4, 0.9}
In all 9 cases b = v reaches the maximum utility (see `part1_second_price_auction/results/B_one_rival_fixed_bids.txt`).
- If the rival bid r < v, any b > r wins and earns v − r, and b = v is one of those bids.
- If r > v, any b < r loses and earns 0, and b = v is one of those bids. Winning would give v − r < 0.

Truthful bidding is therefore a **weakly dominant strategy**. It is never worse than any other bid, whatever the rival bids.

### C. Two rivals (bidders 2 and 3, same strategy)
- **A repeated:** all 9 argmaxes are again at b = v. In the half-value case with v = 0.8, every b ≥ 0.5 ties for the maximum. Expected utilities are lower than with one rival because there is more competition. For example, with v = 0.5 and truthful rivals the expected utility falls from 0.125 to 0.042.
- **B repeated:** the rival bids are fixed at (0.1, 0.1), (0.1, 0.4) and (0.4, 0.9), so the highest rival bid is 0.1, 0.4 and 0.9. b = v is optimal in all 9 cases. Only the highest rival bid affects bidder 1, so the argument from B still applies.

## Part 2 — First-price auction, n bidders

The other bidders use the equilibrium bid ((n−1)/n)·v. Bidder 1 bids k·v with k = 0.10, 0.11, …, 2.00, and each k is simulated with 100 000 auctions. A closed-form expected utility is plotted as a dashed line for comparison.

| n | equilibrium k | best simulated k | E[u₁] at equilibrium | E[u₁] at k = 1 |
|---|---|---|---|---|
| 2 | 0.500 | 0.50 | 0.167 | 0 |
| 3 | 0.667 | 0.67 | 0.083 | 0 |
| 4 | 0.750 | 0.74 (exact: 0.75) | 0.050 | 0 |

- Bidder 1's best deviation is the equilibrium shading k = (n−1)/n, so no profitable deviation exists. For n = 4 the simulation picks 0.74 because the curve is flat near its peak and the difference is within sampling noise; the exact curve peaks at 0.75.
- Bidding truthfully (k = 1) always gives 0 utility, and overbidding (k > 1) gives negative utility. In a first-price auction, bidders should not bid their true value.
- **Could the winner have paid less and still won?** The winner could have paid less in **100 % of auctions** for every k and n. The winning bid is strictly above the second-highest bid with probability 1, because the bids are continuous. Even counting only overpayments of more than 1 cent, the share is 95–99 %. The average amount the winner could have saved is 0.15–0.79 and is smallest near equilibrium. This regret is built into first-price auctions; a second-price auction removes it by charging the winner the second-highest bid.

## Part 3 — VCG for the cheapest A→F path (Figure 7.3)

The edge costs are AB 3, AC 2, BD 2, BE 1, CE 3, CF 5, DF 2, EF 1. The payment to edge e is (cost of the best path without e) − (cost of the chosen path excluding e's own cost).

| edge | on path | best path without it | paid | utility |
|---|---|---|---|---|
| AB | yes | ACEF (6) | **4** | 1 |
| BE | yes | ACEF (6) | **2** | 1 |
| EF | yes | ABDF (7) | **3** | 2 |
| others | no | ABEF (5) | 0 | 0 |

The chosen path is **ABEF** with cost 5, and these payments match the text. The script checks them with an assertion.

**Misreporting declared costs 0, 0.5, …, 10:**
- **BE (on the path, true cost 1):** Any declared cost ≤ 2 keeps ABEF selected and gets the same payment of 2, so utility stays at 1. Above 2 the path switches to ACEF and BE's utility drops to 0. Lying never helps, and overstating its cost can lose BE its place on the path.
- **CE (off the path, true cost 3):** For declared costs ≥ 2, ABEF stays selected and CE's utility stays at 0. Declaring below 2 makes ACEF the cheapest path. CE is then paid 5 − 3 = 2, but its true cost is 3, so its utility is −1. Underbidding to win only loses money.
- The same sweep over all 8 edges finds that the **maximum gain from any misreport is 0** for every edge. This matches the book's result that truth-telling is a dominant strategy under VCG.

Ties are broken alphabetically by path name. When CE declares exactly 2, ABEF and ACEF both cost 5, and ABEF is chosen.
