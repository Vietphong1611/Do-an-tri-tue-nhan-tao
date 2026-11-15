# 💼 CareerLink AI Portal - Hệ Thống Tìm Kiếm Việc Làm & Tuyển Dụng Thông Minh

Đồ án xây dựng nền tảng kết nối **Ứng viên** và **Nhà tuyển dụng** bằng Python (NiceGUI) và MySQL, tích hợp thuật toán **AI Matching đa tiêu chí** nhằm tự động đánh giá mức độ phù hợp giữa hồ sơ năng lực (CV) của ứng viên với yêu cầu tuyển dụng.

---

## 📁 Cấu trúc thư mục dự án

```text
Do-an-tri-tue-nhan-tao/
├── src/
│   └── main.py            # Mã nguồn chính (Giao diện Web NiceGUI, AI Matching, Chat Box)
├── database.sql           # Script khởi tạo CSDL MySQL & dữ liệu mẫu
├── requirements.txt       # Danh sách các thư viện Python cần thiết
├── .gitignore             # Cấu hình loại bỏ file tạm/môi trường ảo
└── README.md              # Tài liệu hướng dẫn và giới thiệu đồ án
```

---

## 🚀 Tính năng nổi bật

- **Phân quyền người dùng:** Đăng ký và đăng nhập tách biệt cho **Ứng viên** (`ung_vien`) và **Nhà tuyển dụng** (`nha_tuyen_dung`).
- **Gợi ý & Chấm điểm AI Matching:** Tự động tính toán phần trăm độ phù hợp của từng công việc với hồ sơ CV của ứng viên và sắp xếp ưu tiên từ cao xuống thấp.
- **Tìm kiếm & Lọc đa điều kiện:** Lọc danh sách việc làm theo vị trí, địa điểm, từ khóa kỹ năng và ngưỡng % độ khớp AI (`≥ 50%`, `≥ 70%`, `≥ 90%`).
- **Quản lý CV & Tin tuyển dụng:**
  - **Ứng viên:** Cập nhật hồ sơ CV trực tuyến (`/cv-edit`), xem chi tiết công việc (`/job/{id}`) và nộp hồ sơ trực tiếp.
  - **Nhà tuyển dụng:** Đăng bài tuyển dụng mới (`/post-job`) lưu trực tiếp vào MySQL.
- **Chat Box Tuyển Dụng 1-1 (Real-time):** Cửa sổ chat nổi góc màn hình giúp ứng viên và nhà tuyển dụng trao đổi trực tiếp theo từng đơn ứng tuyển.

---

## 🧠 Thuật toán AI Matching đa tiêu chí

Hệ thống đánh giá mức độ tương thích giữa CV ứng viên và tin tuyển dụng dựa trên mô hình tính điểm trọng số:

$$\text{Tổng điểm (\%)} = (S_{\text{kỹ năng}} \times 0.6) + (S_{\text{vị trí}} \times 0.2) + (S_{\text{địa điểm}} \times 0.2)$$

- **Kỹ năng chuyên môn (60%):** Đối chiếu tập kỹ năng trong CV với danh sách kỹ năng yêu cầu của nhà tuyển dụng.
- **Vị trí mong muốn (20%):** So khớp chức danh mục tiêu của ứng viên với tiêu đề bài đăng.
- **Địa điểm làm việc (20%):** Đánh giá mức độ trùng khớp khu vực địa lý giữa ứng viên và nơi làm việc.

---

## 🗄️ Thiết kế Cơ sở dữ liệu (`du_lieu_tuyendung`)

Hệ thống sử dụng **MySQL Workbench** gồm 4 bảng quan hệ chính:
1. `nguoi_dung`: Lưu trữ thông tin tài khoản, vai trò và hồ sơ CV ứng viên.
2. `bai_dang`: Lưu trữ danh sách tin tuyển dụng của các doanh nghiệp.
3. `don_ung_tuyen`: Quản lý lịch sử ứng tuyển, điểm AI Match và trạng thái duyệt hồ sơ.
4. `tin_nhan`: Lưu trữ nội dung hội thoại trực tiếp 1-1 gắn với từng đơn ứng tuyển.

---

## ⚙️ Hướng dẫn cài đặt & Chạy dự án

### 1. Khởi tạo Cơ sở dữ liệu MySQL
1. Mở **MySQL Workbench** và kết nối tới Local Server.
2. Mở file `database.sql` trong dự án và nhấn **Execute (⚡)** để tạo database `du_lieu_tuyendung` cùng dữ liệu mẫu.
3. Kiểm tra cấu hình `DB_CONFIG` trong `src/main.py` (mặc định `user='root'`, `password='123456'`).

### 2. Cài đặt thư viện Python
```bash
pip install -r requirements.txt
```

### 3. Khởi chạy ứng dụng
```bash
python src/main.py
```
Sau khi chạy thành công, mở trình duyệt và truy cập địa chỉ: **`http://localhost:8080`**

---

## 🔑 Tài khoản Demo có sẵn

| Vai trò | Tên đăng nhập | Mật khẩu | Ghi chú |
| :--- | :--- | :--- | :--- |
| **Ứng viên** | `ungvien_demo` | `123456` | Có sẵn kỹ năng Python, SQL, FastAPI & đơn ứng tuyển mẫu |
| **Nhà tuyển dụng (FPT)** | `fpt_software` | `123456` | Có sẵn tin tuyển dụng & tin nhắn mẫu từ ứng viên |
| **Nhà tuyển dụng (VNG)** | `vng_corp` | `123456` | Tài khoản doanh nghiệp mẫu |
