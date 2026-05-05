# REPORT STATUS

## Trạng thái hiện tại của dự án

### Đã hoàn thành
- Cài đặt 3 thuật toán CVRP:
  - Greedy (Nearest Neighbor có xét capacity)
  - Clarke-Wright Savings
  - Sweep + 2-opt
- Có pipeline benchmark đầy đủ:
  - Đo `time_ms`
  - Tính `cost`
  - Kiểm tra `valid_capacity`
- Đã sinh output trực quan:
  - `results.csv`
  - `time_line_chart.png`
  - `cost_bar_chart_*.png`
  - `routes_*.png`
- Đã tích hợp đọc CVRPLIB từ thư mục `Vrp-All`.
- Đã lọc chỉ chạy các bộ có `NODE_COORD_SECTION` để ổn định parser hiện tại.

### Điểm cần lưu ý
- Một số bộ CVRPLIB dạng `EDGE_WEIGHT_SECTION` (EXPLICIT) chưa được parse.
- Đây không ảnh hưởng workflow hiện tại vì đã lọc bộ dữ liệu tương thích.

### Kết quả xác minh gần nhất
- Chạy `python run_experiments.py` thành công.
- `outputs/results.csv` có cả case random và case `cvrplib_Vrp-All_*`.
- Các dòng kiểm tra hiện thấy `valid_capacity=True`.
