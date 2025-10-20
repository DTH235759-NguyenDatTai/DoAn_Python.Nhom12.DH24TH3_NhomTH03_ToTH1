import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import get_db_connect
from PIL import Image, ImageTk
import os

def show_diem(frame_right, username):

        # ====== Kết nối SQL ======
    conn = get_db_connect()
    if not conn:
        messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu.")
        return

    cursor = conn.cursor()
    try:
        sql = """
            SELECT (MSSV, MaMH, TenMH, TinChi, PhanTram_KT, PhanTram_Thi, DiemQuaTrinh, DiemThi, DiemTongKet, HocKy, NamHoc) FROM Diem
            WHERE MSSV=?
        """
        cursor.execute(sql, username)
        rows = cursor.fetchone()

        for row in rows:
            table.insert("", "end", values=(
                row.MaMH, row.TenMH, row.SoTC,
                row.PhanTramKT, row.PhanTramThi,
                row.DiemQT, row.DiemThi, row.DiemTongKet
            ))

    except Exception as e:
        messagebox.showerror("Lỗi truy vấn", str(e))
    finally:
        conn.close()


     # Xóa nội dung cũ
    for widget in frame_right.winfo_children():
        widget.destroy()

    # ====== Tiêu đề ======
    lbl_title = tk.Label(
        frame_right,
        text="BẢNG ĐIỂM SINH VIÊN",
        font=("Times New Roman", 16, "bold"),
        fg="darkred",
        bg="white"
    )
    lbl_title.pack(pady=5)

    # ====== Khung màu xanh (viền bao) ======
    outer_frame = tk.Frame(frame_right, bg="#cce6ff", bd=3, relief="ridge")
    outer_frame.pack(padx=15, pady=5, fill="both", expand=True)

    # ====== Nền trắng bên trong (chứa nội dung) ======
    inner_frame = tk.Frame(outer_frame, bg="white")
    inner_frame.pack(padx=15, pady=15, fill="both", expand=True)

    # ====== Học kỳ - năm học ======
    lbl_subtitle = tk.Label(
        inner_frame,
        text="Học kỳ 1 - Năm học 2024–2025",
        font=("Times New Roman", 13, "bold"),
        fg="#003366",
        bg="#cce6ff"
    )
    lbl_subtitle.pack(pady=(5, 10))

    # ====== Frame chứa bảng điểm + thanh cuộn ======
    table_frame = tk.Frame(inner_frame, bg="#cce6ff")
    table_frame.pack(padx=30, pady=10, fill="both", expand=True)

    # ====== Bảng điểm ======
    columns = ("MaMH", "TenMH", "SoTC", "PhanTramKT", "PhanTramThi", "DiemQT", "DiemThi", "DiemTongKet")
    table = ttk.Treeview(table_frame, columns=columns, show="headings", height=14)

    headers = ["Mã MH", "Tên môn học", "Số TC", "% KT", "% Thi", "Điểm QT", "Điểm Thi", "Tổng Kết"]
    widths = [90, 240, 60, 60, 60, 80, 80, 100]

    for col, text, w in zip(columns, headers, widths):
        table.heading(col, text=text)
        table.column(col, anchor="center", width=w)

    # ====== Thanh cuộn ======
    scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=table.xview)
    table.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # ====== Đặt vị trí ======
    table.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, columnspan=2, sticky="ew")

    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)


