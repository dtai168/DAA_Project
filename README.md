# DAA Project - CVRP (Greedy, Clarke-Wright, Sweep)

## Cài đặt
```bash
pip install -r requirements.txt
```

## Chạy benchmark toàn bộ
```bash
python run_experiments.py
```

Kết quả sẽ được lưu trong `outputs/`:
- `results.csv`
- `time_line_chart.png`
- `cost_bar_chart_*.png`
- `routes_*.png` (mỗi bộ test x mỗi thuật toán)

Các bộ test mặc định (random generation):
- `small_20`
- `medium_50`
- `medium_75`
- `large_200`

Hỗ trợ thêm bộ test chuẩn CVRPLIB:
- Đặt file `.vrp` vào thư mục `datasets/` (có thể tạo thư mục con).
- Khi chạy `python run_experiments.py`, hệ thống sẽ tự parse và benchmark cùng với các case random.
- Tên case trong kết quả sẽ có tiền tố `cvrplib_`.

## Cấu trúc
- `src/cvrp_core.py`: cấu trúc dữ liệu CVRP + tính cost
- `src/algorithms.py`: 3 thuật toán Greedy / Clarke-Wright / Sweep
- `src/data_gen.py`: sinh dữ liệu test random
- `src/benchmark.py`: chạy benchmark và lưu kết quả
- `src/visualize.py`: vẽ biểu đồ và route
- `run_experiments.py`: entrypoint chạy toàn bộ pipeline
