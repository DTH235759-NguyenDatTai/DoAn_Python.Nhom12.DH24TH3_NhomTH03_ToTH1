import tkinter as tk
from tkinter import ttk

def add_mh(frame_right, username):
    # Xóa nội dung cũ
    for widget in frame_right.winfo_children():
        widget.destroy()
    
    # ====== Tiêu đề ======
    lbl_title = tk.Label(
        frame_right,
        text="THÊM MÔN HỌC",
        font=("Times New Roman", 16, "bold"),
        fg="darkred",
        bg="white"
    )
    lbl_title.pack(pady=2)
    # ===== Khung nội dung =====
    content_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    content_frame.pack(padx=5, pady=3, fill="both", expand=True)

    # ===== Cấu hình grid cho content_frame =====
    # Hàng 0 (input_frame) sẽ không co giãn
    content_frame.grid_rowconfigure(0, weight=0) 
    # Hàng 1 (table_frame) sẽ co giãn để lấp đầy
    content_frame.grid_rowconfigure(1, weight=1) 
    # Cột 0 sẽ co giãn lấp đầy
    content_frame.grid_columnconfigure(0, weight=1)

    # ==========================================================
    # ===== Khung nhập liệu (bên trên) =====
    # ==========================================================
    input_frame = tk.Frame(content_frame, bg="white", bd=2, relief="groove")
    # THAY ĐỔI: Sử dụng .grid() thay vì .pack()
    input_frame.grid(row=0, column=0, padx=0, pady=0, sticky="ew") # "ew" = East-West (co giãn ngang)


    # ===== Danh sách nhãn =====
    Labels = [
        "Mã môn học:", "Tên môn học:", "Năm học:",
        "Giảng viên:", "Phòng:", "Học kì:"
    ]

    # tạo các widget riêng rồi gom vào danh sách
    entry_mamh = tk.Entry(input_frame, font=("Times New Roman", 12), bg="#e6f0ff", width=22, justify="left")
    entry_tenmh = tk.Entry(input_frame, font=("Times New Roman", 12), bg="#e6f0ff", width=22, justify="left")
    cb_namhoc = ttk.Combobox(input_frame, font=("Times New Roman", 12), width=20,
                             values=["2022–2023", "2023–2024", "2024–2025"])
    cb_gv = ttk.Combobox(input_frame, font=("Times New Roman", 12), width=20,
                         values=["Thầy A", "Cô B", "Thầy C"])
    entry_phong = tk.Entry(input_frame, font=("Times New Roman", 12), bg="#e6f0ff", width=22, justify="left")
    entry_hocky = tk.Entry(input_frame, font=("Times New Roman", 12), bg="#e6f0ff", width=22, justify="left")

    Entrys = [entry_mamh, entry_tenmh, cb_namhoc, cb_gv, entry_phong, entry_hocky]

    for i in range(3):  # 3 hàng mỗi bên
        # --- Cột trái ---
        tk.Label(input_frame, text=Labels[i], font=("Times New Roman", 11, "bold"),
                bg="white", anchor="w").grid(row=i, column=0, padx=5, pady=8, sticky="w")
        Entrys[i].grid(row=i, column=1, padx=5, pady=8, sticky="w")

        # --- Cột phải ---
        tk.Label(input_frame, text=Labels[i+3], font=("Times New Roman", 11, "bold"),
                bg="white", anchor="w").grid(row=i, column=2, padx=(30, 5), pady=8, sticky="w")
        Entrys[i+3].grid(row=i, column=3, padx=5, pady=8, sticky="w")

    # ===== Căn đều cột =====
    for j in range(4):
        input_frame.grid_columnconfigure(j, weight=1)
    
    # ======= Phím chức năng ======
    # Lable chứa các nút
    btn_frame = tk.Frame(input_frame, bg="white")
    btn_frame.grid(row=3, column=0, columnspan=4, pady=10)

    buttons = ["Thêm", "Sửa", "Xóa"]

    for i, text in enumerate(buttons):
        btn = ttk.Button(btn_frame, text=text, width=20)
        btn.grid(row=0, column=i, padx=10, pady=10)

    # ==========================================================
    # ===== KHUNG BẢNG DỮ LIỆU (TREEVIEW) =====
    # ==========================================================
    
    # Đặt khung table_frame vào content_frame, bên dưới input_frame
    table_frame = tk.Frame(content_frame, bg="white", bd=2, relief="groove")
    # THAY ĐỔI: Sử dụng .grid() thay vì .pack()
    table_frame.grid(row=4, column=0, padx=0, pady=5, sticky="nsew") # "nsew" = co giãn 4 chiều

    # --- Cấu hình grid cho table_frame để treeview và scrollbar co giãn ---
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    # --- Thanh cuộn ---
    v_scroll = ttk.Scrollbar(table_frame, orient="vertical")
    h_scroll = ttk.Scrollbar(table_frame, orient="horizontal")

    # --- Treeview ---
    columns = ("ma_mh", "ten_mh", "nam_hoc", "giang_vien", "phong", "hoc_ky")
    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        yscrollcommand=v_scroll.set, # Kết nối thanh cuộn dọc
        xscrollcommand=h_scroll.set  # Kết nối thanh cuộn ngang
    )

    # --- Liên kết thanh cuộn với Treeview ---
    v_scroll.config(command=tree.yview)
    h_scroll.config(command=tree.xview)

    # --- Đặt Treeview và thanh cuộn vào grid của table_frame ---
    tree.grid(row=0, column=0, sticky="nsew") # 'nsew' để treeview co giãn 4 chiều
    v_scroll.grid(row=0, column=1, sticky="ns") # 'ns' để cuộn dọc
    h_scroll.grid(row=1, column=0, sticky="ew") # 'ew' để cuộn ngang

    # --- Định nghĩa các cột ---
    tree.heading("ma_mh", text="Mã MH")
    tree.heading("ten_mh", text="Tên Môn Học")
    tree.heading("nam_hoc", text="Năm Học")
    tree.heading("giang_vien", text="Giảng Viên")
    tree.heading("phong", text="Phòng")
    tree.heading("hoc_ky", text="Học Kỳ")

    # --- Cài đặt độ rộng cột (tùy chọn) ---
    tree.column("ma_mh", width=80, anchor="w")
    tree.column("ten_mh", width=200, anchor="w")
    tree.column("nam_hoc", width=100, anchor="center")
    tree.column("giang_vien", width=150, anchor="w")
    tree.column("phong", width=80, anchor="center")
    tree.column("hoc_ky", width=80, anchor="center")

    # --- Thêm dữ liệu mẫu (để bạn thấy kết quả) ---
    sample_data = [
        ("CS101", "Nhập môn Lập trình", "2023–2024", "Thầy A", "A1-101", "1"),
        ("MA101", "Giải tích 1", "2023–2024", "Cô B", "B2-202", "1"),
        ("PH101", "Vật lý 1", "2023–2024", "Thầy C", "C3-303", "2")
    ]
    for item in sample_data:
        tree.insert("", "end", values=item)