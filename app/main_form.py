import tkinter as tk
from tkinter import ttk, font
from tkinter import messagebox
from PIL import Image, ImageTk
from admin_gui import admin_gui
from sinhvien_gui import sinhVien_gui


def create_adminForm(username, role):
    # ====== CỬA SỔ CHÍNH ======
    adminform = tk.Tk()
    adminform.title("Chương Trình Quản Lý Điểm Sinh Viên")
    adminform.geometry("1000x550")
    adminform.configure(bg="#f4f6f9")

    # ====== ĐỊNH NGHĨA FONT ======
    label_font = font.Font(family="Times New Roman", size=12, weight="bold")
    # button_font = font.Font(family="Times New Roman", size=12, weight="bold")

    # Font riêng cho từng thành phần thông tin người dùng
    hello_font = font.Font(family="Times New Roman", size=14)
    role_font = font.Font(family="Times New Roman", size=12, underline=1)
    name_font = font.Font(family="Times New Roman", size=12, weight="bold")

    # ====== KHUNG TRÁI ======
    frame_left = tk.Frame(adminform, bg="white", bd=1, relief="solid")
    frame_left.place(x=30, y=30, width=300, height=500)

    lbl_info = tk.Label(frame_left, text="Thông tin người dùng", bg="white", font=label_font)
    lbl_info.pack(pady=(15, 10))

    lbl_hello = tk.Label(frame_left, text="Xin Chào", bg="white", fg="black", font=hello_font)
    lbl_hello.pack(pady=2)

    lbl_role = tk.Label(frame_left, text=role, bg="white", fg="#0078D7", font=role_font)
    lbl_role.pack(pady=2)

    lbl_name = tk.Label(frame_left, text=username.upper(), bg="white", fg="#003366", font=name_font)
    lbl_name.pack(pady=5)

    ttk.Separator(frame_left, orient="horizontal").pack(fill="x", padx=30, pady=15)

    lbl_function = tk.Label(frame_left, text="Chức năng - Quyền hạn", bg="white", font=label_font)
    lbl_function.pack(pady=(0, 15))
    
    # ====== KHUNG PHẢI (ẢNH) ======
    frame_right = tk.Frame(adminform, bg="white", bd=1, relief="solid")
    frame_right.place(x=330, y=30, width=645, height=500)

    # Tiêu đề (đưa khoa và trường xuống dòng)
    lbl_title = tk.Label(
        frame_right,
        text="PHẦN MỀM QUẢN LÍ ĐIỂM SINH VIÊN\nKHOA CNTT - TRƯỜNG ĐẠI HỌC AN GIANG",
        bg="white",
        fg="red",
        font=("Times New Roman", 16, "bold"),
        justify="center"
    )
    lbl_title.pack(pady=(10, 10))

    # Ảnh (đặt ảnh trong cùng thư mục)
    try:
        image = Image.open("images/agu.jpg")
        image = image.resize((620, 450))
        img = ImageTk.PhotoImage(image)
        lbl_image = tk.Label(frame_right, image=img, bg="white")
        lbl_image.image = img
        lbl_image.pack(pady=5)
    except Exception as e:
        lbl_error = tk.Label(frame_right, text="Không tìm thấy ảnh", fg="red", bg="white", font=label_font)
        lbl_error.pack(pady=10)


    # ==========================================================================================================
    # =========================================== Các phím chức năng ===========================================
    # ==========================================================================================================

    # Lable chứa các nút
    btn_frame = tk.Label(frame_left, bg="white")
    btn_frame.pack(pady=20)

    # Danh sách nút và nhãn hiển thị
    if role == "admin":
        buttons = admin_gui.create_admin_button()
    elif role == "sinhvien":
        buttons = sinhVien_gui.create_sv_gui(frame_right, username)
    else:
        messagebox.showerror("Thông báo", "button lỗi")

    # ======= Tạo và thêm các nút vào khung =======
    for text, command in buttons:
        btn = ttk.Button(btn_frame, text=text, width=20, command=command)
        btn.pack(pady=8)
