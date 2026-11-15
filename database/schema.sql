-- 1. Tạo Cơ sở dữ liệu tuyển dụng
CREATE DATABASE IF NOT EXISTS du_lieu_tuyendung CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE du_lieu_tuyendung;

-- 2. Bảng Người dùng (Tài khoản Ứng viên & Nhà tuyển dụng)
CREATE TABLE IF NOT EXISTS nguoi_dung (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ten_dang_nhap VARCHAR(50) UNIQUE NOT NULL,
    mat_khau VARCHAR(255) NOT NULL,
    ho_ten VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    vai_tro VARCHAR(20) NOT NULL, -- 'ung_vien' hoặc 'nha_tuyen_dung'
    so_dien_thoai VARCHAR(20),
    dia_diem VARCHAR(100),
    vi_tri_mong_muon VARCHAR(100),
    ky_nang TEXT,
    kinh_nghiem VARCHAR(100),
    tom_tat TEXT,
    ten_file_cv VARCHAR(255)
);

-- 3. Bảng Bài đăng tuyển dụng
CREATE TABLE IF NOT EXISTS bai_dang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tieu_de VARCHAR(255) NOT NULL,
    ten_cong_ty VARCHAR(255) NOT NULL,
    ten_dang_nhap_ntd VARCHAR(50) NOT NULL,
    dia_diem VARCHAR(200) NOT NULL,
    nganh_nghe VARCHAR(100) NOT NULL,
    muc_luong VARCHAR(100),
    ky_nang_yeu_cau VARCHAR(255),
    mo_ta TEXT,
    ngay_dang DATE,
    FOREIGN KEY (ten_dang_nhap_ntd) REFERENCES nguoi_dung(ten_dang_nhap) ON DELETE CASCADE
);

-- 4. Bảng Đơn ứng tuyển
CREATE TABLE IF NOT EXISTS don_ung_tuyen (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_bai_dang INT NOT NULL,
    ten_dang_nhap_ung_vien VARCHAR(50) NOT NULL,
    ten_dang_nhap_ntd VARCHAR(50) NOT NULL,
    diem_phu_hop INT DEFAULT 0,
    trang_thai VARCHAR(50) DEFAULT 'Chờ xử lý',
    ngay_ung_tuyen DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_bai_dang) REFERENCES bai_dang(id) ON DELETE CASCADE,
    FOREIGN KEY (ten_dang_nhap_ung_vien) REFERENCES nguoi_dung(ten_dang_nhap) ON DELETE CASCADE,
    FOREIGN KEY (ten_dang_nhap_ntd) REFERENCES nguoi_dung(ten_dang_nhap) ON DELETE CASCADE
);

-- 5. Bảng Tin nhắn (Trò chuyện trực tiếp 1-1 theo từng đơn)
CREATE TABLE IF NOT EXISTS tin_nhan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_don INT NOT NULL,
    nguoi_gui VARCHAR(50) NOT NULL,
    noi_dung TEXT NOT NULL,
    thoi_gian DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_don) REFERENCES don_ung_tuyen(id) ON DELETE CASCADE,
    FOREIGN KEY (nguoi_gui) REFERENCES nguoi_dung(ten_dang_nhap) ON DELETE CASCADE
);
