from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent / "src"))

from data_gen import random_instance
from data_io import parse_cvrplib
from benchmark import run_benchmark, run_one
from visualize import plot_time_line, plot_cost_bars, plot_routes


def load_cvrplib_instances(project_root: Path):
    search_dirs = [project_root / "datasets", project_root / "Vrp-All"]

    instances = []
    for base_dir in search_dirs:
        if not base_dir.exists():
            continue
        for vrp_file in sorted(base_dir.rglob("*.vrp")):
            content = vrp_file.read_text(encoding="utf-8", errors="ignore")
            if "NODE_COORD_SECTION" not in content:
                continue
            try:
                name, instance = parse_cvrplib(vrp_file)
                case_name = f"cvrplib_{base_dir.name}_{name}"
                instances.append((case_name, instance))
            except Exception as exc:
                print(f"Bo qua {vrp_file.name}: {exc}")
    return instances


def build_instances(project_root: Path):
    random_cases = [
        ("small_20", random_instance(20, capacity=30, seed=1)),
        ("medium_50", random_instance(50, capacity=40, seed=2)),
        ("medium_75", random_instance(75, capacity=50, seed=3)),
        ("large_200", random_instance(200, capacity=80, seed=4)),
    ]
    cvrplib_cases = load_cvrplib_instances(project_root)
    return random_cases + cvrplib_cases


def main():
    project_root = Path(__file__).parent
    output_dir = project_root / "outputs"
    output_dir.mkdir(exist_ok=True)

    instances = build_instances(project_root)
    if not instances:
        raise RuntimeError("Khong tim thay bo du lieu nao de benchmark")

    df = run_benchmark(instances)
    df.to_csv(output_dir / "results.csv", index=False)

    plot_time_line(df, output_dir)
    plot_cost_bars(df, output_dir)

    for case_name, instance in instances:
        for algo in ["Greedy", "Clarke-Wright", "Sweep"]:
            result = run_one(instance, algo)
            safe_algo = algo.lower().replace("-", "_").replace(" ", "_")
            plot_routes(
                instance,
                result["routes"],
                f"{algo} - {case_name}",
                output_dir / f"routes_{case_name}_{safe_algo}.png",
            )

    print("Hoan tat benchmark. Kiem tra thu muc outputs/.")


if __name__ == "__main__":
    main()
