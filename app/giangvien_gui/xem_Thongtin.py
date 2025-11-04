import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import get_db_connect

def xem_thongtin(frame_right, username):
    # ===== Xóa nội dung cũ =====
    for widget in frame_right.winfo_children():
        widget.destroy()

    frame_right.configure(bg="white")

    # ======= Tiêu đề =======
    lbl_title = tk.Label(
        frame_right, text="QUẢN LÝ ĐIỂM SINH VIÊN", font=("Times New Roman", 16, "bold"),
        fg="darkred", bg="white")
    lbl_title.pack(pady=5)

    # ======= Phần nhập liệu =======
    input_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    input_frame.pack(padx=5, pady=20, fill="x")

    tk.Label(input_frame, text="Chọn môn học:", font=("Times New Roman", 12, "bold"), bg="white").grid(
        row=0, column=0, padx=5, pady=5, sticky="e")
    cb_mh = ttk.Combobox(input_frame, font=("Times New Roman", 12), width=25)
    cb_mh.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Lấy danh sách môn học mà giảng viên đang dạy
    conn = get_db_connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MaMH, TenMH FROM MonHoc WHERE MaGV = ?", (username,))
        hp_list = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        cb_mh["values"] = hp_list
        conn.close()

    # ====== Nhập điểm ======
    tk.Label(input_frame, text="Điểm giữa kỳ:", font=("Times New Roman", 12, "bold"), bg="white").grid(
        row=0, column=2, padx=5, pady=5, sticky="e")
    entry_diem_qt = tk.Entry(input_frame, font=("Times New Roman", 12), width=10)
    entry_diem_qt.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(input_frame, text="Điểm cuối kỳ:", font=("Times New Roman", 12, "bold"), bg="white").grid(
        row=0, column=4, padx=5, pady=5, sticky="e")
    entry_diem_ck = tk.Entry(input_frame, font=("Times New Roman", 12), width=10)
    entry_diem_ck.grid(row=0, column=5, padx=5, pady=5, sticky="w")

    tk.Label(input_frame, text="Số TC:", font=("Times New Roman", 12, "bold"), bg="white").grid(
        row=1, column=0, padx=5, pady=5, sticky="e")
    
    entry_SoTc = tk.Entry(input_frame,font=("Times New Roman", 12), width=10)
    entry_SoTc.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(input_frame, text="Học kỳ:", font=("Times New Roman", 12, "bold"), bg="white").grid(
        row=1, column=2, padx=5, pady=5, sticky="e")
    
    entry_hk = tk.Entry(input_frame,font=("Times New Roman", 12), width=10)
    entry_hk.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    
    tk.Label(input_frame, text="Số TC:", font=("Times New Roman", 12, "bold"), bg="white").grid(
        row=1, column=4, padx=5, pady=5, sticky="e")
    
    entry_namhoc = tk.Entry(input_frame,font=("Times New Roman", 12), width=10)
    entry_namhoc.grid(row=1, column=5, padx=5, pady=5, sticky="w")

    # ==========================================================
    # ===================== NÚT CHỨC NĂNG ======================
    # ==========================================================
    btn_frame = tk.Frame(frame_right, bg="white")
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="Lưu điểm", width=20, command=lambda: LuuDiem()).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Làm mới", width=20, command=lambda: LamMoi()).grid(row=0, column=1, padx=10)

    # ==========================================================
    # =================== BẢNG HIỂN THỊ DỮ LIỆU ================
    # ==========================================================
    table_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    table_frame.pack(padx=10, pady=10, fill="both", expand=True)

    columns = ("MSSV", "Họ tên", "Lớp", "Điểm GK", "Điểm CK", "Tổng kết")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col, w in zip(columns, (100, 180, 120, 100, 100, 100)):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=v_scroll.set)

    tree.pack(side="left", fill="both", expand=True)
    v_scroll.pack(side="right", fill="y")

    # ==========================================================
    # =================== CÁC HÀM XỬ LÝ ========================
    # ==========================================================

    def TaiDuLieu():
        """Hiển thị danh sách sinh viên của môn học được chọn"""
        mh_selected = cb_mh.get().strip()
        if not mh_selected:
            return
        ma_mh = mh_selected.split(" - ")[0]

        for row in tree.get_children():
            tree.delete(row)

        try:
            conn = get_db_connect()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT sv.MSSV, sv.HoTen, sv.Lop, 
                       ISNULL(d.DiemQT, ''), ISNULL(d.DiemCK, ''), 
                       CASE 
                           WHEN d.DiemQT IS NOT NULL AND d.DiemCK IS NOT NULL 
                           THEN ROUND((d.DiemQT * mh.PtKt/100.0 + d.DiemCK * mh.PtThi/100.0),2)
                           ELSE NULL END AS DiemTong
                FROM SinhVien sv
                INNER JOIN Diem d ON sv.MSSV = d.MSSV
                INNER JOIN MonHoc mh ON d.MaMH = mh.MaMH
                WHERE d.MaMH = ?
                ORDER BY sv.MSSV
            """, (ma_mh,))
            for row in cursor.fetchall():
                tree.insert("", "end", values=tuple(row))
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def on_mh_selected(event):
        mh_selected = cb_mh.get().strip()
        if not mh_selected:
            return

        ma_mh = mh_selected.split(" - ")[0]

        try:
            conn = get_db_connect()
            cursor = conn.cursor()
            cursor.execute("SELECT SoTinChi, HocKy, NamHoc FROM MonHoc WHERE MaMH = ?", (ma_mh,))
            row = cursor.fetchone()
            conn.close()

            # Xóa nội dung cũ
            entry_SoTc.delete(0, tk.END)
            entry_hk.delete(0, tk.END)
            entry_namhoc.delete(0, tk.END)

            if row:
                entry_SoTc.insert(0, str(row[0]))
                entry_hk.insert(0, str(row[1]))
                entry_namhoc.insert(0, str(row[2]))

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        
        TaiDuLieu()

    cb_mh.bind("<<ComboboxSelected>>", on_mh_selected)

    def on_row_selected(event):
        selected = tree.selection()
        if not selected:
            return
        values = tree.item(selected[0], "values")
        entry_diem_qt.delete(0, tk.END)
        entry_diem_ck.delete(0, tk.END)
        if values[3]:
            entry_diem_qt.insert(0, values[3])
        if values[4]:
            entry_diem_ck.insert(0, values[4])

    tree.bind("<<TreeviewSelect>>", on_row_selected)

    def kiem_tra_diem(diem):
        """Kiểm tra điểm có hợp lệ không (nằm trong khoảng 0-10)"""
        if diem is None:
            return True
        return 0 <= diem <= 10

    def LuuDiem():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn sinh viên.")
            return
        values = tree.item(selected[0], "values")
        mssv = values[0]
        ma_mh = cb_mh.get().split(" - ")[0]
        diem_qt = entry_diem_qt.get().strip()
        diem_ck = entry_diem_ck.get().strip()

        try:
            if diem_qt: diem_qt = float(diem_qt)
            else: diem_qt = None
            if diem_ck: diem_ck = float(diem_ck)
            else: diem_ck = None

            # Kiểm tra điểm có hợp lệ không
            if not kiem_tra_diem(diem_qt):
                messagebox.showwarning("Lỗi", "Điểm giữa kỳ phải nằm trong khoảng 0-10")
                return
            if not kiem_tra_diem(diem_ck):
                messagebox.showwarning("Lỗi", "Điểm cuối kỳ phải nằm trong khoảng 0-10")
                return
                    
        except ValueError:
            messagebox.showwarning("Sai định dạng", "Điểm phải là số.")
            return

        try:
            conn = get_db_connect()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Diem SET DiemQT = ?, DiemCK = ? 
                WHERE MSSV = ? AND MaMH = ?
            """, (diem_qt, diem_ck, mssv, ma_mh))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã lưu điểm.")
            TaiDuLieu()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def LamMoi():
        entry_diem_qt.delete(0, tk.END)
        entry_diem_ck.delete(0, tk.END)
        for row in tree.get_children():
            tree.delete(row)
        cb_mh.set("")

