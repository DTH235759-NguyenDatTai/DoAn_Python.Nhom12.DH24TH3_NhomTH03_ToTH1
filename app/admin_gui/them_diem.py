import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import get_db_connect

def chuyen_doi_diem_he_4(diem_10):
    """Chuyển đổi điểm từ hệ 10 sang hệ 4"""
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

def chuyen_doi_diem_chu(diem_10):
    """Chuyển đổi điểm từ hệ 10 sang hệ chữ"""
    if diem_10 is None:
        return None
    if diem_10 >= 9.0:
        return "A+"
    elif diem_10 >= 8.5:
        return "A"
    elif diem_10 >= 8.0:
        return "B+"
    elif diem_10 >= 7.0:
        return "B"
    elif diem_10 >= 6.5:
        return "C+"
    elif diem_10 >= 6.0:
        return "C"
    elif diem_10 >= 5.5:
        return "D+"
    elif diem_10 >= 5.0:
        return "D"
    else:
        return "F"

def add_diem(frame_right):
    # ===== Xóa nội dung cũ =====
    for widget in frame_right.winfo_children():
        widget.destroy()

    frame_right.configure(bg="white")

    # ======= Tiêu đề =======
    lbl_title = tk.Label(
        frame_right, text="THÊM ĐIỂM CHO SINH VIÊN", font=("Times New Roman", 16, "bold"),
        fg="darkred", bg="white"
    )
    lbl_title.pack(pady=5)

    # ==========================================================
    # ===================== KHUNG NHẬP LIỆU ====================
    # ==========================================================
    input_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    input_frame.pack(padx=5, pady=5, fill="x")

    # Chọn sinh viên
    tk.Label(input_frame, text="Chọn sinh viên:", font=("Times New Roman", 12, "bold"), bg="white").grid(
        row=0, column=0, sticky="e", padx=5, pady=5
    )
    cb_sv = ttk.Combobox(input_frame, font=("Times New Roman", 12), width=35, state="readonly")
    cb_sv.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Lấy danh sách sinh viên từ SQL
    conn = get_db_connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MSSV, HoTen FROM SinhVien ORDER BY MSSV")
        sv_list = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        cb_sv["values"] = sv_list
        conn.close()

    # Chọn môn học
    tk.Label(input_frame, text="Chọn môn học:", font=("Times New Roman", 12, "bold"), bg="white").grid(
        row=1, column=0, sticky="e", padx=5, pady=5
    )
    cb_mh = ttk.Combobox(input_frame, font=("Times New Roman", 12), width=35, state="readonly")
    cb_mh.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Nhập điểm giữa kỳ
    tk.Label(input_frame, text="Điểm giữa kỳ:", font=("Times New Roman", 12, "bold"), bg="white").grid(
        row=0, column=3, sticky="e", padx=5, pady=5
    )
    entry_diem_qt = tk.Entry(input_frame, font=("Times New Roman", 12), width=20)
    entry_diem_qt.grid(row=0, column=4, padx=5, pady=5, sticky="w")

    # Nhập điểm cuối kỳ
    tk.Label(input_frame, text="Điểm cuối kỳ:", font=("Times New Roman", 12, "bold"), bg="white").grid(
        row=1, column=3, sticky="e", padx=5, pady=5
    )
    entry_diem_ck = tk.Entry(input_frame, font=("Times New Roman", 12), width=20)
    entry_diem_ck.grid(row=1, column=4, padx=5, pady=5, sticky="w")

    # ==========================================================
    # ===================== NÚT CHỨC NĂNG ======================
    # ==========================================================
    btn_frame = tk.Frame(frame_right, bg="white")
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="Thêm/Cập nhật điểm", width=20, command=lambda: ThemDiem()).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Xóa điểm", width=20, command=lambda: XoaDiem()).grid(row=0, column=1, padx=10)
    ttk.Button(btn_frame, text="Làm mới", width=20, command=lambda: LamMoi()).grid(row=0, column=2, padx=10)

    # ==========================================================
    # ================= BẢNG HIỂN THỊ DỮ LIỆU ==================
    # ==========================================================
    # Frame chứa canvas và scrollbar
    canvas_frame = tk.Frame(frame_right, bg="white")
    canvas_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Canvas để cuộn
    canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=10)
    v_scroll = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    h_scroll = ttk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
    
    scrollable_frame = tk.Frame(canvas, bg="white")
    
    canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    
    canvas.grid(row=0, column=0, sticky="nsew")
    v_scroll.grid(row=0, column=1, sticky="ns")
    h_scroll.grid(row=1, column=0, sticky="ew")
    
    canvas_frame.grid_rowconfigure(0, weight=1)
    canvas_frame.grid_columnconfigure(0, weight=1)
    
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    def update_canvas_scroll(event=None):
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        # Cập nhật kích thước canvas window
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())
    
    canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width))
    scrollable_frame.bind('<Configure>', update_canvas_scroll)
    
    # Biến để lưu các widget bảng để xóa khi load lại
    table_widgets = []

    # ==========================================================
    # ===================== HÀM CHỨC NĂNG ======================
    # ==========================================================
    
    def TaiDuLieuMh():
        """Tải danh sách môn học của sinh viên được chọn"""
        sv_selected = cb_sv.get().strip()
        if not sv_selected:
            cb_mh["values"] = []
            return
        
        mssv = sv_selected.split(" - ")[0]

        try:
            conn = get_db_connect()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT mh.MaMH, mh.TenMH, mh.HocKy, mh.NamHoc
                FROM MonHoc mh
                INNER JOIN Diem d ON mh.MaMH = d.MaMH
                WHERE d.MSSV = ?
                ORDER BY mh.NamHoc DESC, mh.HocKy ASC
            """, (mssv,))
            mh_list = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
            cb_mh["values"] = mh_list
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def XoaBangCu():
        """Xóa tất cả widget trong bảng cũ"""
        for widget in table_widgets:
            widget.destroy()
        table_widgets.clear()
    
    def PhanLoaiGPA(gpa):
        """Phân loại điểm trung bình"""
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
    
    def TaoBangDiem(data, hoc_ky, nam_hoc, parent_frame):
        """Tạo bảng điểm cho một học kỳ"""
        # Tiêu đề học kỳ
        title_label = tk.Label(
            parent_frame,
            text=f"Học kỳ {hoc_ky} - Năm học {nam_hoc}",
            font=("Arial", 13, "bold"),
            bg="white",
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(10, 5), padx=10)
        table_widgets.append(title_label)
        
        # Tạo frame cho bảng
        table_container = tk.Frame(parent_frame, bg="white")
        table_container.pack(fill="x", padx=10, pady=(0, 20))
        table_widgets.append(table_container)
        
        # Header của bảng (màu xanh, chữ trắng)
        headers = ["STT", "Mã Môn", "Tên Môn", "TC", "% KT", "% Thi", 
                  "Điểm\nGiữa Kỳ", "Thi L1", "Thi L2"]
        col_widths = [50, 90, 200, 50, 60, 60, 90, 70, 70]
        
        # Tạo header row
        header_frame = tk.Frame(table_container, bg="#3498db")
        header_frame.pack(fill="x")
        table_widgets.append(header_frame)
        
        for idx, (header_text, width) in enumerate(zip(headers, col_widths)):
            header_label = tk.Label(
                header_frame,
                text=header_text,
                bg="#3498db",
                fg="white",
                font=("Arial", 10, "bold"),
                width=width//8,
                height=2,
                relief="solid",
                borderwidth=1,
                anchor="center",
                padx=2
            )
            header_label.grid(row=0, column=idx, sticky="nsew", padx=0, pady=0)
            header_frame.grid_columnconfigure(idx, weight=1, minsize=width)
        
        # Tạo các hàng dữ liệu
        tong_diem_tk = 0
        tong_tin_chi = 0
        tong_tin_chi_dat = 0
        
        for idx, row_data in enumerate(data, start=1):
            # Màu xen kẽ
            bg_color = "white" if idx % 2 == 1 else "#f2f2f2"
            
            row_frame = tk.Frame(table_container, bg=bg_color, relief="solid", borderwidth=1)
            row_frame.pack(fill="x")
            table_widgets.append(row_frame)
            
            ma_mh, ten_mh, so_tc, pt_kt, pt_thi, diem_qt, diem_ck = row_data
            
            # Tính điểm tổng kết
            diem_tk_10 = None
            diem_tk_4 = None
            he_chu = None
            if diem_qt is not None and diem_ck is not None and pt_kt is not None and pt_thi is not None:
                diem_tk_10 = round((diem_qt * pt_kt + diem_ck * pt_thi) / 100, 2)
                diem_tk_4 = chuyen_doi_diem_he_4(diem_tk_10)
                he_chu = chuyen_doi_diem_chu(diem_tk_10)
                
                # Cộng vào tổng để tính GPA
                tong_diem_tk += diem_tk_10 * so_tc
                tong_tin_chi += so_tc
                if diem_tk_10 >= 4.0:  # Điểm đạt (>= 4.0 trên hệ 10)
                    tong_tin_chi_dat += so_tc
            
            # Chuẩn bị dữ liệu hiển thị
            values = [
                str(idx),  # STT
                ma_mh,  # Mã Môn
                ten_mh,  # Tên Môn
                str(so_tc),  # TC
                f"{pt_kt}%",  # % KT
                f"{pt_thi}%",  # % Thi
                f"{diem_qt:.2f}" if diem_qt is not None else "",  # Điểm Giữa Kỳ
                f"{diem_ck:.2f}" if diem_ck is not None else "",  # Thi L1
                ""  # Thi L2 (không có)
            ]
            
            # Tạo các cell
            for col_idx, (value, width) in enumerate(zip(values, col_widths)):
                align = "center" if col_idx not in [1, 2] else "w"
                cell_label = tk.Label(
                    row_frame,
                    text=value,
                    bg=bg_color,
                    fg="black",
                    font=("Arial", 10),
                    width=width//8,
                    height=1,
                    relief="solid",
                    borderwidth=1,
                    anchor=align,
                    padx=2,
                    wraplength=width
                )
                cell_label.grid(row=0, column=col_idx, sticky="nsew", padx=0, pady=0)
                row_frame.grid_columnconfigure(col_idx, weight=1, minsize=width)
        
        # Phần tóm tắt học kỳ
        summary_frame = tk.Frame(parent_frame, bg="white")
        summary_frame.pack(fill="x", padx=10, pady=(5, 10))
        table_widgets.append(summary_frame)
        
        # Tính GPA
        gpa_10 = tong_diem_tk / tong_tin_chi if tong_tin_chi > 0 else 0
        gpa_4 = chuyen_doi_diem_he_4(gpa_10)
        
        # Tổng kết toàn bộ tích lũy (sẽ tính ở hàm chính)
        summary_data = [
            ("Điểm trung bình học kỳ hệ 10/100:", f"{gpa_10:.2f}"),
            ("Điểm trung bình học kỳ hệ 4:", f"{gpa_4:.2f}"),
            ("Số tín chỉ đạt:", str(tong_tin_chi_dat)),
            ("Số tín chỉ tích lũy:", str(tong_tin_chi)),
            ("Phân loại điểm trung bình HK:", PhanLoaiGPA(gpa_10))
        ]
        
        for label_text, value_text in summary_data:
            row_frame = tk.Frame(summary_frame, bg="white")
            row_frame.pack(fill="x", pady=2)
            table_widgets.append(row_frame)
            
            label_widget = tk.Label(
                row_frame,
                text=label_text,
                bg="white",
                font=("Arial", 10),
                anchor="w"
            )
            label_widget.pack(side="left")
            table_widgets.append(label_widget)
            
            value_widget = tk.Label(
                row_frame,
                text=value_text,
                bg="white",
                font=("Arial", 10),
                anchor="e"
            )
            value_widget.pack(side="right")
            table_widgets.append(value_widget)
        
        return gpa_10, gpa_4, tong_tin_chi, tong_tin_chi_dat
    
    def TaiDuLieuBang():
        """Tải dữ liệu vào bảng"""
        sv_selected = cb_sv.get().strip()
        if not sv_selected:
            XoaBangCu()
            return

        mssv = sv_selected.split(" - ")[0]
        
        # Xóa bảng cũ
        XoaBangCu()

        try:
            conn = get_db_connect()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    mh.MaMH, mh.TenMH, mh.SoTinChi, mh.PtKt, mh.PtThi,
                    d.DiemQT, d.DiemCK, mh.HocKy, mh.NamHoc
                FROM MonHoc mh
                INNER JOIN Diem d ON mh.MaMH = d.MaMH
                WHERE d.MSSV = ?
                ORDER BY mh.NamHoc DESC, mh.HocKy ASC
            """, (mssv,))
            
            all_rows = cursor.fetchall()
            conn.close()
            
            if not all_rows:
                return
            
            # Nhóm dữ liệu theo học kỳ và năm học
            data_by_semester = {}
            for row in all_rows:
                ma_mh, ten_mh, so_tc, pt_kt, pt_thi, diem_qt, diem_ck, hoc_ky, nam_hoc = row
                key = (hoc_ky, nam_hoc)
                if key not in data_by_semester:
                    data_by_semester[key] = []
                data_by_semester[key].append((ma_mh, ten_mh, so_tc, pt_kt, pt_thi, diem_qt, diem_ck))
            
            # Tính tổng tích lũy - tính từ từng môn
            tong_diem_tich_luy = 0
            tong_tc_tich_luy = 0
            tong_tc_dat_tich_luy = 0
            
            # Tạo bảng cho từng học kỳ
            for (hoc_ky, nam_hoc), data in sorted(data_by_semester.items()):
                gpa_10, gpa_4, tc, tc_dat = TaoBangDiem(data, hoc_ky, nam_hoc, scrollable_frame)
                # Cộng từng môn vào tích lũy
                for row_data in data:
                    ma_mh, ten_mh, so_tc, pt_kt, pt_thi, diem_qt, diem_ck = row_data
                    if diem_qt is not None and diem_ck is not None and pt_kt is not None and pt_thi is not None:
                        diem_tk = round((diem_qt * pt_kt + diem_ck * pt_thi) / 100, 2)
                        tong_diem_tich_luy += diem_tk * so_tc
                        tong_tc_tich_luy += so_tc
                        if diem_tk >= 4.0:  # Điểm đạt
                            tong_tc_dat_tich_luy += so_tc
            
            # Hiển thị tổng tích lũy ở cuối (nếu có nhiều học kỳ)
            if len(data_by_semester) > 1:
                gpa_tich_luy_10 = tong_diem_tich_luy / tong_tc_tich_luy if tong_tc_tich_luy > 0 else 0
                gpa_tich_luy_4 = chuyen_doi_diem_he_4(gpa_tich_luy_10)
                
                summary_tl_frame = tk.Frame(scrollable_frame, bg="white")
                summary_tl_frame.pack(fill="x", padx=10, pady=(10, 10))
                table_widgets.append(summary_tl_frame)
                
                # Tiêu đề
                title_tl = tk.Label(
                    summary_tl_frame,
                    text="TỔNG KẾT TÍCH LŨY:",
                    bg="white",
                    font=("Arial", 12, "bold"),
                    anchor="w"
                )
                title_tl.pack(anchor="w", pady=(0, 10))
                table_widgets.append(title_tl)
                
                # Dữ liệu tích lũy
                tl_data = [
                    ("Điểm trung bình tích lũy:", f"{gpa_tich_luy_10:.2f}"),
                    ("Điểm trung bình tích lũy (hệ 4):", f"{gpa_tich_luy_4:.2f}"),
                    ("Số tín chỉ đạt:", str(tong_tc_dat_tich_luy)),
                    ("Số tín chỉ tích lũy:", str(tong_tc_tich_luy))
                ]
                
                for label_text, value_text in tl_data:
                    row_frame = tk.Frame(summary_tl_frame, bg="white")
                    row_frame.pack(fill="x", pady=2)
                    table_widgets.append(row_frame)
                    
                    label_widget = tk.Label(
                        row_frame,
                        text=label_text,
                        bg="white",
                        font=("Arial", 10),
                        anchor="w"
                    )
                    label_widget.pack(side="left")
                    table_widgets.append(label_widget)
                    
                    value_widget = tk.Label(
                        row_frame,
                        text=value_text,
                        bg="white",
                        font=("Arial", 10),
                        anchor="e"
                    )
                    value_widget.pack(side="right")
                    table_widgets.append(value_widget)
            
            update_canvas_scroll()
            
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def ThemDiem():
        """Thêm hoặc cập nhật điểm"""
        sv_selected = cb_sv.get().strip()
        mh_selected = cb_mh.get().strip()
        diem_qt_str = entry_diem_qt.get().strip()
        diem_ck_str = entry_diem_ck.get().strip()

        if not sv_selected:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn sinh viên.")
            return
        
        if not mh_selected:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn môn học.")
            return

        mssv = sv_selected.split(" - ")[0]
        ma_mh = mh_selected.split(" - ")[0]

        # Validate điểm
        diem_qt = None
        diem_ck = None

        if diem_qt_str:
            try:
                diem_qt = float(diem_qt_str)
                if diem_qt < 0 or diem_qt > 10:
                    messagebox.showwarning("Sai định dạng", "Điểm giữa kỳ phải từ 0 đến 10.")
                    return
            except ValueError:
                messagebox.showwarning("Sai định dạng", "Điểm giữa kỳ phải là số.")
                return

        if diem_ck_str:
            try:
                diem_ck = float(diem_ck_str)
                if diem_ck < 0 or diem_ck > 10:
                    messagebox.showwarning("Sai định dạng", "Điểm cuối kỳ phải từ 0 đến 10.")
                    return
            except ValueError:
                messagebox.showwarning("Sai định dạng", "Điểm cuối kỳ phải là số.")
                return

        try:
            conn = get_db_connect()
            cursor = conn.cursor()
            
            # Kiểm tra xem đã có điểm chưa
            cursor.execute("SELECT COUNT(*) FROM Diem WHERE MSSV=? AND MaMH=?", (mssv, ma_mh))
            if cursor.fetchone()[0] > 0:
                # Cập nhật
                cursor.execute("""
                    UPDATE Diem 
                    SET DiemQT=?, DiemCK=?
                    WHERE MSSV=? AND MaMH=?
                """, (diem_qt, diem_ck, mssv, ma_mh))
                messagebox.showinfo("Thành công", "Cập nhật điểm thành công.")
            else:
                # Thêm mới
                cursor.execute("""
                    INSERT INTO Diem (MSSV, MaMH, DiemQT, DiemCK)
                    VALUES (?, ?, ?, ?)
                """, (mssv, ma_mh, diem_qt, diem_ck))
                messagebox.showinfo("Thành công", "Thêm điểm thành công.")
            
            conn.commit()
            LamMoi()
            TaiDuLieuBang()
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def XoaDiem():
        """Xóa điểm"""
        sv_selected = cb_sv.get().strip()
        mh_selected = cb_mh.get().strip()
        
        if not sv_selected:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn sinh viên.")
            return
        
        if not mh_selected:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn môn học cần xóa điểm.")
            return

        mssv = sv_selected.split(" - ")[0]
        ma_mh = mh_selected.split(" - ")[0]
        
        try:
            conn = get_db_connect()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE Diem 
                SET DiemQT=NULL, DiemCK=NULL
                WHERE MSSV=? AND MaMH=?
            """, (mssv, ma_mh))
            
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa điểm.")
            LamMoi()
            TaiDuLieuBang()
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def LamMoi():
        """Làm mới form"""
        entry_diem_qt.delete(0, tk.END)
        entry_diem_ck.delete(0, tk.END)

    # Sự kiện khi chọn sinh viên
    def on_sv_selected(event):
        TaiDuLieuMh()
        TaiDuLieuBang()
        cb_mh.set("")  # Reset môn học

    # Sự kiện khi chọn môn học
    def on_mh_selected(event):
        # Có thể tự động điền điểm nếu đã có
        sv_selected = cb_sv.get().strip()
        mh_selected = cb_mh.get().strip()
        
        if not sv_selected or not mh_selected:
            return

        mssv = sv_selected.split(" - ")[0]
        ma_mh = mh_selected.split(" - ")[0]

        try:
            conn = get_db_connect()
            cursor = conn.cursor()
            cursor.execute("SELECT DiemQT, DiemCK FROM Diem WHERE MSSV=? AND MaMH=?", (mssv, ma_mh))
            row = cursor.fetchone()
            conn.close()

            entry_diem_qt.delete(0, tk.END)
            entry_diem_ck.delete(0, tk.END)

            if row and row[0] is not None:
                entry_diem_qt.insert(0, str(row[0]))
            if row and row[1] is not None:
                entry_diem_ck.insert(0, str(row[1]))
        except Exception as e:
            pass

    cb_sv.bind("<<ComboboxSelected>>", on_sv_selected)
    cb_mh.bind("<<ComboboxSelected>>", on_mh_selected)