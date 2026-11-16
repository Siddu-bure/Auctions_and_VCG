"""Part 3 entry point: VCG mechanism for the cheapest A -> F path (Figure 7.3).

Usage:  python3 part3_vcg_cheapest_path/run_part3.py
Writes tables to results/ and plots to figures/ (both inside this folder).
"""
import os

import numpy as np

from src.graph import TRUE_COST, cheapest_path, path_name
from src.plots import save_all_edges, save_network, save_sweep
from src.vcg import misreport_sweep, truthful_index, vcg

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
FIGURES = os.path.join(HERE, "figures")

REPORTS = np.round(np.arange(0, 10.5, 0.5), 1)  # misreported costs 0, 0.5, ..., 10
PICKED = {"BE": "on the chosen path", "CE": "off the chosen path"}
BOOK_PAYMENTS = {"AB": 4, "BE": 2, "EF": 3}  # every other edge: 0


def report(text, filename):
    print(text + "\n")
    with open(os.path.join(RESULTS, filename), "w") as f:
        f.write(text + "\n")


def payments_table():
    path, total, payment = vcg(TRUE_COST)
    title = "Part 3 - VCG payments with truthful costs"
    lines = [title, "=" * len(title), f"Chosen path: {path_name(path)} (cost {total})", "",
             f"{'edge':>5} {'cost':>5} {'on path':>8} {'best w/o e':>11} {'paid':>5} {'utility':>8}"]
    for e, c in TRUE_COST.items():
        p_wo, c_wo = cheapest_path(TRUE_COST, exclude=e)
        on = e in path
        lines.append(f"{e:>5} {c:>5} {str(on):>8} {path_name(p_wo) + f' ({c_wo:g})':>11} "
                     f"{payment[e]:>5g} {payment[e] - (c if on else 0):>8g}")
    ok = path_name(path) == "ABEF" and all(payment[e] == BOOK_PAYMENTS.get(e, 0) for e in TRUE_COST)
    lines.append("\n" + ("MATCHES THE BOOK: path ABEF, AB paid 4, BE paid 2, EF paid 3, others 0." if ok
                         else "DOES NOT MATCH THE BOOK"))
    assert ok, "payments differ from the book"
    return "\n".join(lines), path, payment


def sweep_table(edge, where, utilities, chosen):
    t = truthful_index(edge, REPORTS)
    title = f"Edge {edge} ({where}), true cost {TRUE_COST[edge]} - misreport sweep"
    lines = [title, "=" * len(title), f"truthful utility = {utilities[t]:g}", "",
             f"{'report':>7} {'path':>6} {'utility':>8} {'change vs truth':>16}"]
    for r, u, s in zip(REPORTS, utilities, chosen):
        lines.append(f"{r:>7.1f} {s:>6} {u:>8g} {u - utilities[t]:>16g}")
    lines.append(f"\nmax gain from lying: {utilities.max() - utilities[t]:g}")
    return "\n".join(lines)


def main():
    os.makedirs(RESULTS, exist_ok=True)
    os.makedirs(FIGURES, exist_ok=True)

    text, path, payment = payments_table()
    report(text, "1_vcg_payments.txt")
    save_network(path, payment, os.path.join(FIGURES, "1_network_chosen_path.png"))

    sweeps = {e: misreport_sweep(e, REPORTS) for e in TRUE_COST}

    for i, (edge, where) in enumerate(PICKED.items(), start=2):
        u, chosen = sweeps[edge]
        report(sweep_table(edge, where, u, chosen), f"{i}_misreport_{edge}_{where.split()[0]}_path.txt")
        save_sweep(edge, where, REPORTS, u, chosen,
                   os.path.join(FIGURES, f"{i}_misreport_{edge}_{where.split()[0]}_path.png"))

    title = "All edges - maximum gain from any misreport in [0, 10] (should be <= 0)"
    lines = [title, "=" * len(title)]
    for e, (u, _) in sweeps.items():
        lines.append(f"  {e}: {u.max() - u[truthful_index(e, REPORTS)]:g}")
    report("\n".join(lines), "4_misreport_all_edges.txt")
    save_all_edges(REPORTS, sweeps, os.path.join(FIGURES, "4_misreport_all_edges.png"))


if __name__ == "__main__":
    main()
