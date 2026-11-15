from django.urls import path
from . import views

urlpatterns = [
    path('', views.trang_chu_view, name='trang_chu'),
    path('dang-nhap/', views.dang_nhap_view, name='dang_nhap'),
    path('dang-ky/', views.dang_ky_view, name='dang_ky'),
    path('dang-tin/', views.dang_tin_view, name='dang_tin'),
    path('chat/<int:don_id>/', views.chat_don_view, name='chat_don'),
    path('dang-xuat/', views.dang_xuat_view, name='dang_xuat'),
]
