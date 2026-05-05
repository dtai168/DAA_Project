from dataclasses import dataclass
from math import hypot


@dataclass
class Customer:
    idx: int
    x: float
    y: float
    demand: int


@dataclass
class CVRPInstance:
    depot: Customer
    customers: list[Customer]
    capacity: int

    def all_nodes(self) -> list[Customer]:
        return [self.depot] + self.customers


def distance(a: Customer, b: Customer) -> float:
    return hypot(a.x - b.x, a.y - b.y)


def distance_matrix(instance: CVRPInstance) -> list[list[float]]:
    nodes = instance.all_nodes()
    n = len(nodes)
    mat = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = distance(nodes[i], nodes[j])
            mat[i][j] = d
            mat[j][i] = d
    return mat


def route_cost(route: list[int], dist: list[list[float]]) -> float:
    cost = 0.0
    for i in range(len(route) - 1):
        cost += dist[route[i]][route[i + 1]]
    return cost


def total_cost(routes: list[list[int]], dist: list[list[float]]) -> float:
    return sum(route_cost(r, dist) for r in routes)


def validate_capacity(routes: list[list[int]], instance: CVRPInstance) -> bool:
    demand = {c.idx: c.demand for c in instance.customers}
    for route in routes:
        load = sum(demand.get(node, 0) for node in route)
        if load > instance.capacity:
            return False
    return True
