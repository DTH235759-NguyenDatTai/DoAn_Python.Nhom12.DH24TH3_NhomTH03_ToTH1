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

def show_diem(frame_right, username):
    # ===== Xóa nội dung cũ =====
    for widget in frame_right.winfo_children():
        widget.destroy()

    frame_right.configure(bg="white")

    # ======= Tiêu đề =======
    lbl_title = tk.Label(
        frame_right, text="BẢNG ĐIỂM SINH VIÊN", 
        font=("Times New Roman", 16, "bold"),
        fg="darkred", bg="white"
    )
    lbl_title.pack(pady=5)

    # Frame chứa canvas và scrollbar
    canvas_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    canvas_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Canvas để cuộn
    canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
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
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())
    
    canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width))
    scrollable_frame.bind('<Configure>', update_canvas_scroll)
    
    # Biến để lưu các widget bảng để xóa khi load lại
    table_widgets = []

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
                  "Điểm\nGiữa Kỳ", "Điểm\nCuối Kỳ", "Điểm\nTổng", "Điểm\nChữ"]
        col_widths = [50, 90, 200, 50, 60, 60, 90, 90, 90, 70]
        
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
            
            row_frame = tk.Frame(table_container, bg=bg_color)
            row_frame.pack(fill="x")
            table_widgets.append(row_frame)
            
            ma_mh, ten_mh, so_tc, pt_kt, pt_thi, diem_qt, diem_ck = row_data
            
            # Tính điểm tổng kết
            diem_tk = None
            diem_chu = None
            if diem_qt is not None and diem_ck is not None:
                diem_tk = round(diem_qt * pt_kt/100 + diem_ck * pt_thi/100, 2)
                diem_chu = chuyen_doi_diem_chu(diem_tk)
                if diem_tk >= 5.0:
                    tong_tin_chi_dat += so_tc
                tong_diem_tk += diem_tk * so_tc
                tong_tin_chi += so_tc
            
            # Chuẩn bị dữ liệu hiển thị
            values = [
                str(idx),
                ma_mh,
                ten_mh,
                str(so_tc),
                f"{pt_kt}%",
                f"{pt_thi}%",
                f"{diem_qt:.2f}" if diem_qt is not None else "",
                f"{diem_ck:.2f}" if diem_ck is not None else "",
                f"{diem_tk:.2f}" if diem_tk is not None else "",
                diem_chu if diem_chu is not None else ""
            ]
            
            # Tạo các cell
            for col_idx, (value, width) in enumerate(zip(values, col_widths)):
                cell = tk.Label(
                    row_frame,
                    text=value,
                    bg=bg_color,
                    font=("Arial", 10),
                    width=width//8,
                    height=2,
                    relief="solid",
                    borderwidth=1,
                    anchor="center"
                )
                cell.grid(row=0, column=col_idx, sticky="nsew", padx=0, pady=0)
                row_frame.grid_columnconfigure(col_idx, weight=1, minsize=width)
        
        # Phần tóm tắt học kỳ
        summary_frame = tk.Frame(parent_frame, bg="white")
        summary_frame.pack(fill="x", padx=10, pady=(5, 10))
        table_widgets.append(summary_frame)
        
        # Tính GPA
        gpa_10 = tong_diem_tk / tong_tin_chi if tong_tin_chi > 0 else 0
        gpa_4 = chuyen_doi_diem_he_4(gpa_10)
        
        # Tổng kết học kỳ
        summary_data = [
            ("Điểm trung bình học kỳ hệ 10/100:", f"{gpa_10:.2f}"),
            ("Điểm trung bình học kỳ hệ 4:", f"{gpa_4:.2f}"),
            ("Số tín chỉ đạt:", str(tong_tin_chi_dat)),
            ("Số tín chỉ tích lũy:", str(tong_tin_chi)),
            ("Phân loại học lực:", PhanLoaiGPA(gpa_10))
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
                font=("Arial", 10, "bold"),
                anchor="e"
            )
            value_widget.pack(side="right")
            table_widgets.append(value_widget)
        
        return gpa_10, gpa_4, tong_tin_chi, tong_tin_chi_dat

    def XoaBangCu():
        """Xóa tất cả widget trong bảng cũ"""
        for widget in table_widgets:
            widget.destroy()
        table_widgets.clear()

    def TaiDuLieuBang():
        """Tải dữ liệu vào bảng"""
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
            """, (username,))
            
            all_rows = cursor.fetchall()
            conn.close()
            
            if not all_rows:
                no_data_label = tk.Label(
                    scrollable_frame,
                    text="Không có dữ liệu điểm",
                    font=("Arial", 12),
                    bg="white"
                )
                no_data_label.pack(pady=20)
                table_widgets.append(no_data_label)
                return
            
            # Nhóm dữ liệu theo học kỳ và năm học
            data_by_semester = {}
            for row in all_rows:
                key = (row[7], row[8])  # HocKy, NamHoc
                if key not in data_by_semester:
                    data_by_semester[key] = []
                data_by_semester[key].append(row[:7])  # Chỉ lấy thông tin điểm
            
            # Tính tổng tích lũy
            tong_diem_tich_luy = 0
            tong_tc_tich_luy = 0
            tong_tc_dat_tich_luy = 0
            
            # Tạo bảng cho từng học kỳ theo thứ tự: năm học tăng dần, học kỳ tăng dần
            sorted_semesters = sorted(data_by_semester.items(), 
                                    key=lambda x: (x[0][1].split('-')[0], int(x[0][0]))) 
            
            for (hoc_ky, nam_hoc), data in sorted_semesters:
                gpa_10, gpa_4, tc, tc_dat = TaoBangDiem(data, hoc_ky, nam_hoc, scrollable_frame)
                tong_diem_tich_luy += gpa_10 * tc
                tong_tc_tich_luy += tc
                tong_tc_dat_tich_luy += tc_dat
            
            # Hiển thị tổng tích lũy nếu có nhiều học kỳ
            if len(data_by_semester) > 1:
                tk.Label(
                    scrollable_frame,
                    text="TỔNG KẾT TÍCH LŨY",
                    font=("Arial", 13, "bold"),
                    bg="white",
                    fg="darkred"
                ).pack(anchor="w", pady=(20, 5), padx=10)
                
                summary_frame = tk.Frame(scrollable_frame, bg="white")
                summary_frame.pack(fill="x", padx=10, pady=(5, 10))
                table_widgets.append(summary_frame)
                
                # Tính điểm tích lũy
                gpa_tich_luy_10 = tong_diem_tich_luy / tong_tc_tich_luy if tong_tc_tich_luy > 0 else 0
                gpa_tich_luy_4 = chuyen_doi_diem_he_4(gpa_tich_luy_10)
                
                summary_data = [
                    ("Điểm trung bình tích lũy hệ 10/100:", f"{gpa_tich_luy_10:.2f}"),
                    ("Điểm trung bình tích lũy hệ 4:", f"{gpa_tich_luy_4:.2f}"),
                    ("Tổng số tín chỉ đạt:", str(tong_tc_dat_tich_luy)),
                    ("Tổng số tín chỉ tích lũy:", str(tong_tc_tich_luy)),
                    ("Phân loại học lực:", PhanLoaiGPA(gpa_tich_luy_10))
                ]
                
                for label_text, value_text in summary_data:
                    row_frame = tk.Frame(summary_frame, bg="white")
                    row_frame.pack(fill="x", pady=2)
                    table_widgets.append(row_frame)
                    
                    label_widget = tk.Label(
                        row_frame,
                        text=label_text,
                        bg="white",
                        font=("Arial", 10, "bold"),
                        anchor="w"
                    )
                    label_widget.pack(side="left")
                    table_widgets.append(label_widget)
                    
                    value_widget = tk.Label(
                        row_frame,
                        text=value_text,
                        bg="white",
                        font=("Arial", 10, "bold"),
                        anchor="e"
                    )
                    value_widget.pack(side="right")
                    table_widgets.append(value_widget)
            
            update_canvas_scroll()
            
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # Tải dữ liệu khi form được mở
    TaiDuLieuBang()

    

