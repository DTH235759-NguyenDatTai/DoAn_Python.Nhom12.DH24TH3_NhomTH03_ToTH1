import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db_connect import get_db_connect

def show(frame_right, username):
    # Xóa nội dung cũ
    for widget in frame_right.winfo_children():
        widget.destroy()

    # ====== Tiêu đề ======
    lbl_title = tk.Label(
        frame_right,
        text="THÔNG TIN SINH VIÊN",
        font=("Times New Roman", 16, "bold"),
        fg="darkred",
        bg="white"
    )
    lbl_title.pack(pady=10)

    # ====== Khung màu xanh (viền bao) ======
    outer_frame = tk.Frame(frame_right, bg="#cce6ff", bd=3, relief="ridge")
    outer_frame.pack(padx=15, pady=15, fill="both", expand=True)

    # ====== Nền trắng bên trong (chứa nội dung) ======
    inner_frame = tk.Frame(outer_frame, bg="white")
    inner_frame.pack(padx=15, pady=15, fill="both", expand=True)

    # =====Kết nối tới sql=====
    conn = get_db_connect()
    if conn == None:
        return
    # Tạo đối tượng để gửi lệnh đến cơ sở sữ liệu
    cursor = conn.cursor()

    # Truy vấn kiểm tra tài khoản
    sql = "SELECT MSSV, HoTen, NgaySinh, GioiTinh, Lop, Khoa FROM SinhVien WHERE MSSV = ?"
    cursor.execute(sql, (username,))   #Thực thi lệnh sql
    sv_row = cursor.fetchone()     #trả về kết quả của Role
    if not sv_row:
        messagebox.showwarning("Không tìm thấy", "Không tìm thấy thông tin sinh viên.")
        return
    # sv_row là tuple => truy xuất theo index
    mssv, hoten, ngaysinh, gioitinh, lop, khoa = sv_row
    # Tạo danh sách nhãn
    labels = [
        ("Mã sinh viên", mssv),
        ("Tên sinh viên", hoten),
        ("Ngày sinh", ngaysinh),
        ("Giới tính", gioitinh),
        ("Lớp", lop),
        ("Khoa", khoa)
    ]

    # Hiển thị từng dòng trong khung
    for i, (field, value) in enumerate(labels):
        tk.Label(inner_frame, text=f"{field}:", bg="white",
                 anchor="w", font=("Times New Roman", 11, "bold")).grid(row=i, column=0, sticky="w", padx=20, pady=5)
        tk.Label(inner_frame, text=value, bg="white",
                 anchor="w", font=("Times New Roman", 11)).grid(row=i, column=1, sticky="w", padx=10, pady=5)