from tkinter import messagebox, ttk
import tkinter as tk
from db_connect import get_db_connect

def add_sv(frame_right):
    # ===== Xóa nội dung cũ =====
    for widget in frame_right.winfo_children():
        widget.destroy()

        # ======= Tiêu đề =======
    lbl_title = tk.Label(
        frame_right, text="THÊM SINH VIÊN VÀO HỌC PHẦN", font=("Times New Roman", 16, "bold"),
        fg="darkred", bg="white"
    )
    lbl_title.pack(pady=5)

    # ==========================================================
    # ===================== KHUNG NHẬP LIỆU ====================
    # ==========================================================

    input_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    input_frame.pack(padx=5, pady=5, fill="x")

    tk.Label(input_frame, text="Chọn học phần:", font=("Times New Roman", 12, "bold")).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    cb_hp = ttk.Combobox(input_frame, font=("Times New Roman", 12), width=25,
                            values=["HP001", "HP002", "HP003"])
    cb_hp.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # ==========================================================
    # ===================== NÚT CHỨC NĂNG ======================
    # ==========================================================

    btn_frame = tk.Frame(frame_right, bg="white")
    btn_frame.pack(pady=10)
    # Nút
    ttk.Button(btn_frame, text="Thêm sinh viên", width=20, command=lambda: Them()).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Sửa", width=20, command=lambda: Sua()).grid(row=0, column=1, padx=10)
    ttk.Button(btn_frame, text="Xóa", width=20, command=lambda: Xoa()).grid(row=0, column=2, padx=10)

    # ==========================================================
    # ================= BẢNG HIỂN THỊ DỮ LIỆU ==================
    # ==========================================================

    table_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    table_frame.pack(padx=5, pady=5, fill="both", expand=True)

    # Cho phép bảng co giãn
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    cot = ("MSSV", "Họ Tên", "Ngày Sinh", "Giới Tính", "Lớp", "Khoa")
    tree =ttk.Treeview(table_frame, columns=cot, show="headings")

    v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)   
    tree.grid(row=0, column=0, sticky="nsew")
    v_scroll.grid(row=0, column=1, sticky="ns")
    h_scroll.grid(row=1, column=0, sticky="ew")

    for col in cot:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    
    # ==========================================================
    # ===================== HÀM CHỨC NĂNG ======================
    # ==========================================================

    # ========= Kết nối database ===========
    conn = get_db_connect()
    if conn is None:
        return
    cursor = conn.cursor()

    # ========= frame thêm sinh viên ==========
    def open_add_sv_frame(frame_right, reload_table_callback):
        frame = tk.Toplevel(frame_right)
        frame.title("Thêm sinh viên")
        frame.geometry("600x400")

        tk.Label(frame, text=f"Thêm sinh viên vào học phần", font=("Arial", 13, "bold")).pack(pady=10)

        # Thanh tìm kiếm
        frame_search = tk.Frame(frame)
        frame_search.pack(pady=5)
        tk.Label(frame_search, text="Tìm sinh viên:").pack(side="left", padx=5)
        entry_search = tk.Entry(frame_search, width=30)
        entry_search.pack(side="left", padx=5)

        # Bảng sinh viên
        table = tk.Frame(frame, bg="white", bd=2, relief="groove")
        table.pack(padx=5, pady=5, fill="both", expand=True)

        # Cho phép bảng co giãn
        table.grid_rowconfigure(0, weight=1)
        table.grid_columnconfigure(0, weight=1)

        cotsv = ("MSSV", "Họ Tên", "Ngày Sinh", "Giới Tính", "Lớp", "Khoa")
        tree_sv =ttk.Treeview(table, columns=cot, show="headings")

        v_scroll = ttk.Scrollbar(table, orient="vertical", command=tree_sv.yview)
        h_scroll = ttk.Scrollbar(table, orient="horizontal", command=tree_sv.xview)

        tree_sv.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)   
        tree_sv.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        for col in cotsv:
            tree_sv.heading(col, text=col)
            tree_sv.column(col, width=150, anchor="center")

        def load_sv(filter_text=""):
            # Xóa dữ liệu cũ trong Treeview
            tree_sv.delete(*tree_sv.get_children())

            try:
                conn = get_db_connect()
                cursor = conn.cursor()

                # Nếu có nhập chuỗi tìm kiếm → lọc theo mssv, tên, lớp
                if filter_text.strip() != "":
                    query = """
                        SELECT MSSV, HoTen, Lop
                        FROM SinhVien
                        WHERE HoTen LIKE ?
                    """
                    cursor.execute(query, f"%{filter_text}%")
                else:
                    # Không nhập gì thì lấy tất cả
                    query = "SELECT * FROM SinhVien"
                    cursor.execute(query)

                # Duyệt qua từng dòng kết quả và thêm vào Treeview
                for row in cursor.fetchall():
                    tree_sv.insert("", "end", values=tuple(row))

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải danh sách sinh viên:\n{e}")
            finally:
                if 'conn' in locals():
                    conn.close()
        load_sv()

        # Gắn tìm kiếm
        entry_search.bind("<KeyRelease>", lambda e: load_sv(entry_search.get()))

        # Nút thêm
        def them_sv():
            selected = tree_sv.selection()
            if not selected:
                messagebox.showwarning("Chưa chọn", "Vui lòng chọn sinh viên cần thêm!")
                return

            added = 0
            for item in selected:
                ma_sv, ten_sv = tree_sv.item(item, "values")
                if ma_sv not in [sv[0] for sv in HOC_PHAN_SV[ma_hp]]:
                    HOC_PHAN_SV[ma_hp].append((ma_sv, ten_sv))
                    added += 1

            reload_table_callback()
            messagebox.showinfo("Thành công", f"Đã thêm {added} sinh viên vào {ma_hp}.")

        def xoa_tat_ca():
            if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tất cả sinh viên vừa thêm?"):
                HOC_PHAN_SV[ma_hp].clear()
                reload_table_callback()
                messagebox.showinfo("Đã xóa", f"Đã xóa toàn bộ sinh viên trong học phần {ma_hp}.")

        def thoat():
            frame.destroy()

    def TaiDuLieu():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor.execute("SELECT * FROM SinhVien")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=tuple(row))
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def Them():
        try:
            MaHP = cb_hp.get()

            if MaHP == "":
                messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn học phần!")
                return
            else:
                open_add_sv_frame(frame_right, TaiDuLieu)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
            