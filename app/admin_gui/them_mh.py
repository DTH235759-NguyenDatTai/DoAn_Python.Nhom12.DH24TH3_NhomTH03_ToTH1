import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
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

    tk.Label(input_frame, text="%KT/%Thi:", font=("Times New Roman", 12, "bold"), bg="white").grid(row=3, column=0, padx=5, pady=6, sticky="e")
    cb_pt = ttk.Combobox(input_frame, font=("Times New Roman", 12, "bold"), width=25,
                        values=["50/50", "40/60"], state="readonly")
    cb_pt.grid(row=3, column=1, padx=5, pady=6, sticky="w")
    
    tk.Label(input_frame, text="Học kỳ:", font=("Times New Roman", 12, "bold"), bg="white").grid(row=0, column=2, sticky="e", padx=5, pady=5)
    cb_hocky = ttk.Combobox(input_frame, font=("Times New Roman", 12), width=25, values=["1", "2", "3"], state="readonly")
    cb_hocky.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(input_frame, text="Năm học:", font=("Times New Roman", 12, "bold"), bg="white").grid(row=1, column=2, sticky="e", padx=5, pady=5)
    cb_namhoc = ttk.Combobox(input_frame, font=("Times New Roman", 12), width=25, state="readonly")
    cb_namhoc.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    # Lấy năm học từ 2020 đến 2030
    namhoc_values = [f"{y}-{y+1}" for y in range(2020, 2031)]
    cb_namhoc["values"] = namhoc_values
    current_year = datetime.now().year
    default_value = f"{current_year}-{current_year + 1}" if 2020 <= current_year <= 2030 else namhoc_values[0]
    cb_namhoc.set(default_value)

    tk.Label(input_frame, text="Mã giảng viên:", font=("Times New Roman", 12, "bold"), bg="white").grid(row=2, column=2, sticky="e", padx=5, pady=5)
    cb_magv = ttk.Combobox(input_frame, font=("Times New Roman", 12), width=25, state="readonly")
    cb_magv.grid(row=2, column=3, padx=5, pady=5, sticky="w")

    # Lấy danh sách môn học từ SQL
    conn = get_db_connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MaGV FROM GiangVien")
        gv_list = [row[0] for row in cursor.fetchall()]
        cb_magv["values"] = gv_list
        conn.close()


    # ==========================================================
    # ===================== NÚT CHỨC NĂNG ======================
    # ==========================================================
    
    btn_frame = tk.Frame(frame_right, bg="white")
    btn_frame.pack(pady=10)
    # Nút
    ttk.Button(btn_frame, text="Thêm", width=20, command=lambda: Them()).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Sửa", width=20, command=lambda: Sua()).grid(row=0, column=1, padx=10)
    ttk.Button(btn_frame, text="Xóa", width=20, command=lambda: Xoa()).grid(row=0, column=2, padx=10)
    ttk.Button(btn_frame, text="Làm mới", width=20, command=lambda: LamMoi()).grid(row=0, column=3, padx=10)

    # ==========================================================
    # ================= BẢNG HIỂN THỊ DỮ LIỆU ==================
    # ==========================================================

    table_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    table_frame.pack(padx=5, pady=5, fill="both", expand=True)

    columns = ("ma_mh", "ten_mh", "so_tc", "pt_kt", "pt_thi", "hoc_ky", "nam_hoc", "ma_gv")

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
    tree.column("ma_mh", width=90, anchor="center")

    tree.heading("ten_mh", text="Tên MH")
    tree.column("ten_mh", width=220, anchor="w")

    tree.heading("so_tc", text="Số TC")
    tree.column("so_tc", width=60, anchor="center")

    tree.heading("pt_kt", text="% KT")
    tree.column("pt_kt", width=60, anchor="center")

    tree.heading("pt_thi", text="% Thi")
    tree.column("pt_thi", width=60, anchor="center")

    tree.heading("hoc_ky", text="Học kỳ")
    tree.column("hoc_ky", width=70, anchor="center")

    tree.heading("nam_hoc", text="Năm học")
    tree.column("nam_hoc", width=110, anchor="center")

    tree.heading("ma_gv", text="Mã GV")
    tree.column("ma_gv", width=80, anchor="center")

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
            cursor.execute("SELECT * FROM MonHoc ORDER BY HocKy ASC, NamHoc ASC")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=tuple(row))
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def Them():
        ma_mh = entry_mamh.get().strip()
        ten_mh = entry_tenmh.get().strip()
        so_tc = entry_stc.get().strip()
        pt_value = cb_pt.get().strip()
        hoc_ky = cb_hocky.get().strip()
        nam_hoc = cb_namhoc.get().strip()
        ma_gv = cb_magv.get().strip()

        if not all([ma_mh, ten_mh, so_tc, pt_value, hoc_ky, nam_hoc, ma_gv]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            so_tc = int(so_tc)
        except ValueError:
            messagebox.showwarning("Sai định dạng", "Số tín chỉ phải là số nguyên.")
            return

        try:
            pt_kt, pt_thi = map(int, pt_value.split('/'))
        except ValueError:
            messagebox.showwarning("Sai định dạng", "Phần trăm không đúng định dạng (ví dụ: 50/50 hoặc 40/60).")
            return

        try:
            hoc_ky_int = int(hoc_ky)
            if hoc_ky_int not in [1, 2, 3]:
                messagebox.showwarning("Sai định dạng", "Học kỳ phải là 1, 2 hoặc 3.")
                return
        except ValueError:
            messagebox.showwarning("Sai định dạng", "Học kỳ phải là số.")
            return

        conn = get_db_connect()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            # Kiểm tra trùng mã môn học
            cursor.execute("SELECT MaMH FROM MonHoc WHERE MaMH = ?", (ma_mh,))
            if cursor.fetchone():
                messagebox.showwarning("Trùng mã", f"Mã môn học '{ma_mh}' đã tồn tại. Vui lòng chọn mã khác.")
                return
            
            sql = """INSERT INTO MonHoc (MaMH, TenMH, SoTinChi, PtKt, PtThi, HocKy, NamHoc, MaGV)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, (ma_mh, ten_mh, so_tc, pt_kt, pt_thi, hoc_ky_int, nam_hoc, ma_gv))
            conn.commit()
            messagebox.showinfo("Thành công", "Thêm môn học thành công.")
            # Xóa dữ liệu trong form sau khi thêm thành công
            LamMoi()
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
            cursor.execute("DELETE FROM MonHoc WHERE MaMH = ?", (ma_mh,))
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
        pt_value = cb_pt.get().strip()
        hoc_ky = cb_hocky.get().strip()
        nam_hoc = cb_namhoc.get().strip()
        ma_gv = cb_magv.get().strip()

        if not all([ten_mh, so_tc, pt_value, hoc_ky, nam_hoc, ma_gv]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            so_tc = int(so_tc)
        except ValueError:
            messagebox.showwarning("Sai định dạng", "Số tín chỉ phải là số nguyên.")
            return

        try:
            pt_kt, pt_thi = map(int, pt_value.split('/'))
        except ValueError:
            messagebox.showwarning("Sai định dạng", "Phần trăm không đúng định dạng (ví dụ: 50/50 hoặc 40/60).")
            return

        try:
            hoc_ky_int = int(hoc_ky)
            if hoc_ky_int not in [1, 2, 3]:
                messagebox.showwarning("Sai định dạng", "Học kỳ phải là 1, 2 hoặc 3.")
                return
        except ValueError:
            messagebox.showwarning("Sai định dạng", "Học kỳ phải là số.")
            return

        conn = get_db_connect()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE MonHoc
                SET TenMH=?, SoTinChi=?, PtKt=?, PtThi=?, HocKy=?, NamHoc=?, MaGV=?
                WHERE MaMH=?
            """, (ten_mh, so_tc, pt_kt, pt_thi, hoc_ky_int, nam_hoc, ma_gv, ma_mh))
            conn.commit()
            messagebox.showinfo("Thành công", "Cập nhật thành công.")
            # Xóa dữ liệu trong form sau khi sửa thành công
            LamMoi()
            TaiDuLieu()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    # Hàm làm mới form
    def LamMoi():
        entry_mamh.config(state="normal")
        entry_mamh.delete(0, tk.END)
        entry_tenmh.delete(0, tk.END)
        entry_stc.delete(0, tk.END)
        cb_pt.set("")
        cb_hocky.set("")
        # Đặt lại năm học về giá trị mặc định
        current_year = datetime.now().year
        if 2020 <= current_year <= 2030:
            default_namhoc = f"{current_year}-{current_year + 1}"
        else:
            default_namhoc = "2020-2021"
        cb_namhoc.set(default_namhoc)
        cb_magv.set("")
        # Bỏ chọn dòng trong bảng
        for item in tree.selection():
            tree.selection_remove(item)

    # Hàm tự động điền dữ liệu khi chọn dòng trong bảng
    def on_select(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], "values")
            if values and len(values) >= 8:
                # Khóa entry mã môn học khi sửa (chỉ cho đọc, không cho sửa)
                entry_mamh.config(state="normal")
                entry_mamh.delete(0, tk.END)
                entry_mamh.insert(0, values[0] if values[0] else "")
                entry_mamh.config(state="disabled")
                
                entry_tenmh.delete(0, tk.END)
                entry_tenmh.insert(0, values[1] if values[1] else "")
                
                entry_stc.delete(0, tk.END)
                entry_stc.insert(0, str(values[2]) if values[2] else "")
                
                # Điền phần trăm dạng "PtKt/PtThi"
                if values[3] and values[4]:
                    cb_pt.set(f"{values[3]}/{values[4]}")
                else:
                    cb_pt.set("")
                
                # Điền học kỳ
                cb_hocky.set(str(values[5]) if values[5] else "")
                
                # Điền năm học
                cb_namhoc.set(str(values[6]) if values[6] else "")
                
                # Điền mã giảng viên
                cb_magv.set(str(values[7]) if values[7] else "")
    
    # Bind sự kiện chọn dòng
    tree.bind("<<TreeviewSelect>>", on_select)

    # ===== Tải dữ liệu ban đầu =====
    TaiDuLieu()
