from tkinter import messagebox, ttk
import tkinter as tk
from db_connect import get_db_connect

def add_sv(frame_right):
    # ===== Xóa nội dung cũ =====
    for widget in frame_right.winfo_children():
        widget.destroy()

    # ======= Tiêu đề =======
    lbl_title = tk.Label(
        frame_right, text="THÊM SINH VIÊN VÀO MÔN HỌC", font=("Times New Roman", 16, "bold"),
        fg="darkred", bg="white"
    )
    lbl_title.pack(pady=5)

    # ==========================================================
    # ===================== KHUNG NHẬP LIỆU ====================
    # ==========================================================
    input_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    input_frame.pack(padx=5, pady=5, fill="x")

    tk.Label(input_frame, text="Chọn môn học:", font=("Times New Roman", 12, "bold"), bg="white").grid(
        row=0, column=0, sticky="e", padx=5, pady=5
    )
    cb_mh = ttk.Combobox(input_frame, font=("Times New Roman", 12), width=40, state="readonly")
    cb_mh.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(input_frame, text="Tìm kiếm môn học:", font=("Times New Roman", 12, "bold"), bg="white").grid(
        row=0, column=2, sticky="e", padx=5, pady=5
    )

    entry_mh = tk.Entry(input_frame, font=("Times New Roman", 12), width=20)
    entry_mh.grid(row=0, column=3, padx=5, pady=5, sticky="w")
    # Lấy danh sách môn học từ SQL
    conn = get_db_connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MaMH, TenMH FROM MonHoc ORDER BY NamHoc DESC, HocKy ASC")
        mh_list = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        cb_mh["values"] = mh_list
        conn.close()

    tk.Label(input_frame, text="Học kỳ: ", font=("Times New Roman", 12, "bold"), bg="white",).grid(
        row=1, column=0, sticky="e", padx=5, pady=5
    )
    entry_hk = tk.Entry(input_frame, font=("Times New Roman", 12), width=20)
    entry_hk.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(input_frame, text="Năm học: ", font=("Times New Roman", 12, "bold"), bg="white").grid(
        row=1, column=2, sticky="e", padx=5, pady=5
    )
    entry_namhoc = tk.Entry(input_frame, font=("Times New Roman", 12), width=20)
    entry_namhoc.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    # ====== TÌM KIẾM MÔN HỌC ======
    def tim_kiem_mh(event=None):
        text = entry_mh.get().strip().lower()

        conn = get_db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT MaMH, TenMH FROM MonHoc ORDER BY NamHoc DESC, HocKy ASC")
        full_list = cursor.fetchall()
        conn.close()

        # Lọc theo Mã MH hoặc Tên MH
        filtered = []
        for ma, ten in full_list:
            if text in ma.lower() or text in ten.lower():
                filtered.append(f"{ma} - {ten}")

        cb_mh["values"] = filtered

        # Nếu có kết quả → chọn dòng đầu tiên
        if filtered:
            cb_mh.set(filtered[0])
            on_mh_selected(None)
        else:
            cb_mh.set("")
            entry_hk.delete(0, tk.END)
            entry_namhoc.delete(0, tk.END)
            for row in tree.get_children():
                tree.delete(row)

    # Gắn sự kiện mỗi lần gõ phím
    entry_mh.bind("<KeyRelease>", tim_kiem_mh)

    # ==========================================================
    # ===================== NÚT CHỨC NĂNG ======================
    # ==========================================================
    btn_frame = tk.Frame(frame_right, bg="white")
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="Thêm sinh viên", width=20, command=lambda: open_add_sv_frame()).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Xóa sinh viên", width=20, command=lambda: Xoa()).grid(row=0, column=1, padx=10)
    ttk.Button(btn_frame, text="Làm mới", width=20, command=lambda: LamMoi()).grid(row=0, column=2, padx=10)

    # ==========================================================
    # ================= BẢNG HIỂN THỊ DỮ LIỆU ==================
    # ==========================================================
    table_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    table_frame.pack(padx=10, pady=10, fill="both", expand=True)

    tree = ttk.Treeview(
        table_frame,
        columns=("MSSV", "Họ tên", "Lớp", "Khoa"),
        show="headings",
        height=8
    )

    for col, w in zip(("MSSV", "Họ tên", "Lớp", "Khoa"), (100, 180, 100, 150)):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    tree.grid(row=0, column=0, sticky="nsew")
    v_scroll.grid(row=0, column=1, sticky="ns")
    h_scroll.grid(row=1, column=0, sticky="ew")

    # ==========================================================
    # ===================== HÀM CHỨC NĂNG ======================
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
                SELECT sv.MSSV, sv.HoTen, sv.Lop, sv.Khoa
                FROM SinhVien sv
                INNER JOIN Diem d ON sv.MSSV = d.MSSV
                WHERE d.MaMH = ?
                ORDER BY sv.MSSV
            """, (ma_mh,))
            for row in cursor.fetchall():
                tree.insert("", "end", values=tuple(row))
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def Xoa():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn sinh viên cần xóa.")
            return
        mh_selected = cb_mh.get().strip()
        if not mh_selected:
            messagebox.showwarning("Thiếu thông tin", "Chưa chọn môn học.")
            return
        ma_mh = mh_selected.split(" - ")[0]
        try:
            conn = get_db_connect()
            cursor = conn.cursor()
            for item in selected:
                mssv = tree.item(item, "values")[0]
                cursor.execute("DELETE FROM Diem WHERE MaMH=? AND MSSV=?", (ma_mh, mssv))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa sinh viên khỏi môn học.")
            TaiDuLieu()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def LamMoi():
        cb_mh.set("")
        for row in tree.get_children():
            tree.delete(row)

    # ==========================================================
    # =================== SỰ KIỆN CHỌN MÔN HỌC =================
    # ==========================================================
    def on_mh_selected(event):
        mh_selected = cb_mh.get().strip()
        if not mh_selected:
            return

        ma_mh = mh_selected.split(" - ")[0]

        try:
            conn = get_db_connect()
            cursor = conn.cursor()
            cursor.execute("SELECT HocKy, NamHoc FROM MonHoc WHERE MaMH = ?", (ma_mh,))
            row = cursor.fetchone()
            conn.close()

            # Xóa nội dung cũ
            entry_hk.delete(0, tk.END)
            entry_namhoc.delete(0, tk.END)

            if row:
                entry_hk.insert(0, str(row[0]))
                entry_namhoc.insert(0, str(row[1]))

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

        # Sau khi hiển thị học kỳ/năm học thì tải danh sách sinh viên của môn học
        TaiDuLieu()

    cb_mh.bind("<<ComboboxSelected>>", on_mh_selected)

    # ==========================================================
    # =================== CỬA SỔ THÊM SINH VIÊN =================
    # ==========================================================
    def open_add_sv_frame():
        mh_selected = cb_mh.get().strip()
        if not mh_selected:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn môn học!")
            return
        
        ma_mh = mh_selected.split(" - ")[0]

        add_window = tk.Toplevel(frame_right)
        add_window.title("Thêm sinh viên vào môn học")
        add_window.geometry("700x500")
        add_window.resizable(False, False)
        add_window.transient(frame_right)
        add_window.grab_set()
        add_window.focus_set()

        tk.Label(add_window, text=f"Môn học: {mh_selected}", font=("Times New Roman", 14, "bold")).pack(pady=10)

        # Thanh tìm kiếm
        search_frame = tk.Frame(add_window)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Tìm sinh viên: ").pack(side="left")
        entry_search = tk.Entry(search_frame, width=30)
        entry_search.pack(side="left", padx=5)

        # Bảng sinh viên
        table_sv = tk.Frame(add_window, bg="white", bd=2, relief="groove")
        table_sv.pack(padx=10, pady=5, fill="both", expand=True)

        v_scroll_sv = ttk.Scrollbar(table_sv, orient="vertical")
        h_scroll_sv = ttk.Scrollbar(table_sv, orient="horizontal")

        columns_sv = ("MSSV", "Họ tên", "Lớp", "Khoa")
        tree_sv = ttk.Treeview(
            table_sv,
            columns=columns_sv,
            show="headings",
            yscrollcommand=v_scroll_sv.set,
            xscrollcommand=h_scroll_sv.set,
            height=12
        )

        v_scroll_sv.config(command=tree_sv.yview)
        h_scroll_sv.config(command=tree_sv.xview)

        table_sv.grid_rowconfigure(0, weight=1)
        table_sv.grid_columnconfigure(0, weight=1)

        tree_sv.grid(row=0, column=0, sticky="nsew")
        v_scroll_sv.grid(row=0, column=1, sticky="ns")
        h_scroll_sv.grid(row=1, column=0, sticky="ew")

        for col, w in zip(columns_sv, (60, 200, 30, 150)):
            tree_sv.heading(col, text=col)
            tree_sv.column(col, width=w, anchor="center")

        btns = tk.Frame(add_window)
        btns.pack(pady=10)

        ttk.Button(btns, text="Thêm vào môn học", width=25, command=lambda: them_sv()).pack(side="left", padx=5)
        ttk.Button(btns, text="Thoát", width=15, command=add_window.destroy).pack(side="right", padx=5)

        def load_sv(filter_text=""):
            for item in tree_sv.get_children():
                tree_sv.delete(item)
            try:
                conn = get_db_connect()
                cursor = conn.cursor()
                if filter_text:
                    cursor.execute("SELECT MSSV, HoTen, Lop, Khoa FROM SinhVien WHERE HoTen LIKE ?", (f"%{filter_text}%",))
                else:
                    cursor.execute("SELECT MSSV, HoTen, Lop, Khoa FROM SinhVien")
                for row in cursor.fetchall():
                    tree_sv.insert("", "end", values=tuple(row))
            finally:
                conn.close()

        def them_sv():
            selected = tree_sv.selection()
            if not selected:
                messagebox.showwarning("Chưa chọn", "Vui lòng chọn sinh viên để thêm.")
                return
            try:
                conn = get_db_connect()
                cursor = conn.cursor()
                added = 0
                for item in selected:
                    mssv = tree_sv.item(item, "values")[0]
                    cursor.execute("SELECT COUNT(*) FROM Diem WHERE MaMH=? AND MSSV=?", (ma_mh, mssv))
                    if cursor.fetchone()[0] == 0:
                        cursor.execute("INSERT INTO Diem (MaMH, MSSV, DiemQT, DiemCK) VALUES (?, ?, NULL, NULL)", (ma_mh, mssv))
                        added += 1
                conn.commit()
                messagebox.showinfo("Thành công", f"Đã thêm {added} sinh viên vào môn học.")
                TaiDuLieu()
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
            finally:
                conn.close()

        entry_search.bind("<KeyRelease>", lambda e: load_sv(entry_search.get()))
        load_sv()
