import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import get_db_connect

# ====== Hàm chuyển đổi điểm hệ 10 sang hệ 4 ======
def chuyen_doi_diem_he_4(diem_10):
    if diem_10 is None:
        return None
    if diem_10 >= 9.0:
        return 4.0
    elif diem_10 >= 8.5:
        return 3.7
    elif diem_10 >= 8.0:
        return 3.5
    elif diem_10 >= 7.0:
        return 3.0
    elif diem_10 >= 6.5:
        return 2.5
    elif diem_10 >= 6.0:
        return 2.0
    elif diem_10 >= 5.5:
        return 1.5
    elif diem_10 >= 5.0:
        return 1.0
    else:
        return 0.0

# ====== Hàm phân loại học lực ======
def PhanLoaiGPA(gpa):
    if gpa >= 9.0:
        return "Xuất sắc"
    elif gpa >= 8.0:
        return "Giỏi"
    elif gpa >= 7.0:
        return "Khá"
    elif gpa >= 6.5:
        return "Trung bình khá"
    elif gpa >= 5.0:
        return "Trung bình"
    elif gpa >= 4.0:
        return "Yếu"
    else:
        return "Kém"

# ====== Hiển thị thông tin sinh viên và tổng kết ======
def show_info(frame_right, username):
    # Xóa nội dung cũ
    for widget in frame_right.winfo_children():
        widget.destroy()

    # ====== Tiêu đề ======
    lbl_title = tk.Label(
        frame_right,
        text="THÔNG TIN SINH VIÊN",
        font=("Times New Roman", 16, "bold"),
        fg="darkred",
        bg="white"
    )
    lbl_title.pack(pady=5)

    # ====== Khung ngoài ======
    outer_frame = tk.Frame(frame_right, bg="#acd2f6", bd=3, relief="ridge")
    outer_frame.pack(padx=10, pady=5, fill="both", expand=True)

    # ====== Khung chứa Canvas và Scrollbar ======
    canvas_container = tk.Frame(outer_frame, bg="white")
    canvas_container.pack(padx=15, pady=15, fill="both", expand=True)

    # ====== Canvas để chứa nội dung ======
    main_canvas = tk.Canvas(canvas_container, bg="white", highlightthickness=0)
    
    # ====== Thanh cuộn ======
    scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=main_canvas.yview)
    
    # ====== Khung nội dung thực sự (nằm trong Canvas) ======
    inner_frame = tk.Frame(main_canvas, bg="white")

    # ====== Cấu hình binding để cập nhật scroll region ======
    def on_frame_configure(event):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))

    inner_frame.bind("<Configure>", on_frame_configure)

    # ====== Đặt inner_frame vào trong canvas ======
    main_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # ====== Cấu hình canvas để dùng thanh cuộn ======
    main_canvas.configure(yscrollcommand=scrollbar.set)

    # ====== Đóng gói scrollbar và canvas ======
    # Scrollbar ở bên phải, Canvas lấp đầy phần còn lại
    scrollbar.pack(side="right", fill="y")
    main_canvas.pack(side="left", fill="both", expand=True)

    # ====== Lấy thông tin sinh viên ======
    conn = get_db_connect()
    if conn is None:
        messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT MSSV, HoTen, NgaySinh, GioiTinh, Lop, Khoa FROM SinhVien WHERE MSSV = ?", (username,))
    sv_row = cursor.fetchone()
    if not sv_row:
        messagebox.showwarning("Không tìm thấy", "Không tìm thấy thông tin sinh viên.")
        conn.close()
        return

    mssv, hoten, ngaysinh, gioitinh, lop, khoa = sv_row

    # ====== Hiển thị thông tin cá nhân ======
    labels = [
        ("Mã sinh viên", mssv),
        ("Tên sinh viên", hoten),
        ("Ngày sinh", ngaysinh),
        ("Giới tính", gioitinh),
        ("Lớp", lop),
        ("Khoa", khoa)
    ]

    for i, (field, value) in enumerate(labels):
        tk.Label(inner_frame, text=f"{field}:", bg="white", fg="red",
                 font=("Times New Roman", 11, "bold")).grid(row=i, column=0, sticky="w", padx=20, pady=5)
        tk.Label(inner_frame, text=value, bg="white",
                 font=("Times New Roman", 11)).grid(row=i, column=1, sticky="w", padx=10, pady=5)

    # ====== TÍNH TỔNG KẾT THEO HỌC KỲ ======
    cursor.execute("""
        SELECT mh.NamHoc, mh.HocKy, mh.SoTinChi, mh.PtKt, mh.PtThi, d.DiemQT, d.DiemCK
        FROM MonHoc mh
        INNER JOIN Diem d ON mh.MaMH = d.MaMH
        WHERE d.MSSV = ?
        ORDER BY mh.NamHoc, mh.HocKy
    """, (username,))
    rows = cursor.fetchall()

    # Nếu sinh viên có điểm
    if rows:
        hk_data = {}
        tong_diem_all = tong_tc_all = tong_tc_dat_all = 0

        for nam_hoc, hoc_ky, so_tc, pt_kt, pt_thi, diem_qt, diem_ck in rows:
            if diem_qt is not None and diem_ck is not None:
                diem_tk = diem_qt * pt_kt / 100 + diem_ck * pt_thi / 100
                key = f"{hoc_ky} - {nam_hoc}"
                if key not in hk_data:
                    hk_data[key] = {"tong_diem": 0, "tong_tc": 0, "tc_dat": 0}
                hk_data[key]["tong_diem"] += diem_tk * so_tc
                hk_data[key]["tong_tc"] += so_tc
                if diem_tk >= 5.0:
                    hk_data[key]["tc_dat"] += so_tc

                # Tích lũy
                tong_diem_all += diem_tk * so_tc
                tong_tc_all += so_tc
                if diem_tk >= 5.0:
                    tong_tc_dat_all += so_tc

        # ====== Hiển thị bảng tổng kết học kỳ ======
        start_row = len(labels) + 2
        tk.Label(inner_frame, text="--------------------- TỔNG KẾT HỌC KỲ ---------------------",
                 font=("Times New Roman", 12, "bold"), bg="white", fg="darkblue").grid(
            row=start_row, column=0, sticky="w", padx=20, pady=10, columnspan=2
        )

        current_row = start_row + 1
        for hk, data in hk_data.items():
            if data["tong_tc"] > 0:
                gpa_10 = round(data["tong_diem"] / data["tong_tc"], 2)
                gpa_4 = chuyen_doi_diem_he_4(gpa_10)
                hoc_luc = PhanLoaiGPA(gpa_10)
            else:
                gpa_10 = gpa_4 = 0
                hoc_luc = "Chưa có dữ liệu"

            tk.Label(inner_frame, text=f"Học kỳ - Năm học: {hk}",
                     font=("Times New Roman", 11, "bold"), bg="white", fg="brown").grid(
                row=current_row, column=0, sticky="w", padx=20, pady=5, columnspan=2)
            current_row += 1

            tk.Label(inner_frame, text=f"  GPA hệ 10: {gpa_10} | GPA hệ 4: {gpa_4} | Phân loại: {hoc_luc}",
                     font=("Times New Roman", 11), bg="white").grid(
                row=current_row, column=0, sticky="w", padx=40, pady=2, columnspan=2)
            current_row += 1

            tk.Label(inner_frame, text=f"  Tổng TC: {data['tong_tc']} | TC đạt: {data['tc_dat']}",
                     font=("Times New Roman", 11), bg="white").grid(
                row=current_row, column=0, sticky="w", padx=40, pady=2, columnspan=2)
            current_row += 1

        # ====== Hiển thị tổng kết tích lũy ======
        tk.Label(inner_frame, text="--- TỔNG KẾT TÍCH LŨY ---",
                 font=("Times New Roman", 12, "bold"), bg="white", fg="darkgreen").grid(
            row=current_row + 1, column=0, sticky="w", padx=20, pady=10, columnspan=2
        )
        if tong_tc_all > 0:
            gpa_tich_luy_10 = round(tong_diem_all / tong_tc_all, 2)
            gpa_tich_luy_4 = chuyen_doi_diem_he_4(gpa_tich_luy_10)
            hoc_luc_tl = PhanLoaiGPA(gpa_tich_luy_10)
        else:
            gpa_tich_luy_10 = gpa_tich_luy_4 = 0
            hoc_luc_tl = "Chưa có dữ liệu"

        tk.Label(inner_frame, text=f"GPA tích lũy (hệ 10): {gpa_tich_luy_10} | GPA (hệ 4): {gpa_tich_luy_4}",
                 font=("Times New Roman", 11), bg="white").grid(
            row=current_row + 2, column=0, sticky="w", padx=40, pady=2, columnspan=2)

        tk.Label(inner_frame, text=f"Tổng tín chỉ tích lũy: {tong_tc_all} | TC đạt: {tong_tc_dat_all}",
                 font=("Times New Roman", 11), bg="white").grid(
            row=current_row + 3, column=0, sticky="w", padx=40, pady=2, columnspan=2)

        tk.Label(inner_frame, text=f"Phân loại học lực tích lũy: {hoc_luc_tl}",
                 font=("Times New Roman", 11, "bold"), bg="white", fg="darkred").grid(
            row=current_row + 4, column=0, sticky="w", padx=40, pady=5, columnspan=2)

    conn.close()
