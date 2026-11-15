# 💼 CareerLink AI Portal - Hệ Thống Tìm Kiếm Việc Làm & Tuyển Dụng Thông Minh

Đồ án xây dựng nền tảng kết nối Ứng viên và Nhà tuyển dụng tích hợp thuật toán **AI Matching đa tiêu chí** để đánh giá tự động mức độ phù hợp giữa CV ứng viên và yêu cầu công việc.

## 🚀 Tính năng nổi bật

- **Phân quyền tài khoản:** Đăng ký / Đăng nhập riêng biệt cho **Ứng viên** (`ung_vien`) và **Nhà tuyển dụng** (`nha_tuyen_dung`).
- **Thuật toán AI Matching đa tiêu chí:** Tính điểm % phù hợp tự động dựa trên 3 trọng số:
  - 🛠️ **Kỹ năng chuyên môn:** 60%
  - 🎯 **Vị trí công việc mong muốn:** 20%
  - 📍 **Địa điểm làm việc:** 20%
- **Tìm kiếm & Lọc thông minh:** Lọc việc làm theo vị trí, địa điểm, từ khóa kỹ năng và ngưỡng % độ khớp AI (`≥ 50%`, `≥ 70%`, `≥ 90%`).
- **Quản lý Hồ sơ & Tin tuyển dụng:**
  - Ứng viên cập nhật hồ sơ CV trực tuyến (`/cv-edit`) và ứng tuyển trực tiếp tại trang chi tiết việc làm (`/job/{id}`).
  - Nhà tuyển dụng đăng bài tuyển dụng mới (`/post-job`).
- **Chat Box Tuyển Dụng 1-1 (Real-time):** Cửa sổ chat nổi góc màn hình cho phép ứng viên và nhà tuyển dụng trao đổi trực tiếp theo từng đơn ứng tuyển.

## 🛠️ Công nghệ sử dụng

- **Ngôn ngữ:** Python 3.x
- **Giao diện Web (Frontend & Backend):** NiceGUI
- **Cơ sở dữ liệu:** MySQL Workbench (`du_lieu_tuyendung`)

## ⚙️ Hướng dẫn cài đặt & Chạy dự án

### 1. Khởi tạo Cơ sở dữ liệu MySQL
1. Mở **MySQL Workbench** và kết nối tới Local Server.
2. Mở file `database.sql` trong dự án và nhấn **Execute (⚡)** để tạo database `du_lieu_tuyendung` cùng dữ liệu mẫu.
3. Kiểm tra thông số kết nối `DB_CONFIG` trong `main.py` (mặc định `user='root'`, `password='123456'`).

### 2. Cài đặt thư viện Python
```bash
pip install -r requirements.txt
