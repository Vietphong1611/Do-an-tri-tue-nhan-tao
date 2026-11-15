# Khai báo model User tùy chỉnh và App tuyển dụng
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tuyendung',
]

AUTH_USER_MODEL = 'tuyendung.NguoiDung'

# Cấu hình Cơ sở dữ liệu MySQL Workbench
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'du_lieu_tuyendung',
        'USER': 'root',
        'PASSWORD': '123',  # <--- Thay mật khẩu MySQL Workbench của bạn
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

LOGIN_URL = 'dang_nhap'
