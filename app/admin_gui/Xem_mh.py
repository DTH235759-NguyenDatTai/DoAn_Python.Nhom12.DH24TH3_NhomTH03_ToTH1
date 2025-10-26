import tkinter as tk
from tkinter import ttk

def xem_mh(frame_right):
    # Tạo bảng gồm có các cột thông tin của môn học và có thể xem danh sách sinh viên trong đó

    table_frame = tk.Frame(frame_right, bg="white", bd=2, relief="groove")
    table_frame.pack(fill="both", expand=True, pady=5)
    # Thanh cuộc dọc và ngang
    v_scroll = ttk.Scrollbar(table_frame, orient="vertical")
    h_scroll = ttk.Scrollbar(table_frame, orient="horizontal")

    columns = ("ma_mh","ten_mh", "so_tc", "pt_kt", "pt_thi", "phong", "hoc_ky", "nam_hoc", "ma_gv")
    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        yscrollcommand=v_scroll.set,
        xscrollcommand=h_scroll.set
    )

    v_scroll.config(command=tree.yview)
    h_scroll.config(command=tree.xview)
    tree.grid(row=0, column=0, sticky="nsew")
    v_scroll.grid(row=0, column=1, sticky="ns")
    h_scroll.grid(row=1, column=0, sticky="ew")

    # ===== Cấu hình cột =====
    tree.heading("ma_mh", text="Mã MH")
    tree.heading("ten_mh", text="Tên MH")
    tree.heading("so_tc", text="Số TC")
    tree.heading("pt_kt", text="%Kt")
    tree.heading("pt_thi", text="%Thi")
    tree.heading("phong", text="Phòng")
    tree.heading("hoc_ky", text="Học Kỳ")
    tree.heading("nam_hoc", text="Năm Học")
    tree.heading("ma_gv", text="Mã GV")

    tree.column("ma_mh", width=120, anchor="center")
    tree.column("ten_mh", width=180, anchor="center")
    tree.column("so_tc", width=80, anchor="center")
    tree.column("pt_kt", width=80, anchor="center")
    tree.column("pt_thi", width=80, anchor="center")
    tree.column("phong", width=110, anchor="center")
    tree.column("hoc_ky", width=80, anchor="center")
    tree.column("nam_hoc", width=100, anchor="center")
    tree.column("ma_gv", width=100, anchor="center")