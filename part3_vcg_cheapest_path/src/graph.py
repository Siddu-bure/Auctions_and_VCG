"""The transportation network of Figure 7.3 (Shoham & Leyton-Brown) and path search.

Each edge is a selfish agent; its number is its private cost.  Edges are directed as drawn.
"""
import numpy as np

TRUE_COST = {"AB": 3, "AC": 2, "BD": 2, "BE": 1, "CE": 3, "CF": 5, "DF": 2, "EF": 1}
SOURCE, TARGET = "A", "F"

# Node layout used only for drawing the network
NODE_POS = {"A": (0, 1), "B": (1, 2), "C": (1, 0), "D": (2, 2), "E": (2, 0), "F": (3, 1)}


def path_name(path):
    """('AB', 'BE', 'EF') -> 'ABEF'."""
    return path[0][0] + "".join(e[1] for e in path) if path else "-"


def all_paths(edges, src=SOURCE, dst=TARGET):
    """Every simple src -> dst path, as tuples of edge names (the graph is tiny, so enumerate)."""
    out_edges = {}
    for e in edges:
        out_edges.setdefault(e[0], []).append(e)
    paths, stack = [], [(src, ())]
    while stack:
        node, path = stack.pop()
        if node == dst:
            paths.append(path)
            continue
        visited = {src} | {e[1] for e in path}
        for e in out_edges.get(node, []):
            if e[1] not in visited:
                stack.append((e[1], path + (e,)))
    return paths


def cheapest_path(costs, exclude=None):
    """Cheapest path under `costs`, optionally with edge `exclude` removed.
    Ties are broken deterministically by path name (alphabetical)."""
    paths = all_paths([e for e in costs if e != exclude])
    if not paths:
        return None, np.inf
    best = min(paths, key=lambda p: (sum(costs[e] for e in p), path_name(p)))
    return best, sum(costs[e] for e in best)
