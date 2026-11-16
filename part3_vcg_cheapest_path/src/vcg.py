"""VCG mechanism for buying a path, and the misreporting experiment.

Edge e's value for a path is -c_e if e is used, else 0.  VCG picks the cheapest path under
the declared costs and pays each edge

    payment(e) = cost of best path without e  -  (declared cost of chosen path - e's declared cost)

This is 0 for edges off the chosen path.  (The book writes p_e as what e pays, i.e. -payment.)
Utility of an edge = payment - true cost if its edge is used, else payment.
"""
import numpy as np

from .graph import TRUE_COST, cheapest_path, path_name


def vcg(declared):
    """Return (chosen path, its declared cost, {edge: payment to edge})."""
    path, total = cheapest_path(declared)
    payment = {}
    for e in declared:
        if e in path:
            _, cost_without_e = cheapest_path(declared, exclude=e)
            payment[e] = cost_without_e - (total - declared[e])
        else:
            payment[e] = 0.0  # not pivotal: the chosen path is the same with or without e
    return path, total, payment


def misreport_sweep(edge, reports, true_cost=TRUE_COST):
    """Utility of `edge` (true cost fixed) for each declared cost in `reports`;
    every other edge reports truthfully.  Returns (utilities, chosen path names)."""
    utilities, chosen = [], []
    for r in reports:
        declared = dict(true_cost, **{edge: float(r)})
        path, _, payment = vcg(declared)
        used = edge in path
        utilities.append(payment[edge] - (true_cost[edge] if used else 0))
        chosen.append(path_name(path))
    return np.array(utilities), chosen


def truthful_index(edge, reports):
    return int(np.argmin(np.abs(np.asarray(reports) - TRUE_COST[edge])))
