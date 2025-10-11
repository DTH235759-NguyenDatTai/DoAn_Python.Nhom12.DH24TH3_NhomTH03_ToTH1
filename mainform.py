import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk

# ====== CỬA SỔ CHÍNH ======
root = tk.Tk()
root.title("Chương Trình Quản Lý Điểm Sinh Viên")
root.geometry("900x500")
root.configure(bg="#f4f6f9")

# ====== ĐỊNH NGHĨA FONT ======
label_font = font.Font(family="Times New Roman", size=12, weight="bold")
button_font = font.Font(family="Times New Roman", size=12, weight="bold")

# Font riêng cho từng thành phần thông tin người dùng
hello_font = font.Font(family="Times New Roman", size=14)
role_font = font.Font(family="Times New Roman", size=12, underline=1)
name_font = font.Font(family="Times New Roman", size=12, weight="bold")

# ====== KHUNG TRÁI ======
frame_left = tk.Frame(root, bg="white", bd=1, relief="solid")
frame_left.place(x=30, y=40, width=250, height=400)

# Tiêu đề thông tin người dùng
lbl_info = tk.Label(frame_left, text="Thông tin người dùng", bg="white", font=label_font)
lbl_info.pack(pady=(10, 5))

# Dòng chào
lbl_hello = tk.Label(frame_left, text="Xin Chào", bg="white", fg="black", font=hello_font)
lbl_hello.pack(pady=2)

# Vai trò người dùng
lbl_role = tk.Label(frame_left, text="Admin", bg="white", fg="#0078D7", cursor="hand2", font=role_font)
lbl_role.pack(pady=2)

# Tên người dùng
lbl_name = tk.Label(frame_left, text="NGUYEN DAT TAI", bg="white", fg="#003366", font=name_font)
lbl_name.pack(pady=5)

# Dòng phân cách
ttk.Separator(frame_left, orient="horizontal").pack(fill="x", padx=10, pady=10)

# Chức năng - quyền hạn
lbl_function = tk.Label(frame_left, text="Chức năng - Quyền hạn", bg="white", font=label_font)
lbl_function.pack(pady=(0, 10))

# ====== NÚT BẤM ======
style = ttk.Style()
style.configure("TButton", font=button_font, padding=6)
style.map("TButton", background=[("active", "#cce6ff")])

btn_add_sv = ttk.Button(frame_left, text="Thêm Sinh Viên")
btn_add_sv.pack(pady=5, ipadx=10)

btn_add_mh = ttk.Button(frame_left, text="Thêm Môn Học")
btn_add_mh.pack(pady=5, ipadx=10)

btn_view = ttk.Button(frame_left, text="Xem")
btn_view.pack(pady=5, ipadx=10)

# ====== KHUNG PHẢI (ẢNH) ======
frame_right = tk.Frame(root, bg="white", bd=1, relief="solid")
frame_right.place(x=310, y=40, width=550, height=400)

# Tiêu đề (đưa khoa và trường xuống dòng)
lbl_title = tk.Label(
    frame_right,
    text="PHẦN MỀM QUẢN LÍ ĐIỂM SINH VIÊN\nKHOA CNTT - TRƯỜNG ĐẠI HỌC AN GIANG",
    bg="white",
    fg="black",
    font=("Times New Roman", 12, "bold"),
    justify="center"
)
lbl_title.pack(pady=(10, 10))

# Ảnh (đặt ảnh trong cùng thư mục)
try:
    image = Image.open("mainform.jpg")
    image = image.resize((520, 300))
    img = ImageTk.PhotoImage(image)
    lbl_image = tk.Label(frame_right, image=img, bg="white")
    lbl_image.image = img
    lbl_image.pack(pady=5)
except Exception as e:
    lbl_error = tk.Label(frame_right, text="Không tìm thấy ảnh mainform.jpg", fg="red", bg="white", font=label_font)
    lbl_error.pack(pady=10)

# ====== CHẠY APP ======
root.mainloop()