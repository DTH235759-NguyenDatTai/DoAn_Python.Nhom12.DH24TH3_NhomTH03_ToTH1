import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import get_db_connect

def add_mh(frame_right):
    # ===== Xóa nội dung cũ =====
    for widget in frame_right.winfo_children():
        widget.destroy()

    frame_right.configure(bg="white")

    # ===== Tiêu đề =====
    lbl_title = tk.Label(frame_right, text="THÊM MÔN HỌC",
        font=("Times New Roman", 16, "bold"), fg="darkred", bg="white"
    )
    lbl_title.pack(pady=5)

    # ==========================================================
    # ===================== KHUNG NHẬP LIỆU ====================
    # ==========================================================
    input_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    input_frame.pack(padx=5, pady=5, fill="x")

    tk.Label(input_frame, text="Mã môn học:", font=("Times New Roman", 12, "bold"), bg="white").grid(row=0, column=0, padx=5, pady=6, sticky="e")
    entry_mamh = tk.Entry(input_frame, font=("Times New Roman", 12), width=22)
    entry_mamh.grid(row=0, column=1, padx=5, pady=6, ipady=2, sticky="w")

    tk.Label(input_frame, text="Tên môn học:", font=("Times New Roman", 12, "bold"), bg="white").grid(row=1, column=0, padx=5, pady=6, sticky="e")
    entry_tenmh = tk.Entry(input_frame, font=("Times New Roman", 12), width=22)
    entry_tenmh.grid(row=1, column=1, padx=5, pady=6, ipady=2, sticky="w")

    tk.Label(input_frame, text="Số tín chỉ:", font=("Times New Roman", 12, "bold"), bg="white").grid(row=2, column=0, padx=5, pady=6, sticky="e")
    entry_stc = tk.Entry(input_frame, font=("Times New Roman", 12), width=22)
    entry_stc.grid(row=2, column=1, padx=5, pady=6, ipady=2, sticky="w")

    # ==========================================================
    # ===================== NÚT CHỨC NĂNG ======================
    # ==========================================================
    
    btn_frame = tk.Frame(frame_right, bg="white")
    btn_frame.pack(pady=10)
    # Nút
    ttk.Button(btn_frame, text="Thêm", width=20, command=lambda: Them()).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Sửa", width=20, command=lambda: Sua()).grid(row=0, column=1, padx=10)
    ttk.Button(btn_frame, text="Xóa", width=20, command=lambda: Xoa()).grid(row=0, column=2, padx=10)

    # ==========================================================
    # ================= BẢNG HIỂN THỊ DỮ LIỆU ==================
    # ==========================================================

    table_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    table_frame.pack(padx=5, pady=5, fill="both", expand=True)

    columns = ("ma_mh", "ten_mh", "so_tc")

    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    tree.grid(row=0, column=0, sticky="nsew")
    v_scroll.grid(row=0, column=1, sticky="ns")
    h_scroll.grid(row=1, column=0, sticky="ew")

    # Cho phép co giãn
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    # ====== CẤU HÌNH CỘT ======
    tree.heading("ma_mh", text="Mã MH")
    tree.column("ma_mh", width=80, anchor="center")

    tree.heading("ten_mh", text="Tên MH")
    tree.column("ten_mh", width=180, anchor="w")

    tree.heading("so_tc", text="Số TC")
    tree.column("so_tc", width=50, anchor="center")

    # ==========================================================
    # ===================== HÀM CHỨC NĂNG ======================
    # ==========================================================

    conn = get_db_connect()
    if conn is None:
        return
    cursor = conn.cursor()
    
    def TaiDuLieu():
        for item in tree.get_children():
            tree.delete(item)
        try:
            cursor.execute("SELECT * FROM MonHoc")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=tuple(row))
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def Them():
        ma_mh = entry_mamh.get().strip()
        ten_mh = entry_tenmh.get().strip()
        so_tc = entry_stc.get().strip()

        if not all([ma_mh, ten_mh, so_tc]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            so_tc = int(so_tc)
        except ValueError:
            messagebox.showwarning("Sai định dạng", "Số tín chỉ phải là số nguyên.")
            return

        conn = get_db_connect()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            sql = """INSERT INTO MonHoc (MaMH, TenMH, SoTinChi)
                     VALUES (?, ?, ?)"""
            cursor.execute(sql, (ma_mh, ten_mh, so_tc))
            conn.commit()
            messagebox.showinfo("Thành công", "Thêm môn học thành công.")
            TaiDuLieu()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def Xoa():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn môn học để xóa.")
            return
        ma_mh = tree.item(selected[0], "values")[0]
        conn = get_db_connect()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM MonHoc WHERE MaMH = ?", (ma_mh))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa môn học.")
            TaiDuLieu()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def Sua():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn môn học để sửa.")
            return
        ma_mh = tree.item(selected[0], "values")[0]
        ten_mh = entry_tenmh.get().strip()
        so_tc = entry_stc.get().strip()

        if not all([ten_mh, so_tc]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            so_tc = int(so_tc)
        except ValueError:
            messagebox.showwarning("Sai định dạng", "Số tín chỉ phải là số nguyên.")
            return

        conn = get_db_connect()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE MonHoc
                SET TenMH=?, SoTinChi=?
                WHERE MaMH=?
            """, (ten_mh, so_tc, ma_mh))
            conn.commit()
            messagebox.showinfo("Thành công", "Cập nhật thành công.")
            TaiDuLieu()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    # ===== Tải dữ liệu ban đầu =====
    TaiDuLieu()
