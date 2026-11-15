import mysql.connector
from nicegui import app, ui

# ----------------------------------------------------
# 1. CẤU HÌNH KẾT NỐI MYSQL WORKBENCH
# ----------------------------------------------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',  # Mật khẩu MySQL của bạn
    'database': 'du_lieu_tuyendung',
    'port': 3306,
}


def get_db():
  try:
    return mysql.connector.connect(**DB_CONFIG)
  except Exception as e:
    print('Lỗi kết nối MySQL:', e)
    return None


def ensure_chat_table():
  conn = get_db()
  if not conn:
    return
  try:
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS tin_nhan (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_don INT NOT NULL,
                nguoi_gui VARCHAR(50) NOT NULL,
                noi_dung TEXT NOT NULL,
                thoi_gian DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_don) REFERENCES don_ung_tuyen(id) ON DELETE CASCADE,
                FOREIGN KEY (nguoi_gui) REFERENCES nguoi_dung(ten_dang_nhap) ON DELETE CASCADE
            )
        """)
    conn.commit()
  except Exception as e:
    print('Kiểm tra bảng tin_nhan:', e)
  finally:
    conn.close()


user_state = {'logged_in': False, 'user': None}


# ----------------------------------------------------
# 2. THUẬT TOÁN ĐO % PHÙ HỢP ĐA TIÊU CHÍ (AI MATCHING)
# ----------------------------------------------------
def calculate_match_advanced(user, job):
  if not user or user.get('vai_tro') != 'ung_vien':
    return 0

  cv_skills = [
      s.strip().lower()
      for s in (user.get('ky_nang') or '').split(',')
      if s.strip()
  ]
  job_skills = [
      t.strip().lower()
      for t in (job.get('ky_nang_yeu_cau') or '').split(',')
      if t.strip()
  ]

  skill_score = 0
  if job_skills and cv_skills:
    matched_skills = [
        t for t in job_skills if any(s in t or t in s for s in cv_skills)
    ]
    skill_score = (len(matched_skills) / len(job_skills)) * 100

  target_pos = (user.get('vi_tri_mong_muon') or '').lower().strip()
  job_title = (job.get('tieu_de') or '').lower().strip()
  title_score = 0
  if target_pos and job_title:
    if target_pos in job_title or job_title in target_pos:
      title_score = 100

  cv_loc = (user.get('dia_diem') or '').lower().strip()
  job_loc = (job.get('dia_diem') or '').lower().strip()
  loc_score = 0
  if cv_loc and job_loc:
    if cv_loc in job_loc or job_loc in cv_loc:
      loc_score = 100

  total_score = int(
      (skill_score * 0.6) + (title_score * 0.2) + (loc_score * 0.2)
  )
  return min(100, max(0, total_score))


# ----------------------------------------------------
# 3. FLOATING CHAT BOX (SỬA LỖI CLICK & Z-INDEX MENU)
# ----------------------------------------------------
def render_floating_chat():
  if not user_state['logged_in']:
    return

  user = user_state['user']
  is_cand = user['vai_tro'] == 'ung_vien'
  last_msg_count = {'count': -1}

  # Đặt z-index: 4000 (cao hơn header 2000 nhưng thấp hơn dropdown menu 6000)
  with ui.page_sticky(position='bottom-right', x_offset=24, y_offset=20).style(
      'z-index: 4000;'
  ):
    with ui.column().classes('items-end gap-3'):
      chat_card = (
          ui.card()
          .style('width: 360px; height: 460px;')
          .classes(
              'bg-white shadow-2xl border-2 border-blue-600 rounded-2xl flex'
              ' flex-col justify-between p-0'
          )
      )
      chat_card.set_visibility(False)

      with chat_card:
        # Header khung chat
        with ui.row().classes(
            'w-full bg-blue-900 text-white px-4 py-2.5 rounded-t-xl'
            ' justify-between items-center'
        ):
          with ui.row().classes('items-center gap-2'):
            ui.icon('chat', size='sm').classes('text-blue-200')
            ui.label('💬 Chat Tuyển Dụng 1-1').classes('font-bold text-sm')

          def close_chat():
            chat_card.set_visibility(False)
            chat_timer.deactivate()

          ui.button(icon='close', on_click=close_chat).props(
              'flat dense round color=white'
          )

        # Chọn cuộc trò chuyện
        with ui.column().classes(
            'w-full px-3 pt-2 pb-1 gap-1 bg-gray-50 border-b'
        ):
          ui.label(
              'Chọn '
              + ('Nhà tuyển dụng' if is_cand else 'Ứng viên')
              + ' để nhắn tin:'
          ).classes('text-xs text-gray-600 font-semibold')
          select_app = (
              ui.select(options={}, label='-- Chọn cuộc trò chuyện --')
              .classes('w-full text-xs')
              .props('outlined dense bg-white')
          )

        # Vùng hiển thị tin nhắn
        msg_container = ui.scroll_area().classes(
            'w-full flex-1 px-3 py-2 bg-gray-50'
        )

        # Ô nhập tin nhắn + nút gửi
        with ui.row().classes(
            'w-full p-2 border-t gap-1 items-center bg-white rounded-b-2xl'
        ):
          msg_input = (
              ui.input(placeholder='Nhập tin nhắn... (Enter để gửi)')
              .classes('flex-1')
              .props('dense outlined')
          )

          def send_message():
            if not select_app.value:
              ui.notify(
                  'Chưa có đơn ứng tuyển để nhắn tin!', type='warning'
              )
              return
            if not msg_input.value or not msg_input.value.strip():
              return
            don_id = select_app.value
            text_to_send = msg_input.value.strip()
            msg_input.value = ''
            conn = get_db()
            if conn:
              try:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO tin_nhan (id_don, nguoi_gui, noi_dung)'
                    ' VALUES (%s, %s, %s)',
                    (don_id, user['ten_dang_nhap'], text_to_send),
                )
                conn.commit()
              except Exception as e:
                ui.notify(f'Lỗi gửi tin: {e}', type='negative')
              finally:
                conn.close()
              last_msg_count['count'] = -1
              render_messages()

          msg_input.on('keydown.enter', send_message)
          ui.button(icon='send', on_click=send_message).props(
              'dense color=primary'
          )

      def render_messages(quiet=False):
        if not select_app.value:
          return
        don_id = select_app.value
        conn = get_db()
        if not conn:
          return
        try:
          cursor = conn.cursor(dictionary=True)
          cursor.execute(
              'SELECT * FROM tin_nhan WHERE id_don = %s ORDER BY thoi_gian ASC',
              (don_id,),
          )
          msgs = cursor.fetchall()
        except Exception as e:
          print('Lỗi tải tin nhắn:', e)
          return
        finally:
          conn.close()

        if quiet and len(msgs) == last_msg_count['count']:
          return

        last_msg_count['count'] = len(msgs)
        msg_container.clear()

        with msg_container:
          if not msgs:
            ui.label('Chưa có tin nhắn nào. Hãy gửi lời chào!').classes(
                'text-xs text-gray-400 text-center w-full my-4 italic'
            )
          for m in msgs:
            is_me = m['nguoi_gui'] == user['ten_dang_nhap']
            sender_name = (
                'Bạn' if is_me else ('Công ty' if is_cand else 'Ứng viên')
            )
            stamp_str = (
                m['thoi_gian'].strftime('%H:%M %d/%m')
                if m['thoi_gian']
                else ''
            )
            ui.chat_message(
                text=m['noi_dung'],
                name=sender_name,
                stamp=stamp_str,
                sent=is_me,
            ).classes('text-xs')

        msg_container.scroll_to(percent=1.0)

      def load_chat_apps():
        last_msg_count['count'] = -1
        conn = get_db()
        if not conn:
          return
        try:
          cursor = conn.cursor(dictionary=True)
          if is_cand:
            cursor.execute(
                """
                SELECT d.id, b.tieu_de, b.ten_cong_ty
                FROM don_ung_tuyen d 
                JOIN bai_dang b ON d.id_bai_dang = b.id 
                WHERE d.ten_dang_nhap_ung_vien = %s 
                ORDER BY d.id DESC
                """,
                (user['ten_dang_nhap'],),
            )
          else:
            cursor.execute(
                """
                SELECT d.id, b.tieu_de, n.ho_ten as ten_ung_vien
                FROM don_ung_tuyen d 
                JOIN bai_dang b ON d.id_bai_dang = b.id 
                JOIN nguoi_dung n ON d.ten_dang_nhap_ung_vien = n.ten_dang_nhap 
                WHERE d.ten_dang_nhap_ntd = %s 
                ORDER BY d.id DESC
                """,
                (user['ten_dang_nhap'],),
            )
          apps_list = cursor.fetchall()
        except Exception as e:
          print('Lỗi tải danh sách chat:', e)
          apps_list = []
        finally:
          conn.close()

        options = {}
        for a in apps_list:
          label_text = (
              f"🏢 {a['ten_cong_ty']} - {a['tieu_de']}"
              if is_cand
              else f"👤 {a['ten_ung_vien']} - {a['tieu_de']}"
          )
          options[a['id']] = label_text

        if options:
          selected_val = (
              select_app.value
              if select_app.value in options
              else list(options.keys())[0]
          )
          select_app.set_options(options, value=selected_val)
          render_messages()
        else:
          select_app.set_options({}, value=None)
          msg_container.clear()
          with msg_container:
            ui.label(
                'Chưa có đơn ứng tuyển nào! Hãy bấm "Xem chi tiết" -> "Ứng'
                ' tuyển ngay" ở 1 công việc để bắt đầu chat.'
            ).classes(
                'text-xs text-amber-700 font-medium text-center w-full my-6'
                ' px-2'
            )

      def on_app_change():
        last_msg_count['count'] = -1
        render_messages()

      select_app.on('update:model-value', on_app_change)

      def auto_refresh():
        if chat_card.visible and select_app.value:
          render_messages(quiet=True)

      chat_timer = ui.timer(2.0, auto_refresh, active=False)

      def toggle_chat():
        new_state = not chat_card.visible
        chat_card.set_visibility(new_state)
        if new_state:
          load_chat_apps()
          chat_timer.activate()
        else:
          chat_timer.deactivate()

      # Nút tròn mở/đóng chat dùng on_click chuẩn của NiceGUI
      ui.button(icon='chat', on_click=toggle_chat).classes(
          'w-14 h-14 rounded-full bg-blue-700 text-white shadow-xl'
          ' hover:bg-blue-800'
      ).props('round')


# ----------------------------------------------------
# 4. TRANG ĐĂNG NHẬP / ĐĂNG KÝ
# ----------------------------------------------------
@ui.page('/login')
def login_page():
  with ui.card().classes(
      'w-96 absolute-center p-6 shadow-xl border-t-4 border-blue-600'
  ):
    ui.label('💼 CareerLink AI Portal').classes(
        'text-2xl font-bold text-blue-900 text-center w-full mb-2'
    )
    ui.label('Hệ thống Tìm kiếm Việc làm & AI Match').classes(
        'text-sm text-gray-500 text-center w-full mb-4'
    )

    with ui.tabs().classes('w-full') as tabs:
      tab_login = ui.tab('🔒 Đăng nhập')
      tab_reg = ui.tab('📝 Đăng ký')

    with ui.tab_panels(tabs, value=tab_login).classes('w-full mt-4'):
      with ui.tab_panel(tab_login):
        u_input = ui.input('Tên đăng nhập').classes('w-full')
        p_input = (
            ui.input('Mật khẩu', password=True, password_toggle_button=True)
            .classes('w-full')
        )

        def do_login():
          conn = get_db()
          if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                'SELECT * FROM nguoi_dung WHERE ten_dang_nhap=%s AND'
                ' mat_khau=%s',
                (u_input.value, p_input.value),
            )
            usr = cursor.fetchone()
            conn.close()
            if usr:
              user_state['logged_in'] = True
              user_state['user'] = usr
              ui.navigate.to('/')
            else:
              ui.notify('Sai tên đăng nhập hoặc mật khẩu!', type='negative')

        ui.button('Đăng nhập ngay', on_click=do_login).classes(
            'w-full bg-blue-700 text-white mt-4'
        )

      with ui.tab_panel(tab_reg):
        role = ui.radio(
            {'ung_vien': 'Ứng viên', 'nha_tuyen_dung': 'Nhà tuyển dụng'},
            value='ung_vien',
        ).props('inline')
        ru_input = ui.input('Tên đăng nhập mới').classes('w-full')
        rp_input = ui.input('Mật khẩu', password=True).classes('w-full')
        rn_input = ui.input('Họ tên / Tên công ty').classes('w-full')
        re_input = ui.input('Email liên hệ').classes('w-full')

        def do_reg():
          if ru_input.value and rp_input.value and rn_input.value:
            conn = get_db()
            if conn:
              cursor = conn.cursor()
              try:
                cursor.execute(
                    'INSERT INTO nguoi_dung (ten_dang_nhap, mat_khau, ho_ten,'
                    ' email, vai_tro) VALUES (%s,%s,%s,%s,%s)',
                    (
                        ru_input.value,
                        rp_input.value,
                        rn_input.value,
                        re_input.value,
                        role.value,
                    ),
                )
                conn.commit()
                ui.notify(
                    'Đăng ký thành công! Vui lòng đăng nhập.', type='positive'
                )
              except Exception as err:
                ui.notify(f'Lỗi đăng ký: {err}', type='negative')
              finally:
                conn.close()

        ui.button('Tạo tài khoản', on_click=do_reg).classes(
            'w-full bg-green-600 text-white mt-4'
        )


# ----------------------------------------------------
# 5. TRANG CHỦ CHÍNH
# ----------------------------------------------------
@ui.page('/')
def main_page():
  if not user_state['logged_in']:
    ui.navigate.to('/login')
    return

  user = user_state['user']

  with ui.header().classes(
      'bg-white text-gray-800 px-8 py-3 flex justify-between items-center'
      ' border-b border-gray-200 shadow-sm'
  ):
    with ui.row().classes('items-center gap-3 cursor-pointer').on(
        'click', lambda: ui.navigate.to('/')
    ):
      ui.label('CareerLink').classes('text-2xl font-black text-blue-700')
      ui.label('.vn').classes('text-2xl font-black text-red-500 -ml-3')
      ui.label('| AI Jobs').classes('text-sm font-semibold text-gray-500 ml-1')

    with ui.row().classes('items-center gap-4'):
      ui.label(
          f"👋 {user['ho_ten']}"
          f" ({'NTD' if user['vai_tro']=='nha_tuyen_dung' else 'Ứng viên'})"
      ).classes('text-sm font-medium text-gray-700')

      if user['vai_tro'] == 'ung_vien':
        ui.button(
            '📝 Sửa hồ sơ CV', on_click=lambda: ui.navigate.to('/cv-edit')
        ).props('flat color=primary icon=edit')
      elif user['vai_tro'] == 'nha_tuyen_dung':
        ui.button(
            '📢 Đăng tin tuyển dụng',
            on_click=lambda: ui.navigate.to('/post-job'),
        ).props('flat color=primary icon=add_circle')

      def logout():
        user_state['logged_in'] = False
        user_state['user'] = None
        ui.navigate.to('/login')

      ui.button('Đăng xuất', on_click=logout).props(
          'flat color=negative icon=logout'
      )

  with ui.column().classes('w-full max-w-7xl mx-auto p-6 gap-6 mb-20'):
    with ui.card().classes(
        'w-full p-5 shadow-sm bg-white border border-gray-200 rounded-xl'
    ):
      ui.label('🔍 Tìm kiếm việc làm & Lọc theo % AI Match CV').classes(
          'text-base font-bold text-blue-900 mb-2'
      )

      with ui.row().classes('w-full gap-3 items-center flex-nowrap'):
        search_pos = (
            ui.input(placeholder='🎯 Vị trí công việc...')
            .classes('flex-1')
            .props('outlined dense')
        )
        search_loc = (
            ui.input(placeholder='📍 Địa chỉ / Thành phố...')
            .classes('flex-1')
            .props('outlined dense')
        )
        search_kw = (
            ui.input(placeholder='🔑 Từ khóa kỹ năng...')
            .classes('flex-1')
            .props('outlined dense')
        )

        match_filter = ui.select(
            options={
                '0': '🎯 Tất cả độ khớp',
                '50': '≥ 50% Phù hợp',
                '70': '≥ 70% Phù hợp',
                '90': '≥ 90% Phù hợp',
            },
            value='0',
        ).classes('w-44').props('outlined dense')

        search_btn = ui.button('🔍 Tìm kiếm').classes(
            'bg-blue-700 text-white px-5 h-10 font-bold flex-shrink-0'
        )

      grid_container = ui.element('div').classes('w-full')

      def load_jobs():
        grid_container.clear()
        conn = get_db()
        if not conn:
          return
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM bai_dang ORDER BY id DESC')
        jobs = cursor.fetchall()
        conn.close()

        if search_pos.value:
          jobs = [
              j
              for j in jobs
              if search_pos.value.lower() in j['tieu_de'].lower()
          ]
        if search_loc.value:
          jobs = [
              j
              for j in jobs
              if search_loc.value.lower() in j['dia_diem'].lower()
          ]
        if search_kw.value:
          jobs = [
              j
              for j in jobs
              if search_kw.value.lower() in j['ky_nang_yeu_cau'].lower()
          ]

        min_score = int(match_filter.value or 0)
        filtered_jobs = []

        for job in jobs:
          score = (
              calculate_match_advanced(user, job)
              if user['vai_tro'] == 'ung_vien'
              else 0
          )
          job['match_score'] = score

          if user['vai_tro'] == 'ung_vien' and score < min_score:
            continue
          filtered_jobs.append(job)

        if user['vai_tro'] == 'ung_vien':
          filtered_jobs.sort(key=lambda x: x['match_score'], reverse=True)

        jobs = filtered_jobs

        with grid_container:
          with ui.row().classes(
              'justify-between items-center w-full mt-6 mb-2'
          ):
            ui.label('Việc làm hấp dẫn 🔥').classes(
                'text-2xl font-extrabold text-gray-900'
            )

          if not jobs:
            ui.label(
                'Không tìm thấy công việc nào đạt mức % phù hợp đã chọn.'
            ).classes('text-red-500 font-medium text-center w-full my-6')
            return

          with ui.grid().classes('grid-cols-1 md:grid-cols-3 gap-4 w-full'):
            for job in jobs:
              job_id = job['id']
              score = job['match_score']

              badge_bg = (
                  'bg-green-100 text-green-800 border-green-300'
                  if score >= 70
                  else 'bg-blue-100 text-blue-800 border-blue-200'
              )

              with ui.card().classes(
                  'w-full p-4 shadow-sm hover:shadow-md border border-gray-200'
                  ' rounded-xl transition-all'
              ):
                with ui.row().classes('justify-between w-full items-start'):
                  ui.label(job['ten_cong_ty'][:1].upper()).classes(
                      'bg-blue-600 text-white font-black w-10 h-10 rounded-lg'
                      ' flex items-center justify-center text-lg'
                  )
                  ui.label('🔥 HOT JOB').classes(
                      'bg-rose-100 text-rose-600 font-bold text-xs px-2 py-0.5'
                      ' rounded-md border border-rose-200'
                  )

                ui.label(job['tieu_de']).classes(
                    'font-bold text-gray-900 hover:text-blue-600 text-base'
                    ' mt-2 line-clamp-1 cursor-pointer'
                ).on('click', lambda j_id=job_id: ui.navigate.to(f'/job/{j_id}'))

                ui.label(f"🏢 {job['ten_cong_ty']}").classes(
                    'text-xs text-gray-500 font-medium'
                )
                ui.label(f"📍 {job['dia_diem']}").classes(
                    'text-xs text-gray-600'
                )
                ui.label(f"🛠️ {job['ky_nang_yeu_cau']}").classes(
                    'text-xs text-gray-600 font-mono bg-gray-100 p-1 rounded'
                )

                with ui.row().classes(
                    'justify-between items-center w-full mt-3 border-t pt-2'
                ):
                  ui.label(f"💰 {job['muc_luong']}").classes(
                      'text-blue-600 font-bold text-sm'
                  )
                  if user['vai_tro'] == 'ung_vien':
                    ui.label(f'Khớp: {score}%').classes(
                        f'text-xs font-bold px-2 py-0.5 rounded border'
                        f' {badge_bg}'
                    )

                with ui.row().classes('w-full gap-2 mt-2'):
                  ui.button(
                      '👁️ Xem chi tiết',
                      on_click=lambda j_id=job_id: ui.navigate.to(
                          f'/job/{j_id}'
                      ),
                  ).classes(
                      'flex-1 bg-gray-100 text-gray-800 text-xs shadow-none'
                  )

      search_btn.on_click(load_jobs)
      load_jobs()

  render_floating_chat()


# ----------------------------------------------------
# 6. TRANG CHI TIẾT CÔNG VIỆC DỘNG (/job/{job_id})
# ----------------------------------------------------
@ui.page('/job/{job_id}')
def job_detail_page(job_id: int):
  if not user_state['logged_in']:
    ui.navigate.to('/login')
    return

  user = user_state['user']
  conn = get_db()
  if not conn:
    return

  cursor = conn.cursor(dictionary=True)
  cursor.execute('SELECT * FROM bai_dang WHERE id = %s', (job_id,))
  job = cursor.fetchone()
  conn.close()

  if not job:
    with ui.column().classes('w-full max-w-4xl mx-auto p-6 items-center'):
      ui.label('⚠️ Bài tuyển dụng này không tồn tại!').classes(
          'text-lg font-bold text-red-600'
      )
      ui.button(
          '⬅ Quay lại trang chủ', on_click=lambda: ui.navigate.to('/')
      ).classes('mt-4 bg-blue-700 text-white')
    return

  match_score = calculate_match_advanced(user, job)

  with ui.header().classes(
      'bg-white text-gray-800 px-8 py-3 flex justify-between items-center'
      ' border-b shadow-sm'
  ):
    with ui.row().classes('items-center gap-2 cursor-pointer').on(
        'click', lambda: ui.navigate.to('/')
    ):
      ui.label('CareerLink').classes('text-2xl font-black text-blue-700')
      ui.label('.vn').classes('text-2xl font-black text-red-500 -ml-3')
    ui.button(
        '🏠 Trang chủ', on_click=lambda: ui.navigate.to('/')
    ).props('flat color=primary icon=home')

  with ui.column().classes('w-full max-w-5xl mx-auto p-6 gap-6 mb-20'):
    ui.button(
        '⬅ Quay lại danh sách việc làm', on_click=lambda: ui.navigate.to('/')
    ).props('flat color=primary icon=arrow_back')

    with ui.card().classes(
        'w-full p-6 shadow-sm border border-gray-200 rounded-xl bg-white'
    ):
      with ui.row().classes('justify-between items-start w-full'):
        with ui.row().classes('gap-4 items-center'):
          ui.label(job['ten_cong_ty'][:1].upper()).classes(
              'bg-blue-600 text-white font-black w-16 h-16 rounded-xl flex'
              ' items-center justify-center text-2xl shadow-sm'
          )
          with ui.column().classes('gap-0'):
            ui.label(job['tieu_de']).classes(
                'text-2xl font-extrabold text-gray-900'
            )
            ui.label(f"🏢 {job['ten_cong_ty']}").classes(
                'text-base font-semibold text-blue-700'
            )

        if user['vai_tro'] == 'ung_vien':
          ui.label(f'Độ khớp AI: {match_score}%').classes(
              'bg-blue-100 text-blue-900 font-extrabold text-base px-4 py-2'
              ' rounded-xl border border-blue-300 shadow-sm'
          )

      ui.separator().classes('my-4')

      with ui.grid().classes(
          'grid-cols-1 md:grid-cols-4 gap-4 w-full bg-gray-50 p-4 rounded-lg'
      ):
        with ui.column().classes('gap-0'):
          ui.label('📍 Địa điểm cụ thể').classes('text-xs text-gray-500')
          ui.label(job['dia_diem']).classes(
              'text-sm font-bold text-gray-800'
          )
        with ui.column().classes('gap-0'):
          ui.label('💰 Mức lương').classes('text-xs text-gray-500')
          ui.label(job['muc_luong']).classes(
              'text-sm font-bold text-blue-600'
          )
        with ui.column().classes('gap-0'):
          ui.label('📂 Ngành nghề').classes('text-xs text-gray-500')
          ui.label(job['nganh_nghe']).classes(
              'text-sm font-bold text-gray-800'
          )
        with ui.column().classes('gap-0'):
          ui.label('📅 Ngày đăng tin').classes('text-xs text-gray-500')
          ui.label(str(job['ngay_dang'])).classes(
              'text-sm font-bold text-gray-800'
          )

    with ui.card().classes(
        'w-full p-6 shadow-sm border border-gray-200 rounded-xl bg-white gap-4'
    ):
      ui.label('🛠️ Kỹ năng yêu cầu').classes('text-lg font-bold text-gray-900')
      ui.label(job['ky_nang_yeu_cau']).classes(
          'text-sm font-mono bg-blue-50 text-blue-900 p-3 rounded-lg border'
          ' border-blue-100'
      )
      ui.separator().classes('my-2')
      ui.label('📋 Mô tả chi tiết công việc').classes(
          'text-lg font-bold text-gray-900'
      )
      desc_text = (
          job['mo_ta']
          if job['mo_ta']
          else 'Nhà tuyển dụng chưa cập nhật mô tả chi tiết.'
      )
      ui.markdown(desc_text).classes('text-gray-700 text-sm leading-relaxed')

      if user['vai_tro'] == 'ung_vien':

        def apply_from_detail():
          c = get_db()
          cur = c.cursor()
          cur.execute(
              'SELECT * FROM don_ung_tuyen WHERE id_bai_dang=%s AND'
              ' ten_dang_nhap_ung_vien=%s',
              (job['id'], user['ten_dang_nhap']),
          )
          if cur.fetchone():
            ui.notify('Bạn đã nộp hồ sơ bài đăng này rồi!', type='warning')
          else:
            cur.execute(
                'INSERT INTO don_ung_tuyen (id_bai_dang,'
                ' ten_dang_nhap_ung_vien, ten_dang_nhap_ntd, diem_phu_hop,'
                " trang_thai) VALUES (%s, %s, %s, %s, 'Chờ xử lý')",
                (
                    job['id'],
                    user['ten_dang_nhap'],
                    job['ten_dang_nhap_ntd'],
                    match_score,
                ),
            )
            c.commit()
            ui.notify(
                f'🎉 Nộp hồ sơ thành công! (Điểm AI Match: {match_score}%)',
                type='positive',
            )
          c.close()

        with ui.row().classes('w-full justify-end gap-3 mt-4'):
          ui.button(
              '🚀 Ứng tuyển ngay', on_click=apply_from_detail
          ).classes('bg-blue-600 text-white text-base px-6 py-2 shadow-md')

  render_floating_chat()


# ----------------------------------------------------
# 7. TRANG ĐĂNG TIN TUYỂN DỤNG DÀNH CHO NTD (/post-job)
# ----------------------------------------------------
@ui.page('/post-job')
def post_job_page():
  if not user_state['logged_in']:
    ui.navigate.to('/login')
    return

  user = user_state['user']
  if user['vai_tro'] != 'nha_tuyen_dung':
    ui.notify('Chức năng chỉ dành cho Nhà tuyển dụng!', type='warning')
    ui.navigate.to('/')
    return

  with ui.header().classes(
      'bg-white text-gray-800 px-8 py-3 flex justify-between items-center'
      ' border-b shadow-sm'
  ):
    with ui.row().classes('items-center gap-2 cursor-pointer').on(
        'click', lambda: ui.navigate.to('/')
    ):
      ui.label('CareerLink').classes('text-2xl font-black text-blue-700')
      ui.label('.vn').classes('text-2xl font-black text-red-500 -ml-3')
    ui.button(
        '🏠 Trang chủ', on_click=lambda: ui.navigate.to('/')
    ).props('flat color=primary icon=home')

  with ui.column().classes('w-full max-w-4xl mx-auto p-6 gap-4 mb-20'):
    ui.button(
        '⬅ Quay lại trang chủ', on_click=lambda: ui.navigate.to('/')
    ).props('flat color=primary icon=arrow_back')

    with ui.card().classes(
        'w-full p-6 shadow-sm border border-gray-200 rounded-xl bg-white gap-4'
    ):
      ui.label('📢 Đăng tin tuyển dụng mới').classes(
          'text-2xl font-bold text-blue-900 mb-2'
      )

      with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
        title_in = (
            ui.input(
                'Tên vị trí tuyển dụng (*)',
                placeholder='Ví dụ: Senior Python Developer',
            )
            .classes('w-full')
            .props('outlined dense')
        )
        company_in = (
            ui.input('Tên công ty (*)', value=user.get('ho_ten', ''))
            .classes('w-full')
            .props('outlined dense')
        )
        loc_in = (
            ui.input(
                'Địa điểm cụ thể (*)',
                placeholder='Ví dụ: 123 Nguyễn Văn Linh, Đà Nẵng',
            )
            .classes('w-full')
            .props('outlined dense')
        )
        cat_in = (
            ui.input(
                'Ngành nghề (*)', placeholder='Ví dụ: Công nghệ thông tin'
            )
            .classes('w-full')
            .props('outlined dense')
        )
        salary_in = (
            ui.input(
                'Mức lương', placeholder='Ví dụ: 15 - 25 triệu / Thỏa thuận'
            )
            .classes('w-full')
            .props('outlined dense')
        )
        skills_in = (
            ui.input(
                'Kỹ năng yêu cầu (phân cách dấu phẩy) (*)',
                placeholder='Ví dụ: Python, FastAPI, SQL, Git',
            )
            .classes('w-full')
            .props('outlined dense')
        )

      desc_in = (
          ui.textarea(
              'Mô tả công việc chi tiết',
              placeholder='Nhập chi tiết yêu cầu công việc...',
          )
          .classes('w-full')
          .props('outlined dense')
      )

      def save_job():
        if (
            not title_in.value
            or not company_in.value
            or not loc_in.value
            or not cat_in.value
            or not skills_in.value
        ):
          ui.notify('Vui lòng điền đủ các trường (*)!', type='warning')
          return

        conn = get_db()
        if conn:
          cursor = conn.cursor()
          cursor.execute(
              """
                INSERT INTO bai_dang (tieu_de, ten_cong_ty, ten_dang_nhap_ntd, dia_diem, nganh_nghe, muc_luong, ky_nang_yeu_cau, mo_ta, ngay_dang)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURDATE())
            """,
              (
                  title_in.value.strip(),
                  company_in.value.strip(),
                  user['ten_dang_nhap'],
                  loc_in.value.strip(),
                  cat_in.value.strip(),
                  (
                      salary_in.value.strip()
                      if salary_in.value
                      else 'Thỏa thuận'
                  ),
                  skills_in.value.strip(),
                  desc_in.value.strip() if desc_in.value else '',
              ),
          )
          conn.commit()
          conn.close()

          ui.notify(
              '🎉 Đã đăng tin tuyển dụng lên CSDL MySQL!', type='positive'
          )
          ui.navigate.to('/')

      with ui.row().classes('w-full justify-end gap-3 mt-4'):
        ui.button('🚀 Đăng tin tuyển dụng ngay', on_click=save_job).classes(
            'bg-blue-600 text-white text-base px-6 py-2 shadow-md'
        )

  render_floating_chat()


# ----------------------------------------------------
# 8. TRANG CẬP NHẬT CV ỨNG VIÊN (/cv-edit)
# ----------------------------------------------------
@ui.page('/cv-edit')
def cv_edit_page():
  if not user_state['logged_in']:
    ui.navigate.to('/login')
    return

  user = user_state['user']
  if user['vai_tro'] != 'ung_vien':
    ui.notify('Chức năng chỉ dành cho Ứng viên!', type='warning')
    ui.navigate.to('/')
    return

  with ui.header().classes(
      'bg-white text-gray-800 px-8 py-3 flex justify-between items-center'
      ' border-b shadow-sm'
  ):
    with ui.row().classes('items-center gap-2 cursor-pointer').on(
        'click', lambda: ui.navigate.to('/')
    ):
      ui.label('CareerLink').classes('text-2xl font-black text-blue-700')
      ui.label('.vn').classes('text-2xl font-black text-red-500 -ml-3')
    ui.button(
        '🏠 Trang chủ', on_click=lambda: ui.navigate.to('/')
    ).props('flat color=primary icon=home')

  with ui.column().classes('w-full max-w-4xl mx-auto p-6 gap-4 mb-20'):
    ui.button(
        '⬅ Quay lại trang chủ', on_click=lambda: ui.navigate.to('/')
    ).props('flat color=primary icon=arrow_back')

    with ui.card().classes(
        'w-full p-6 shadow-sm border border-gray-200 rounded-xl bg-white gap-4'
    ):
      ui.label('📝 Cập nhật thông tin Hồ sơ CV').classes(
          'text-2xl font-bold text-blue-900 mb-2'
      )

      with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
        name_in = (
            ui.input('Họ và tên (*)', value=user.get('ho_ten', '') or '')
            .classes('w-full')
            .props('outlined dense')
        )
        email_in = (
            ui.input('Email (*)', value=user.get('email', '') or '')
            .classes('w-full')
            .props('outlined dense')
        )
        phone_in = (
            ui.input('Số điện thoại', value=user.get('so_dien_thoai', '') or '')
            .classes('w-full')
            .props('outlined dense')
        )
        loc_in = (
            ui.input(
                'Địa điểm mong muốn', value=user.get('dia_diem', '') or ''
            )
            .classes('w-full')
            .props('outlined dense placeholder="Ví dụ: Đà Nẵng, Hà Nội..."')
        )
        target_in = (
            ui.input(
                'Vị trí mong muốn',
                value=user.get('vi_tri_mong_muon', '') or '',
            )
            .classes('w-full')
            .props('outlined dense placeholder="Ví dụ: Python Developer..."')
        )
        exp_in = (
            ui.input(
                'Kinh nghiệm làm việc', value=user.get('kinh_nghiem', '') or ''
            )
            .classes('w-full')
            .props('outlined dense')
        )

      skills_in = (
          ui.textarea(
              'Kỹ năng chuyên môn (phân cách bằng dấu phẩy) (*)',
              value=user.get('ky_nang', '') or '',
          )
          .classes('w-full')
          .props('outlined dense placeholder="Python, FastAPI, SQL, Git"')
      )
      summary_in = (
          ui.textarea(
              'Tóm tắt bản thân', value=user.get('tom_tat', '') or ''
          )
          .classes('w-full')
          .props('outlined dense')
      )
      cv_file_in = (
          ui.input(
              'File CV đính kèm',
              value=user.get('ten_file_cv', '') or 'CV_Online.pdf',
          )
          .classes('w-full')
          .props('outlined dense')
      )

      def save_cv():
        if not name_in.value or not email_in.value or not skills_in.value:
          ui.notify(
              'Vui lòng điền đủ Họ tên, Email và Kỹ năng!', type='warning'
          )
          return

        conn = get_db()
        if conn:
          cursor = conn.cursor(dictionary=True)
          cursor.execute(
              """
                UPDATE nguoi_dung 
                SET ho_ten=%s, email=%s, so_dien_thoai=%s, dia_diem=%s, vi_tri_mong_muon=%s, kinh_nghiem=%s, ky_nang=%s, tom_tat=%s, ten_file_cv=%s
                WHERE ten_dang_nhap=%s
            """,
              (
                  name_in.value,
                  email_in.value,
                  phone_in.value,
                  loc_in.value,
                  target_in.value,
                  exp_in.value,
                  skills_in.value,
                  summary_in.value,
                  cv_file_in.value,
                  user['ten_dang_nhap'],
              ),
          )
          conn.commit()

          cursor.execute(
              'SELECT * FROM nguoi_dung WHERE ten_dang_nhap=%s',
              (user['ten_dang_nhap'],),
          )
          user_state['user'] = cursor.fetchone()
          conn.close()

          ui.notify(
              '🎉 Đã cập nhật Hồ sơ CV thành công!', type='positive'
          )
          ui.navigate.to('/')

      with ui.row().classes('w-full justify-end gap-3 mt-4'):
        ui.button('💾 Lưu CV vào MySQL', on_click=save_cv).classes(
            'bg-blue-600 text-white text-base px-6 py-2 shadow-md'
        )

  render_floating_chat()


ensure_chat_table()
ui.run(title='CareerLink AI Portal', port=8080, reload=False)
