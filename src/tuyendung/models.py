from django.contrib.auth.models import AbstractUser
from django.db import models


class NguoiDung(AbstractUser):
  VAI_TRO_CHOICES = (
      ('ung_vien', 'Ứng viên'),
      ('nha_tuyen_dung', 'Nhà tuyển dụng'),
  )
  ho_ten = models.CharField(max_length=100, verbose_name='Họ tên / Tên công ty')
  vai_tro = models.CharField(
      max_length=20, choices=VAI_TRO_CHOICES, default='ung_vien'
  )
  so_dien_thoai = models.CharField(max_length=20, blank=True, null=True)
  dia_diem = models.CharField(max_length=100, blank=True, null=True)
  vi_tri_mong_muon = models.CharField(max_length=100, blank=True, null=True)
  ky_nang = models.TextField(blank=True, null=True)
  kinh_nghiem = models.CharField(max_length=100, blank=True, null=True)
  tom_tat = models.TextField(blank=True, null=True)
  ten_file_cv = models.CharField(max_length=255, blank=True, null=True)

  class Meta:
    db_table = 'nguoi_dung'


class BaiDang(models.Model):
  tieu_de = models.CharField(max_length=255)
  ten_cong_ty = models.CharField(max_length=255)
  nha_tuyen_dung = models.ForeignKey(
      NguoiDung, on_delete=models.CASCADE, related_name='bai_dang_set'
  )
  dia_diem = models.CharField(max_length=100)
  nganh_nghe = models.CharField(max_length=100)
  muc_luong = models.CharField(max_length=100, blank=True, null=True)
  ky_nang_yeu_cau = models.CharField(max_length=255, blank=True, null=True)
  mo_ta = models.TextField(blank=True, null=True)
  ngay_dang = models.DateField(auto_now_add=True)

  class Meta:
    db_table = 'bai_dang'


class DonUngTuyen(models.Model):
  bai_dang = models.ForeignKey(BaiDang, on_delete=models.CASCADE)
  ung_vien = models.ForeignKey(
      NguoiDung, on_delete=models.CASCADE, related_name='don_ung_vien_set'
  )
  nha_tuyen_dung = models.ForeignKey(
      NguoiDung, on_delete=models.CASCADE, related_name='don_ntd_set'
  )
  diem_phu_hop = models.IntegerField(default=0)
  trang_thai = models.CharField(max_length=50, default='Chờ xử lý')
  ngay_ung_tuyen = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 'don_ung_tuyen'


class TinNhan(models.Model):
  don_ung_tuyen = models.ForeignKey(DonUngTuyen, on_delete=models.CASCADE)
  nguoi_gui = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
  noi_dung = models.TextField()
  thoi_gian = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 'tin_nhan'
