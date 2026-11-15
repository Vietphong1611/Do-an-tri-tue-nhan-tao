from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import BaiDang, DonUngTuyen, NguoiDung, TinNhan


# Hàm tính điểm khớp AI Match
def calculate_match(skills_str, tags_str):
  if not skills_str or not tags_str:
    return 0
  cv_skills = [s.strip().lower() for s in skills_str.split(',') if s.strip()]
  job_tags = [t.strip().lower() for t in tags_str.split(',') if t.strip()]
  if not job_tags:
    return 50
  matched = [t for t in job_tags if any(s in t or t in s for s in cv_skills)]
  return int((len(matched) / len(job_tags)) * 100)


# 1. Đăng ký tài khoản (Chọn vai trò trước)
def dang_ky_view(request):
  if request.method == 'POST':
    reg_role = request.POST.get('vai_tro')
    username = request.POST.get('ten_dang_nhap')
    password = request.POST.get('mat_khau')
    ho_ten = request.POST.get('ho_ten')
    email = request.POST.get('email')

    if username and password and ho_ten:
      if NguoiDung.objects.filter(username=username).exists():
        messages.error(request, 'Tên đăng nhập đã tồn tại.')
      else:
        user = NguoiDung.objects.create_user(
            username=username,
            password=password,
            ho_ten=ho_ten,
            email=email,
            vai_tro=reg_role,
        )
        login(request, user)
        return redirect('trang_chu')
  return render(request, 'dang_ky.html')


# 2. Đăng nhập
def dang_nhap_view(request):
  if request.method == 'POST':
    username = request.POST.get('ten_dang_nhap')
    password = request.POST.get('mat_khau')
    from django.contrib.auth import authenticate

    user = authenticate(request, username=username, password=password)
    if user:
      login(request, user)
      return redirect('trang_chu')
    messages.error(request, 'Mật khẩu hoặc tài khoản sai.')
  return render(request, 'dang_nhap.html')


# 3. Trang chủ việc làm (CareerLink Style - Top Navbar & Grid Cards 3 cột)
@login_required
def trang_chu_view(request):
  jobs = BaiDang.objects.all().order_by('-id')

  search_pos = request.GET.get('pos', '')
  search_addr = request.GET.get('addr', '')
  search_kw = request.GET.get('kw', '')

  if search_pos:
    jobs = jobs.filter(tieu_de__icontains=search_pos)
  if search_addr:
    jobs = jobs.filter(dia_diem__icontains=search_addr)
  if search_kw:
    jobs = jobs.filter(ky_nang_yeu_cau__icontains=search_kw)

  # Tính AI Match nếu là Ứng viên
  if request.user.vai_tro == 'ung_vien' and request.user.ky_nang:
    for job in jobs:
      job.match_score = calculate_match(
          request.user.ky_nang, job.ky_nang_yeu_cau
      )

  context = {'jobs': jobs}
  return render(request, 'trang_chu.html', context)


# 4. NTD Đăng tin tuyển dụng (Địa chỉ, ngành nghề, kỹ năng tự nhập)
@login_required
def dang_tin_view(request):
  if request.user.vai_tro != 'nha_tuyen_dung':
    return redirect('trang_chu')

  if request.method == 'POST':
    tieu_de = request.POST.get('tieu_de')
    dia_diem = request.POST.get('dia_diem')
    nganh_nghe = request.POST.get('nganh_nghe')
    muc_luong = request.POST.get('muc_luong')
    ky_nang = request.POST.get('ky_nang_yeu_cau')
    mo_ta = request.POST.get('mo_ta')

    BaiDang.objects.create(
        tieu_de=tieu_de,
        ten_cong_ty=request.user.ho_ten,
        nha_tuyen_dung=request.user,
        dia_diem=dia_diem,
        nganh_nghe=nganh_nghe,
        muc_luong=muc_luong,
        ky_nang_yeu_cau=ky_nang,
        mo_ta=mo_ta,
    )
    messages.success(request, 'Đăng tin thành công!')
    return redirect('trang_chu')

  return render(request, 'dang_tin.html')


# 5. Ứng tuyển & Nhắn tin Chat 1-1
@login_required
def chat_don_view(request, don_id):
  don = get_object_or_404(DonUngTuyen, id=don_id)

  if request.method == 'POST':
    if 'action' in request.POST:
      # Nút xác nhận/từ chối của Nhà tuyển dụng
      new_status = request.POST.get('action')
      if new_status in ['Đã xác nhận', 'Từ chối']:
        don.trang_thai = new_status
        don.save()
    elif 'noi_dung' in request.POST:
      # Gửi tin nhắn chat
      noi_dung = request.POST.get('noi_dung')
      if noi_dung:
        TinNhan.objects.create(
            don_ung_tuyen=don, nguoi_gui=request.user, noi_dung=noi_dung
        )
    return redirect('chat_don', don_id=don.id)

  tin_nhan_list = TinNhan.objects.filter(don_ung_tuyen=don).order_by(
      'thoi_gian'
  )
  return render(
      request, 'chat_don.html', {'don': don, 'tin_nhan_list': tin_nhan_list}
  )


def dang_xuat_view(request):
  logout(request)
  return redirect('dang_nhap')
