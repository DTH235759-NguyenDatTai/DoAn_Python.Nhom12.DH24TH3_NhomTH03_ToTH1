import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Chương Trình Quản Lý Điểm Sinh Viên")
root.geometry("900x500")
root.configure(bg="#f4f6f9")

# ============= KHUNG TRÁI =============
frame_left = tk.Frame(root, bg="white", bd=1, relief="solid")
frame_left.place(x=30, y=40, width=250, height=400)

# Tiêu đề thông tin người dùng
lbl_info = tk.Label(frame_left, text="Thông tin người dùng", bg="white", font=("Arial", 11, "bold"))
lbl_info.pack(pady=(10, 5))

# Dòng chào
lbl_hello = tk.Label(frame_left, text="Xin Chào", bg="white", fg="black", font=("Times New Roman", 14))
lbl_hello.pack(pady=2)

lbl_role = tk.Label(frame_left, text="Admin", bg="white", fg="#0078D7", cursor="hand2", font=("Arial", 12, "underline"))
lbl_role.pack(pady=2)

lbl_name = tk.Label(frame_left, text="NGUYEN DAT TAI", bg="white", fg="#003366", font=("Arial", 11, "bold"))
lbl_name.pack(pady=5)

# Dòng phân cách
ttk.Separator(frame_left, orient="horizontal").pack(fill="x", padx=10, pady=10)

# Chức năng - quyền hạn
lbl_function = tk.Label(frame_left, text="Chức năng - Quyền hạn", bg="white", font=("Arial", 11, "bold"))
lbl_function.pack(pady=(0, 10))

# Nút bấm
style = ttk.Style()
style.configure("TButton", font=("Arial", 11, "bold"), padding=6)
style.map("TButton", background=[("active", "#cce6ff")])

btn_add_sv = ttk.Button(frame_left, text="Thêm Sinh Viên")
btn_add_sv.pack(pady=5, ipadx=10)

btn_add_mh = ttk.Button(frame_left, text="Thêm Môn Học")
btn_add_mh.pack(pady=5, ipadx=10)

btn_view = ttk.Button(frame_left, text="Xem")
btn_view.pack(pady=5, ipadx=10)

# ============= KHUNG PHẢI (ẢNH) =============
frame_right = tk.Frame(root, bg="white", bd=1, relief="solid")
frame_right.place(x=310, y=40, width=550, height=400)

# Tiêu đề
lbl_title = tk.Label(frame_right, text="PHẦN MỀM QUẢN LÍ ĐIỂM SINH VIÊN KHOA CNTT - TRƯỜNG ĐH AN GIANG",
                     bg="white", fg="black", font=("Arial", 11, "bold"))
lbl_title.pack(pady=(10, 10))

# Ảnh (đặt ảnh trong cùng thư mục)
try:
    image = Image.open("mainform.jpg")  # ảnh bạn gửi
    image = image.resize((520, 300))
    img = ImageTk.PhotoImage(image)
    lbl_image = tk.Label(frame_right, image=img, bg="white")
    lbl_image.image = img
    lbl_image.pack(pady=5)
except Exception as e:
    lbl_error = tk.Label(frame_right, text="Không tìm thấy ảnh mainform.jpg", fg="red", bg="white")
    lbl_error.pack(pady=10)

# ============= CHẠY APP =============
root.mainloop()