# ĐỒ ÁN: HỆ THỐNG TUYỂN DỤNG VÀ TÌM KIẾM VIỆC LÀM AI

## I. NHÓM 1: SƠ ĐỒ PHÂN TÍCH YÊU CẦU

### 1. Sơ đồ Use Case
```mermaid
graph LR
    Candidate(("Ứng viên"))

    subgraph System ["HỆ THỐNG TUYỂN DỤNG & TÌM VIỆC AI"]
        direction LR

        subgraph Candidate_UC ["Phân hệ Ứng viên"]
            direction TB
            UC_Auth("Đăng ký / Đăng nhập")
            UC_ManageProfile("Quản lý Hồ sơ cá nhân")
            UC_UploadCV("Tải lên & Quản lý CV")
            UC_ParseCV("Phân tích & Trích xuất CV (AI)")
            UC_SearchJob("Tìm kiếm & Lọc việc làm")
            UC_SuggestJob("Xem gợi ý việc làm từ AI")
            UC_ApplyJob("Nộp đơn ứng tuyển")
            UC_TrackApp("Theo dõi trạng thái ứng tuyển")
        end

        subgraph Recruiter_UC ["Phân hệ Nhà tuyển dụng"]
            direction TB
            UC_ManageCompany("Quản lý Thông tin Công ty")
            UC_ManageJob("Đăng & Quản lý Bài tuyển dụng")
            UC_ViewApp("Xem danh sách ứng viên")
            UC_Matching("Chấm điểm CV - JD (AI)")
            UC_UpdateAppStatus("Cập nhật trạng thái ứng tuyển")
        end

        subgraph Admin_UC ["Phân hệ Quản trị viên"]
            direction TB
            UC_ManageUsers("Quản lý Người dùng")
            UC_ApproveJob("Duyệt bài đăng tuyển dụng")
            UC_ManageCategory("Quản lý Danh mục Ngành nghề")
        end
    end

    Recruiter(("Nhà tuyển dụng"))
    Admin(("Quản trị viên"))
    AIEngine[("Hệ thống AI Engine")]

    Candidate --- UC_Auth
    Candidate --- UC_ManageProfile
    Candidate --- UC_UploadCV
    Candidate --- UC_SearchJob
    Candidate --- UC_SuggestJob
    Candidate --- UC_ApplyJob
    Candidate --- UC_TrackApp

    Recruiter --- UC_Auth
    Recruiter --- UC_ManageCompany
    Recruiter --- UC_ManageJob
    Recruiter --- UC_ViewApp
    Recruiter --- UC_UpdateAppStatus

    Admin --- UC_Auth
    Admin --- UC_ManageUsers
    Admin --- UC_ApproveJob
    Admin --- UC_ManageCategory

    UC_UploadCV -. "<<include>>" .-> UC_ParseCV
    UC_ViewApp -. "<<include>>" .-> UC_Matching

    UC_ParseCV <==> AIEngine
    UC_SuggestJob <==> AIEngine
    UC_Matching <==> AIEngine
```

---

## II. NHÓM 2: THIẾT KẾ CSDL VÀ KIẾN TRÚC

### 1. Sơ đồ ERD (Entity-Relationship Diagram)
```mermaid
erDiagram
    USERS {
        int user_id PK
        string email
        string password_hash
        string full_name
        string role
    }

    CANDIDATES {
        int candidate_id PK
        int user_id FK
        string title
        string skills_list
    }

    RESUMES {
        int resume_id PK
        int candidate_id FK
        string file_url
        text parsed_content
    }

    COMPANIES {
        int company_id PK
        int recruiter_id FK
        string company_name
        string location
    }

    JOB_POSTS {
        int job_id PK
        int company_id FK
        string title
        text requirements
    }

    APPLICATIONS {
        int application_id PK
        int job_id FK
        int candidate_id FK
        int resume_id FK
        float matching_score
    }

    USERS ||--o| CANDIDATES : "is"
    USERS ||--o{ COMPANIES : "manages"
    CANDIDATES ||--o{ RESUMES : "owns"
    COMPANIES ||--o{ JOB_POSTS : "publishes"
    CANDIDATES ||--o{ APPLICATIONS : "submits"
    JOB_POSTS ||--o{ APPLICATIONS : "receives"
    RESUMES ||--o{ APPLICATIONS : "used_in"
```

### 2. Sơ đồ Kiến trúc Hệ thống
```mermaid
graph TD
    A[Giao diện Người dùng - Frontend] --> B[Cổng REST API - Backend Service]

    subgraph Backend_Layer ["Tầng Xử lý & Lưu trữ"]
        direction TB
        B --> C[(Cơ sở dữ liệu Quan hệ - MySQL / PostgreSQL)]
        B --> D[(Lưu trữ Tập tin - Cloud Storage / S3)]
    end

    subgraph AI_Layer ["Tầng Dịch vụ AI Engine"]
        direction TB
        B --> E[Tác tử Phân tích CV - CV Parser Module]
        B --> F[Mô hình Chấm điểm Tương đồng - Matching Model]
        E --> G[(Vector Database / Embeddings)]
        F --> G
    end
```

---

## III. NHÓM 3: SƠ ĐỒ LUỒNG VÀ ĐỘNG LỰC

### 1. Sơ đồ Luồng (Activity Diagram)
```mermaid
graph TD
    A(["Bắt đầu"]) --> B["Ứng viên tải file CV lên hệ thống"]
    B --> C["Backend nhận file & gửi tới AI Parser Module"]
    C --> D["AI đọc & bóc tách Kỹ năng, Kinh nghiệm từ CV"]
    D --> E["Lưu thông tin trích xuất vào CSDL"]
    
    E --> F["Nhà tuyển dụng chọn danh sách CV ứng tuyển vào JD"]
    F --> G["Hệ thống lấy thông tin CV và JD tương ứng"]
    G --> H["AI Engine tính toán độ tương đồng - Matching Score"]
    
    H --> I{"Điểm Matching >= 70%?"}
    I -- "Có" --> J["Gợi ý CV vào danh sách Tiềm năng / Shortlist"]
    I -- "Không" --> K["Xếp CV vào danh sách Chờ xem xét"]
    
    J --> L["Hiển thị kết quả & điểm % cho Nhà tuyển dụng"]
    K --> L
    L --> M(["Kết thúc"])
```

### 2. Sơ đồ Tuần tự (Sequence Diagram)
```mermaid
sequenceDiagram
    autonumber
    actor Candidate as Ứng viên
    participant UI as Giao diện Frontend
    participant API as Backend Service
    participant DB as Database
    participant AI as AI Engine

    Candidate->>UI: Tải CV và bấm Nộp đơn ứng tuyển
    UI->>API: Gửi file CV và Job_ID
    API->>AI: Truyền file CV để bóc tách thông tin
    AI-->>API: Trả về Kỹ năng và Nội dung đã trích xuất
    API->>DB: Lưu thông tin CV vào CSDL
    
    API->>DB: Lấy yêu cầu công việc JD Requirements
    DB-->>API: Trả về thông tin JD
    
    API->>AI: Gửi data CV và JD để chấm điểm Matching
    AI-->>API: Trả về Matching Score % và Phân tích
    
    API->>DB: Lưu kết quả ứng tuyển Application Record
    API-->>UI: Thông báo Nộp đơn thành công
    UI-->>Candidate: Hiển thị màn hình xác nhận
```
## IV. THIẾT KẾ CỔNG KẾT NỐI API (RESTFUL API SPECS)

### 1. Luồng Upload & Parse CV bằng AI
* **Endpoint:** `POST /api/v1/resumes/upload`
* **Request:** `FormData` chứa file CV
* **Response:**
```json
{
  "status": "success",
  "data": {
    "resume_id": 12,
    "parsed_skills": ["Python", "FastAPI", "PyTorch", "SQL"],
    "experience_years": 2,
    "file_url": "[https://storage.example.com/cvs/candidate_12.pdf](https://storage.example.com/cvs/candidate_12.pdf)"
  }
}
```

### 2. Luồng Chấm điểm CV & JD Matching
* **Endpoint:** `GET /api/v1/jobs/{job_id}/applications`
* **Response:**
```json
{
  "job_id": 101,
  "candidates": [
    {
      "candidate_id": 5,
      "full_name": "Nguyen Van A",
      "matching_score": 85.5,
      "ai_analysis": "Ứng viên đáp ứng tốt yêu cầu Python và AI framework, thiếu 1 năm kinh nghiệm so với YC."
    }
  ]
}
```
