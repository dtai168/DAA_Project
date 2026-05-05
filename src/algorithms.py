from math import atan2
from cvrp_core import CVRPInstance, distance_matrix


def greedy_nearest_neighbor(instance: CVRPInstance) -> list[list[int]]:
    dist = distance_matrix(instance)
    unserved = set(c.idx for c in instance.customers)
    demand = {c.idx: c.demand for c in instance.customers}
    routes = []

    while unserved:
        route = [0]
        load = 0
        current = 0
        while True:
            candidates = [
                u for u in unserved if load + demand[u] <= instance.capacity
            ]
            if not candidates:
                break
            nxt = min(candidates, key=lambda u: dist[current][u])
            route.append(nxt)
            load += demand[nxt]
            unserved.remove(nxt)
            current = nxt
        route.append(0)
        routes.append(route)
    return routes


def clarke_wright_savings(instance: CVRPInstance) -> list[list[int]]:
    dist = distance_matrix(instance)
    demand = {c.idx: c.demand for c in instance.customers}

    routes = {c.idx: [0, c.idx, 0] for c in instance.customers}
    route_load = {c.idx: demand[c.idx] for c in instance.customers}
    owner = {c.idx: c.idx for c in instance.customers}

    savings = []
    ids = [c.idx for c in instance.customers]
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            s = dist[0][a] + dist[0][b] - dist[a][b]
            savings.append((s, a, b))
    savings.sort(reverse=True)

    for _, i, j in savings:
        ri = owner[i]
        rj = owner[j]
        if ri == rj:
            continue

        route_i = routes[ri]
        route_j = routes[rj]

        i_is_end = route_i[-2] == i
        i_is_start = route_i[1] == i
        j_is_end = route_j[-2] == j
        j_is_start = route_j[1] == j

        if not ((i_is_end or i_is_start) and (j_is_end or j_is_start)):
            continue

        if route_load[ri] + route_load[rj] > instance.capacity:
            continue

        seq_i = route_i[1:-1]
        seq_j = route_j[1:-1]

        if i_is_start:
            seq_i = list(reversed(seq_i))
        if j_is_end:
            seq_j = list(reversed(seq_j))

        merged = [0] + seq_i + seq_j + [0]

        routes[ri] = merged
        route_load[ri] += route_load[rj]

        for node in seq_j:
            owner[node] = ri

        del routes[rj]
        del route_load[rj]

    return list(routes.values())


def _two_opt(route: list[int], dist: list[list[float]]) -> list[int]:
    best = route[:]
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best) - 1):
                if j - i == 1:
                    continue
                cand = best[:]
                cand[i:j] = reversed(best[i:j])
                old_cost = sum(dist[best[k]][best[k + 1]] for k in range(len(best) - 1))
                new_cost = sum(dist[cand[k]][cand[k + 1]] for k in range(len(cand) - 1))
                if new_cost < old_cost:
                    best = cand
                    improved = True
    return best


def sweep_algorithm(instance: CVRPInstance, use_two_opt: bool = True) -> list[list[int]]:
    dist = distance_matrix(instance)
    demand = {c.idx: c.demand for c in instance.customers}
    customers = sorted(
        instance.customers,
        key=lambda c: atan2(c.y - instance.depot.y, c.x - instance.depot.x)
    )

    routes = []
    current_nodes = []
    current_load = 0

    for c in customers:
        if current_load + c.demand <= instance.capacity:
            current_nodes.append(c.idx)
            current_load += c.demand
        else:
            route = [0] + current_nodes + [0]
            if use_two_opt and len(route) > 4:
                route = _two_opt(route, dist)
            routes.append(route)
            current_nodes = [c.idx]
            current_load = c.demand

    if current_nodes:
        route = [0] + current_nodes + [0]
        if use_two_opt and len(route) > 4:
            route = _two_opt(route, dist)
        routes.append(route)

    return routes
