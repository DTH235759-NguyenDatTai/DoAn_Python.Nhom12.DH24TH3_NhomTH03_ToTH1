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

    tk.Label(input_frame, text="Chọn môn học:", font=("Times New Roman", 12, "bold"), bg="white").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    cb_mh = ttk.Combobox(input_frame, font=("Times New Roman", 12), width=40, state="readonly")
    cb_mh.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Lấy danh sách môn học từ SQL (hiển thị mã và tên môn học)
    conn = get_db_connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MaMH, TenMH FROM MonHoc ORDER BY NamHoc DESC, HocKy ASC")
        mh_list = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        cb_mh["values"] = mh_list
        conn.close()

    # ==========================================================
    # ===================== NÚT CHỨC NĂNG ======================
    # ==========================================================

    btn_frame = tk.Frame(frame_right, bg="white")
    btn_frame.pack(pady=10)
    ttk.Button(btn_frame, text="Xem danh sách SV", width=20, command=lambda: TaiDuLieu()).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Thêm sinh viên", width=20, command=lambda: open_add_sv_frame()).grid(row=0, column=1, padx=10)
    ttk.Button(btn_frame, text="Xóa sinh viên", width=20, command=lambda: Xoa()).grid(row=0, column=2, padx=10)
    ttk.Button(btn_frame, text="Làm mới", width=20, command=lambda: LamMoi()).grid(row=0, column=3, padx=10)

    # ==========================================================
    # ================= BẢNG HIỂN THỊ DỮ LIỆU ==================
    # ==========================================================

    table_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    table_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # ===== Treeview =====
    tree = ttk.Treeview(
        table_frame,
        columns=("MSSV", "Họ tên", "Lớp", "Khoa"),
        show="headings",
        height=8
    )

    # Cấu hình cột
    tree.heading("MSSV", text="MSSV")
    tree.column("MSSV", width=50, anchor="center")

    tree.heading("Họ tên", text="Họ tên")
    tree.column("Họ tên", width=120, anchor="center")

    tree.heading("Lớp", text="Lớp")
    tree.column("Lớp", width=50, anchor="center")

    tree.heading("Khoa", text="Khoa")
    tree.column("Khoa", width=150, anchor="center")

    # ===== Thanh cuộn =====
    v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    # ===== Dùng grid để canh chỉnh =====
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
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn môn học!")
            return
        
        # Lấy mã môn học từ chuỗi "MaMH - TenMH"
        ma_mh = mh_selected.split(" - ")[0] if " - " in mh_selected else mh_selected

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
            rows = cursor.fetchall()
            for row in rows:
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
        
        # Lấy mã môn học từ chuỗi "MaMH - TenMH"
        ma_mh = mh_selected.split(" - ")[0] if " - " in mh_selected else mh_selected
        
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
        """Làm mới form"""
        cb_mh.set("")
        for row in tree.get_children():
            tree.delete(row)

    def open_add_sv_frame():
        """Mở cửa sổ thêm sinh viên vào môn học"""
        mh_selected = cb_mh.get().strip()
        if not mh_selected:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn môn học!")
            return
        
        # Lấy mã môn học từ chuỗi "MaMH - TenMH"
        ma_mh = mh_selected.split(" - ")[0] if " - " in mh_selected else mh_selected

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

        # ======= KHUNG CHỨA BẢNG SINH VIÊN =======
        table_sv = tk.Frame(add_window, bg="white", bd=2, relief="groove")
        table_sv.pack(padx=10, pady=5, fill="both", expand=True)
        table_sv.pack_propagate(False)  # Giữ kích thước khung, không co lại

        # ======= THANH CUỘN =======
        v_scroll_sv = ttk.Scrollbar(table_sv, orient="vertical")
        h_scroll_sv = ttk.Scrollbar(table_sv, orient="horizontal")

        columns_sv = ("MSSV", "Họ tên", "Lớp", "Khoa")
        tree_sv = ttk.Treeview(
            table_sv,
            columns=columns_sv,
            show="headings",
            yscrollcommand=v_scroll_sv.set,
            xscrollcommand=h_scroll_sv.set
        )

        # Liên kết thanh cuộn
        v_scroll_sv.config(command=tree_sv.yview)
        h_scroll_sv.config(command=tree_sv.xview)

        v_scroll_sv.pack(side="right", fill="y")    # Cuộn dọc bên phải
        h_scroll_sv.pack(side="bottom", fill="x")   # Cuộn ngang bên dưới
        tree_sv.pack(side="left", fill="both", expand=True)  # Bảng chiếm phần còn lại

        # ======= CẤU HÌNH CỘT =======
        for col in columns_sv:
            tree_sv.heading(col, text=col)
            tree_sv.column(col, width=180, anchor="center")  # đặt rộng hơn khung để test cuộn ngang

        # ======= NÚT =======
        btns = tk.Frame(add_window)
        btns.pack(pady=10)

        ttk.Button(btns, text="Thêm vào môn học", width=25, command=them_sv).pack(side="left", padx=5)
        ttk.Button(btns, text="Thoát", width=15, command=add_window.destroy).pack(side="right", padx=5)

        def load_sv(filter_text=""):
            """Tải danh sách sinh viên từ bảng SinhVien"""
            tree_sv.delete(*tree_sv.get_children())
            conn = None
            try:
                conn = get_db_connect()
                if conn is None:
                    messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu.")
                    return
                cursor = conn.cursor()
                if filter_text:
                    cursor.execute("SELECT MSSV, HoTen, Lop, Khoa FROM SinhVien WHERE HoTen LIKE ? ORDER BY MSSV", (f"%{filter_text}%",))
                else:
                    cursor.execute("SELECT MSSV, HoTen, Lop, Khoa FROM SinhVien ORDER BY MSSV")
                rows = cursor.fetchall()
                for row in rows:
                    tree_sv.insert("", "end", values=tuple(row))
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải danh sách sinh viên: {str(e)}")
            finally:
                if conn:
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
                skipped = 0
                for item in selected:
                    mssv = tree_sv.item(item, "values")[0]
                    cursor.execute("SELECT COUNT(*) FROM Diem WHERE MaMH=? AND MSSV=?", (ma_mh, mssv))
                    if cursor.fetchone()[0] == 0:
                        cursor.execute("INSERT INTO Diem (MaMH, MSSV, DiemQT, DiemCK) VALUES (?, ?, NULL, NULL)", (ma_mh, mssv))
                        added += 1
                    else:
                        skipped += 1
                conn.commit()
                if added > 0:
                    messagebox.showinfo("Thành công", f"Đã thêm {added} sinh viên vào môn học.\n{skipped} sinh viên đã tồn tại.")
                else:
                    messagebox.showwarning("Thông báo", f"Tất cả sinh viên đã được thêm vào môn học.")
                TaiDuLieu()
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
            finally:
                conn.close()

        entry_search.bind("<KeyRelease>", lambda e: load_sv(entry_search.get()))
        load_sv()

