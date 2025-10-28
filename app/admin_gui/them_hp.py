import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import get_db_connect

def add_hp(frame_right):
    # ===== Xóa nội dung cũ =====
    for widget in frame_right.winfo_children():
        widget.destroy()

    frame_right.configure(bg="white")

    # ======= Tiêu đề =======
    lbl_title = tk.Label(
        frame_right, text="THÊM HỌC PHẦN", font=("Times New Roman", 16, "bold"),
        fg="darkred", bg="white"
    )
    lbl_title.pack(pady=5)

    # ==========================================================
    # ===================== KHUNG NHẬP LIỆU ====================
    # ==========================================================
    input_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    input_frame.pack(padx=5, pady=5, fill="x")

    tk.Label(input_frame, text="Mã học phần:", font=("Times New Roman", 12, "bold")).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_mahp = tk.Entry(input_frame, font=("Times New Roman", 12), width=25)
    entry_mahp.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(input_frame, text="Mã môn học:", font=("Times New Roman", 12, "bold")).grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_mamh = tk.Entry(input_frame, font=("Times New Roman", 12), width=25)
    entry_mamh.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    tk.Label(input_frame, text="Mã giảng viên:", font=("Times New Roman", 12, "bold")).grid(row=3, column=0, sticky="e", padx=5, pady=5)
    entry_magv = tk.Entry(input_frame, font=("Times New Roman", 12), width=25)
    entry_magv.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    tk.Label(input_frame, text="Học kỳ:", font=("Times New Roman", 12, "bold")).grid(row=4, column=0, sticky="e", padx=5, pady=5)
    entry_hocky = tk.Entry(input_frame, font=("Times New Roman", 12), width=25)
    entry_hocky.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    tk.Label(input_frame, text="Năm học:", font=("Times New Roman", 12, "bold")).grid(row=5, column=0, sticky="e", padx=5, pady=5)
    entry_namhoc = tk.Entry(input_frame, font=("Times New Roman", 12), width=25)
    entry_namhoc.grid(row=5, column=1, padx=5, pady=5, sticky="w")

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
    # Cho phép co giãn
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)


    cot = ("Mã HP", "Mã MH", "Mã GV", "Học Kỳ", "Năm Học")
    tree = ttk.Treeview(table_frame, columns=cot, show="headings")

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

    # ====== Kết nối database ======
    conn = get_db_connect()
    if conn is None:
        return
    cursor = conn.cursor()

    def TaiDuLieu():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor.execute("SELECT * FROM HocPhan")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=tuple(row))
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def Them():
        try:
            MaHP = entry_mahp.get()
            MaMH = entry_mamh.get()
            MaGV = entry_magv.get()
            HocKy = entry_hocky.get()
            NamHoc = entry_namhoc.get()

            if MaHP == "" or MaMH == "" or MaGV == "" or HocKy == "":
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin!")
                return

            cursor.execute("INSERT INTO HocPhan (MaHP, MaMH, MaGV, HocKy, NamHoc) VALUES (?, ?, ?, ?, ?)",
                           (MaHP, MaMH, MaGV, HocKy, NamHoc))
            conn.commit()
            messagebox.showinfo("Thành công", "Thêm học phần thành công!")
            TaiDuLieu()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def Sua():
        try:
            MaHP = entry_mahp.get()
            MaMH = entry_mamh.get()
            MaGV = entry_magv.get()
            HocKy = entry_hocky.get()
            NamHoc = entry_namhoc.get()

            cursor.execute("UPDATE HocPhan SET MaMH=?, MaGV=?, HocKy=?, NamHoc=? WHERE MaHP=?",
                           (MaMH, MaGV, HocKy, NamHoc, MaHP))
            conn.commit()
            messagebox.showinfo("Thành công", "Cập nhật học phần thành công!")
            TaiDuLieu()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def Xoa():
        try:
            MaHP = entry_mahp.get()
            if MaHP == "":
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Mã học phần cần xóa!")
                return

            cursor.execute("DELETE FROM HocPhan WHERE MaHP=?", (MaHP,))
            conn.commit()
            messagebox.showinfo("Thành công", "Xóa học phần thành công!")
            TaiDuLieu()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ===== Tải dữ liệu ban đầu =====
    TaiDuLieu()