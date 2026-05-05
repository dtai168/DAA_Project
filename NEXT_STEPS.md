# NEXT STEPS

## 1) Hoàn thiện báo cáo sơ bộ
- Dùng file `report.tex` (hoặc nội dung LaTeX mình đã gửi) để viết 2 phần:
  - Đặt bài toán CVRP (hàm mục tiêu + ràng buộc tải trọng)
  - Cơ sở lý thuyết 3 thuật toán: Greedy, Clarke-Wright, Sweep
- Xuất PDF để nộp bản sơ bộ.

## 2) Hoàn thiện báo cáo cuối
- Bổ sung phần thực nghiệm từ `outputs/results.csv`.
- Chèn các biểu đồ:
  - `outputs/time_line_chart.png`
  - `outputs/cost_bar_chart_*.png`
  - `outputs/routes_*.png`
- Viết nhận xét so sánh time/cost giữa 3 thuật toán.

## 3) Nếu cần mở rộng kỹ thuật
- Hiện tại pipeline CVRPLIB đang lọc các file có `NODE_COORD_SECTION`.
- Nếu giảng viên yêu cầu thêm bộ `EXPLICIT/EDGE_WEIGHT_SECTION`, cần nâng parser trong `src/data_io.py`.

## 4) Trước khi nộp
- Chạy lại toàn bộ benchmark để đảm bảo kết quả mới nhất.
- Soát lại tên hình/bảng trong báo cáo trùng đúng file thực tế.
