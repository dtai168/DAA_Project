from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def plot_routes(instance, routes: list[list[int]], title: str, output_path: Path):
    node_xy = {0: (instance.depot.x, instance.depot.y)}
    for c in instance.customers:
        node_xy[c.idx] = (c.x, c.y)

    plt.figure(figsize=(8, 6))
    depot_x, depot_y = node_xy[0]
    plt.scatter([depot_x], [depot_y], c="red", marker="s", s=80, label="Depot")

    for i, route in enumerate(routes):
        xs = [node_xy[n][0] for n in route]
        ys = [node_xy[n][1] for n in route]
        plt.plot(xs, ys, marker="o", linewidth=1.5, label=f"Route {i+1}")

    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend(fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_time_line(df: pd.DataFrame, output_dir: Path):
    plt.figure(figsize=(8, 5))
    for algo in df["algorithm"].unique():
        sub = df[df["algorithm"] == algo].sort_values("n_customers")
        plt.plot(sub["n_customers"], sub["time_ms"], marker="o", label=algo)
    plt.xlabel("So luong khach hang")
    plt.ylabel("Thoi gian chay (ms)")
    plt.title("So sanh thoi gian chay")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "time_line_chart.png", dpi=200)
    plt.close()


def plot_cost_bars(df: pd.DataFrame, output_dir: Path):
    for case in df["case"].unique():
        sub = df[df["case"] == case]
        plt.figure(figsize=(6, 4))
        plt.bar(sub["algorithm"], sub["cost"])
        plt.xlabel("Thuat toan")
        plt.ylabel("Tong quang duong")
        plt.title(f"So sanh cost - {case}")
        plt.tight_layout()
        safe = case.replace(" ", "_")
        plt.savefig(output_dir / f"cost_bar_chart_{safe}.png", dpi=200)
        plt.close()
