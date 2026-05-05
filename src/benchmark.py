import time
import pandas as pd

from cvrp_core import distance_matrix, total_cost, validate_capacity
from algorithms import greedy_nearest_neighbor, clarke_wright_savings, sweep_algorithm


def run_one(instance, algo_name: str):
    start = time.perf_counter()
    if algo_name == "Greedy":
        routes = greedy_nearest_neighbor(instance)
    elif algo_name == "Clarke-Wright":
        routes = clarke_wright_savings(instance)
    elif algo_name == "Sweep":
        routes = sweep_algorithm(instance, use_two_opt=True)
    else:
        raise ValueError(algo_name)
    end = time.perf_counter()

    dist = distance_matrix(instance)
    cost = total_cost(routes, dist)
    ok = validate_capacity(routes, instance)

    return {
        "algorithm": algo_name,
        "time_ms": (end - start) * 1000,
        "cost": cost,
        "valid_capacity": ok,
        "vehicles": len(routes),
        "routes": routes,
    }


def run_benchmark(instances: list[tuple[str, object]]) -> pd.DataFrame:
    rows = []
    for case_name, instance in instances:
        for algo in ["Greedy", "Clarke-Wright", "Sweep"]:
            result = run_one(instance, algo)
            rows.append({
                "case": case_name,
                "n_customers": len(instance.customers),
                "algorithm": result["algorithm"],
                "time_ms": result["time_ms"],
                "cost": result["cost"],
                "valid_capacity": result["valid_capacity"],
                "vehicles": result["vehicles"],
            })
    return pd.DataFrame(rows)
