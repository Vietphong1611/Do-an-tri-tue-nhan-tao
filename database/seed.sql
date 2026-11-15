USE du_lieu_tuyendung;

-- 1. Tạo các tài khoản Nhà tuyển dụng mẫu (tránh lỗi khóa ngoại FOREIGN KEY)
INSERT IGNORE INTO nguoi_dung (ten_dang_nhap, mat_khau, ho_ten, email, vai_tro) VALUES
('fpt_software', '123456', 'Công ty FPT Software', 'recruitment@fpt.com', 'nha_tuyen_dung'),
('vng_corp', '123456', 'Tập đoàn VNG', 'hr@vng.com.vn', 'nha_tuyen_dung'),
('viettel_group', '123456', 'Tập đoàn Viettel', 'tuyendung@viettel.com.vn', 'nha_tuyen_dung'),
('shopee_vn', '123456', 'Shopee Việt Nam', 'careers@shopee.vn', 'nha_tuyen_dung');

-- 2. Thêm danh sách bài đăng tuyển dụng mẫu
INSERT INTO bai_dang (tieu_de, ten_cong_ty, ten_dang_nhap_ntd, dia_diem, nganh_nghe, muc_luong, ky_nang_yeu_cau, mo_ta, ngay_dang) VALUES
(
    'Lập trình viên Senior Python / FastAPI',
    'Công ty FPT Software',
    'fpt_software',
    'Đà Nẵng (Khu công nghệ cao)',
    'Công nghệ thông tin',
    '20 - 35 triệu',
    'Python, FastAPI, SQL, Docker, Git',
    '### Mô tả công việc:\n- Phát triển các dịch vụ Microservices bằng Python / FastAPI.\n- Tối ưu hóa truy vấn CSDL MySQL, PostgreSQL.\n- Tham gia thiết kế hệ thống và làm việc với Docker/Kubernetes.\n\n### Quyền lợi:\n- Lương tháng 13 + Bonus dự án.\n- BHYT, BHXH đầy đủ và gói bảo hiểm FPT Care.',
    CURDATE()
),
(
    'Kỹ sư Trí tuệ Nhân tạo (AI / Machine Learning Engineer)',
    'Tập đoàn VNG',
    'vng_corp',
    'TP. Hồ Chí Minh (Quận 7)',
    'Trí tuệ nhân tạo',
    '30 - 50 triệu',
    'Python, Machine Learning, TensorFlow, PyTorch, SQL',
    '### Mô tả công việc:\n- Nghiên cứu và triển khai các mô hình Machine Learning / Deep Learning.\n- Xây dựng hệ thống Gợi ý (Recommendation System) và Xử lý ngôn ngữ tự nhiên (NLP).\n\n### Yêu cầu:\n- Thành thạo Python, PyTorch/TensorFlow, CSDL SQL.\n- Có tư duy thuật toán tốt.',
    CURDATE()
),
(
    'Chuyên viên Phân tích Dữ liệu (Data Analyst)',
    'Shopee Việt Nam',
    'shopee_vn',
    'Hà Nội (Cầu Giấy)',
    'Phân tích dữ liệu',
    '18 - 28 triệu',
    'SQL, Python, PowerBI, Excel, Tableau',
    '### Mô tả công việc:\n- Phân tích hành vi người dùng trên sàn thương mại điện tử.\n- Xây dựng dashboard báo cáo trực quan bằng PowerBI / Tableau.\n- Viết các truy vấn SQL nâng cao phục vụ trích xuất dữ liệu.\n\n### Quyền lợi:\n- Môi trường năng động, nhiều cơ hội thăng tiến.\n- Phụ cấp ăn trưa và trang bị Laptop đời mới.',
    CURDATE()
),
(
    'Lập trình viên Frontend (ReactJS / TypeScript)',
    'Tập đoàn Viettel',
    'viettel_group',
    'Hà Nội & Đà Nẵng',
    'Công nghệ thông tin',
    '15 - 25 triệu',
    'ReactJS, TypeScript, HTML, CSS, Git',
    '### Mô tả công việc:\n- Xây dựng giao diện ứng dụng Web đáp ứng responsive.\n- Tích hợp RESTful API từ Backend.\n- Tối ưu hóa hiệu năng trải nghiệm người dùng (UX/UI).\n\n### Yêu cầu:\n- Có tối thiểu 2 năm kinh nghiệm với ReactJS, TypeScript.',
    CURDATE()
),
(
    'Chuyên viên Digital Marketing Executive',
    'Shopee Việt Nam',
    'shopee_vn',
    'TP. Hồ Chí Minh',
    'Marketing / Truyền thông',
    '12 - 18 triệu',
    'Digital Marketing, SEO, Facebook Ads, Google Ads, Content Writing',
    '### Mô tả công việc:\n- Lập kế hoạch và thực thi các chiến dịch quảng cáo Facebook Ads, Google Ads.\n- Tối ưu hóa SEO website và xây dựng nội dung truyền thông.\n- Đo lường và báo cáo chỉ số ROI chiến dịch.',
    CURDATE()
);
