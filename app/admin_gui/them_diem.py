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

    # Nhập điểm quá trình
    tk.Label(input_frame, text="Điểm quá trình:", font=("Times New Roman", 12, "bold"), bg="white").grid(
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
    # Frame chứa tiêu đề học kỳ và năm học
    title_frame = tk.Frame(frame_right, bg="white")
    title_frame.pack(pady=(10, 5))

    lbl_hoc_ky_nam_hoc = tk.Label(
        title_frame, text="", font=("Times New Roman", 14, "bold"),
        fg="darkblue", bg="white"
    )
    lbl_hoc_ky_nam_hoc.pack()

    # Bảng hiển thị
    table_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    table_frame.pack(padx=10, pady=10, fill="both", expand=True)

    columns = ("ma_mh", "ten_mh", "so_tc", "pt_kt", "pt_thi", "diem_qt", "diem_ck", 
               "diem_tk_10", "diem_tk_4", "he_chu")

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=12
    )

    v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    tree.grid(row=0, column=0, sticky="nsew")
    v_scroll.grid(row=0, column=1, sticky="ns")
    h_scroll.grid(row=1, column=0, sticky="ew")

    # Cấu hình các cột
    headers = {
        "ma_mh": "Mã môn học",
        "ten_mh": "Tên môn học",
        "so_tc": "Số tín chỉ",
        "pt_kt": "% Kiểm tra",
        "pt_thi": "% Thi",
        "diem_qt": "Điểm quá trình",
        "diem_ck": "Điểm cuối kỳ",
        "diem_tk_10": "Điểm TK (10)",
        "diem_tk_4": "Điểm TK (4)",
        "he_chu": "Hệ chữ"
    }

    widths = {
        "ma_mh": 100,
        "ten_mh": 200,
        "so_tc": 80,
        "pt_kt": 80,
        "pt_thi": 70,
        "diem_qt": 100,
        "diem_ck": 100,
        "diem_tk_10": 100,
        "diem_tk_4": 90,
        "he_chu": 80
    }

    for col in columns:
        tree.heading(col, text=headers[col])
        tree.column(col, width=widths[col], anchor="center")

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

    def TaiDuLieuBang():
        """Tải dữ liệu vào bảng"""
        sv_selected = cb_sv.get().strip()
        if not sv_selected:
            for item in tree.get_children():
                tree.delete(item)
            lbl_hoc_ky_nam_hoc.config(text="")
            return

        mssv = sv_selected.split(" - ")[0]

        # Xóa dữ liệu cũ
        for item in tree.get_children():
            tree.delete(item)

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
            
            rows = cursor.fetchall()
            if rows:
                # Hiển thị học kỳ và năm học từ môn học đầu tiên (hoặc có thể lấy từ môn được chọn)
                first_row = rows[0]
                hoc_ky = first_row[7]
                nam_hoc = first_row[8]
                lbl_hoc_ky_nam_hoc.config(text=f"Học kỳ {hoc_ky} - Năm học {nam_hoc}")

            for row in rows:
                ma_mh, ten_mh, so_tc, pt_kt, pt_thi, diem_qt, diem_ck, hoc_ky, nam_hoc = row
                
                # Tính điểm tổng kết
                diem_tk_10 = None
                if diem_qt is not None and diem_ck is not None and pt_kt is not None and pt_thi is not None:
                    diem_tk_10 = round((diem_qt * pt_kt + diem_ck * pt_thi) / 100, 2)
                
                diem_tk_4 = chuyen_doi_diem_he_4(diem_tk_10) if diem_tk_10 is not None else None
                he_chu = chuyen_doi_diem_chu(diem_tk_10) if diem_tk_10 is not None else None

                # Format hiển thị
                diem_qt_str = f"{diem_qt:.2f}" if diem_qt is not None else ""
                diem_ck_str = f"{diem_ck:.2f}" if diem_ck is not None else ""
                diem_tk_10_str = f"{diem_tk_10:.2f}" if diem_tk_10 is not None else ""
                diem_tk_4_str = f"{diem_tk_4:.2f}" if diem_tk_4 is not None else ""
                he_chu_str = he_chu if he_chu is not None else ""

                tree.insert("", "end", values=(
                    ma_mh, ten_mh, so_tc, f"{pt_kt}%", f"{pt_thi}%",
                    diem_qt_str, diem_ck_str, diem_tk_10_str, diem_tk_4_str, he_chu_str
                ))
            conn.close()
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
                    messagebox.showwarning("Sai định dạng", "Điểm quá trình phải từ 0 đến 10.")
                    return
            except ValueError:
                messagebox.showwarning("Sai định dạng", "Điểm quá trình phải là số.")
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
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn môn học cần xóa điểm.")
            return

        sv_selected = cb_sv.get().strip()
        if not sv_selected:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn sinh viên.")
            return

        mssv = sv_selected.split(" - ")[0]
        
        try:
            conn = get_db_connect()
            cursor = conn.cursor()
            
            for item in selected:
                ma_mh = tree.item(item, "values")[0]
                cursor.execute("""
                    UPDATE Diem 
                    SET DiemQT=NULL, DiemCK=NULL
                    WHERE MSSV=? AND MaMH=?
                """, (mssv, ma_mh))
            
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa điểm.")
            TaiDuLieuBang()
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def LamMoi():
        """Làm mới form"""
        entry_diem_qt.delete(0, tk.END)
        entry_diem_ck.delete(0, tk.END)
        # Bỏ chọn trong bảng
        for item in tree.selection():
            tree.selection_remove(item)

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

    # Sự kiện khi click vào dòng trong bảng
    def on_tree_select(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], "values")
            # Tự động chọn môn học tương ứng
            if values:
                ma_mh = values[0]
                ten_mh = values[1]
                mh_text = f"{ma_mh} - {ten_mh}"
                cb_mh.set(mh_text)
                # Điền điểm
                diem_qt_val = values[5]
                diem_ck_val = values[6]
                
                entry_diem_qt.delete(0, tk.END)
                entry_diem_ck.delete(0, tk.END)
                
                if diem_qt_val:
                    entry_diem_qt.insert(0, diem_qt_val)
                if diem_ck_val:
                    entry_diem_ck.insert(0, diem_ck_val)

    tree.bind("<<TreeviewSelect>>", on_tree_select)
