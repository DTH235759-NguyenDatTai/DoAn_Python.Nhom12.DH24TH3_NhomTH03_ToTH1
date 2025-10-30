import tkinter as tk
from tkinter import ttk, messagebox

def add_diem(frame_right):
    # ===== Xóa nội dung cũ =====
    for widget in frame_right.winfo_children():
        widget.destroy()

    # ======= Tiêu đề =======
    lbl_title = tk.Label(
        frame_right, text="THÊM ĐIỂM SINH VIÊN", font=("Times New Roman", 16, "bold"),
        fg="darkred", bg="white"
    )

    # ======= Phần nhập liệu =======
    lbl_title.pack(pady=5)
    input_frame = tk.Frame(frame_right, bg = "white", bd = 2, relief = "groove")
    input_frame.pack(padx=5, pady = 5, fill = "x")

    lbl_hp = tk.Label(input_frame, text = "Chọn học phần:", font = ("Times New Roman", 12, "bold"), bg = "white")
    lbl_hp.grid(row = 0, column = 0, padx = 5, pady = 5,sticky = "e")
    cb_hp = ttk.Combobox(input_frame, font = ("Times New Roman", 12), width = 25,
                         values = ["HP001 - Toán cao cấp", "HP002 - Lập trình Python", "HP003 - Cơ sở dữ liệu"])
    cb_hp.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "w") 

    # ======= Nút chức năng =======
    btn_frame = tk.Frame(frame_right, bg = "white", bd = 2)
    btn_frame.pack(pady = 5)
    btn_themsv = ttk.Button(btn_frame, text = "Thêm điểm", width = 20, command = lambda: messagebox.showinfo("Thông báo", "Chức năng đang phát triển"))
    btn_themsv.grid(row = 0, column = 0, padx = 5)
    btn_thoat = ttk.Button(btn_frame, text = "Xóa", width = 20, command = lambda: messagebox.showinfo("Thông báo", "Chức năng đang phát triển"))
    btn_thoat.grid(row = 0, column = 1, padx = 5)


    # ======= Bảng hiển thị dữ liệu =======
    table_frame = tk.Frame(frame_right, bg = "white", bd = 2, relief = "groove")
    table_frame.pack(padx=5, pady = 5, fill = "both", expand = True)
    # =========Cho phép cuộn ==========
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    collumns = ("STT", "Mã SV", "Họ tên", "Điểm chuyên cần", "Điểm giữa kỳ", "Điểm cuối kỳ", "Điểm tổng kết")
    tree = ttk.Treeview(table_frame, columns = collumns, show = "headings")
    v_scroll = ttk.Scrollbar(table_frame, orient = "vertical", command = tree.yview)
    h_scroll = ttk.Scrollbar(table_frame, orient = "horizontal", command = tree.xview)

    tree.configure(yscrollcommand = v_scroll.set, xscrollcommand = h_scroll.set)
    tree.grid(row = 0, column = 0, sticky = "nsew")
    v_scroll.grid(row = 0, column = 1, sticky = "ns")
    h_scroll.grid(row = 1, column = 0, sticky = "ew")

    # ======= Định dạng cột =======
    tree.heading ("STT", text = "STT")
    tree.column ("STT", width = 50, anchor = "center")

    tree.heading ("Mã SV", text = "Mã SV")
    tree.column ("Mã SV", width = 100, anchor = "center")

    tree.heading ("Họ tên", text = "Họ tên")
    tree.column ("Họ tên", width = 200, anchor = "w")

    tree.heading ("Điểm chuyên cần", text = "Điểm chuyên cần")
    tree.column ("Điểm chuyên cần", width = 120, anchor = "center")

    tree.heading ("Điểm giữa kỳ", text = "Điểm giữa kỳ")
    tree.column ("Điểm giữa kỳ", width = 100, anchor = "center")

    tree.heading ("Điểm cuối kỳ", text = "Điểm cuối kỳ")
    tree.column ("Điểm cuối kỳ", width = 100, anchor = "center")
    
    tree.heading ("Điểm tổng kết", text = "Điểm tổng kết")
    tree.column ("Điểm tổng kết", width = 100, anchor = "center")



    