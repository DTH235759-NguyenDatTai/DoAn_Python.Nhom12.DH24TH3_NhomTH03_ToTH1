import tkinter as tk
from tkinter import ttk, messagebox

def xem_Thongtin(frame_right):
    # ===== Xóa nội dung cũ =====
    for widget in frame_right.winfo_children():
        widget.destroy()

    # ======= Tiêu đề =======
    lbl_title = tk.Label(
        frame_right, text="XEM THÔNG TIN SINH VIÊN", font=("Times New Roman", 16, "bold"),
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
    btn_xemtt = ttk.Button(btn_frame, text = "Xem thông tin", width = 20, command = lambda: messagebox.showinfo("Thông báo", "Chức năng đang phát triển"))
    btn_xemtt.grid(row = 0, column = 0, padx = 5)
    btn_thoat = ttk.Button(btn_frame, text = "Thoát", width = 20, command = lambda: messagebox.showinfo("Thông báo", "Chức năng đang phát triển"))
    btn_thoat.grid(row = 0, column = 1, padx = 5)
    
