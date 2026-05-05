from pathlib import Path
from cvrp_core import Customer, CVRPInstance


def parse_cvrplib(path: str | Path) -> tuple[str, CVRPInstance]:
    p = Path(path)
    lines = [line.strip() for line in p.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]

    name = p.stem
    capacity = None
    coords: dict[int, tuple[float, float]] = {}
    demands: dict[int, int] = {}
    depot_id = None

    mode = None
    for line in lines:
        if line.startswith("NAME"):
            name = line.split(":", 1)[-1].strip()
        elif line.startswith("CAPACITY"):
            capacity = int(line.split(":", 1)[-1].strip())
        elif line == "NODE_COORD_SECTION":
            mode = "coord"
            continue
        elif line == "DEMAND_SECTION":
            mode = "demand"
            continue
        elif line == "DEPOT_SECTION":
            mode = "depot"
            continue
        elif line == "EOF":
            break
        elif ":" in line:
            continue
        else:
            if mode == "coord":
                parts = line.split()
                if len(parts) >= 3:
                    i = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    coords[i] = (x, y)
            elif mode == "demand":
                parts = line.split()
                if len(parts) >= 2:
                    i = int(parts[0])
                    d = int(parts[1])
                    demands[i] = d
            elif mode == "depot":
                parts = line.split()
                if parts and parts[0] != "-1":
                    depot_id = int(parts[0])

    if capacity is None:
        raise ValueError(f"Missing CAPACITY in {p}")
    if depot_id is None:
        depot_id = min(coords.keys()) if coords else None
    if depot_id not in coords:
        raise ValueError(f"Depot id {depot_id} missing in NODE_COORD_SECTION")

    depot_xy = coords[depot_id]
    depot = Customer(0, depot_xy[0], depot_xy[1], 0)

    customers = []
    idx = 1
    for node_id in sorted(coords.keys()):
        if node_id == depot_id:
            continue
        x, y = coords[node_id]
        demand = demands.get(node_id, 0)
        customers.append(Customer(idx, x, y, demand))
        idx += 1

    instance = CVRPInstance(depot=depot, customers=customers, capacity=capacity)
    return name, instance
