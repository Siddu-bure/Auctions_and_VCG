# Part 3 — VCG mechanism for the cheapest A→F path (Figure 7.3)

Run from the project root: `python3 part3_vcg_cheapest_path/run_part3.py`

## Code (`src/`)
| file | what it does |
|---|---|
| `graph.py` | Edge costs from Figure 7.3 (AB 3, AC 2, BD 2, BE 1, CE 3, CF 5, DF 2, EF 1), listing of all paths, and the cheapest-path search (optionally with one edge removed) |
| `vcg.py` | `vcg()` picks the path and each edge's payment. `misreport_sweep()` gives one edge's utility for each cost it might declare |
| `plots.py` | Network drawing, misreport plot for a single edge, and the all-edges comparison |
| `../run_part3.py` | Checks the payments against the book, runs the sweeps and writes `results/` and `figures/` |

## Outputs (numbered in reading order)
| # | table | figure |
|---|---|---|
| 1 | `results/1_vcg_payments.txt`: path ABEF; AB paid 4, BE 2, EF 3, all others 0 | `figures/1_network_chosen_path.png` |
| 2 | `results/2_misreport_BE_on_path.txt`: edge on the path | `figures/2_misreport_BE_on_path.png` |
| 3 | `results/3_misreport_CE_off_path.txt`: edge off the path | `figures/3_misreport_CE_off_path.png` |
| 4 | `results/4_misreport_all_edges.txt`: every edge | `figures/4_misreport_all_edges.png` |

**Result:** no edge gains from any misreport between 0 and 10. The answers are explained in the main [README](../README.md#part-3--vcg-for-the-cheapest-af-path-figure-73).
