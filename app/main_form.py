import tkinter as tk
from tkinter import ttk, font, messagebox
from PIL import Image, ImageTk
from admin_gui import admin_gui
from sinhvien_gui import sinhVien_gui
from giangvien_gui import giangVien_gui
import login_gui

# ========= Hàm căn giữa cửa sổ ============
def center_window(win, w, h):
    """Căn giữa cửa sổ Tkinter"""
    win.update_idletasks()
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ====== HÀM TẠO MAIN FORM ======
def create_mainForm(username=None, role=None):
    mainform = tk.Tk()
    mainform.title("Chương Trình Quản Lý Điểm Sinh Viên")
    center_window(mainform, 1350, 650)
    mainform.configure(bg="#f4f6f9")

    # ====== ĐỊNH NGHĨA FONT ======
    label_font = font.Font(family="Times New Roman", size=12, weight="bold")
    hello_font = font.Font(family="Times New Roman", size=14)
    role_font = font.Font(family="Times New Roman", size=12, underline=1)
    name_font = font.Font(family="Times New Roman", size=12, weight="bold")

    # ====== KHUNG TRÁI - PHẢI ======
    frame_left = tk.Frame(mainform, bg="white", bd=1, relief="solid")
    frame_left.place(x=30, y=30, width=320, height=600)

    frame_right = tk.Frame(mainform, bg="white", bd=1, relief="solid")
    frame_right.place(x=370, y=30, width=950, height=600)

    # ==============================
    # ====== HÀM CON ==============
    # ==============================
    def create_frame_right():
        # ===================== KHUNG PHẢI ======================
        lbl_title = tk.Label(
            frame_right,
            text="PHẦN MỀM QUẢN LÍ ĐIỂM SINH VIÊN\nKHOA CNTT - TRƯỜNG ĐẠI HỌC AN GIANG",
            bg="white",
            fg="red",
            font=("Times New Roman", 16, "bold"),
            justify="center"
        )
        lbl_title.pack(pady=(10, 10))

    def create_frame_left():
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

        btn_frame = tk.Frame(frame_left, bg="white")
        btn_frame.pack(pady=20)

        # ======= Tạo nút chức năng tùy quyền =======
        if role == "admin":
            buttons = admin_gui.create_admin_button(frame_right, username)
        elif role == "giangvien":
            buttons = giangVien_gui.create_gv_form(frame_right, username)
        elif role == "sinhvien":
            buttons = sinhVien_gui.create_sv_gui(frame_right, username)
        else:
            buttons = []

        for text, command in buttons:
            btn = ttk.Button(btn_frame, text=text, width=25, command=command)
            btn.pack(pady=10)

    def anhnen():
        # Ảnh minh họa
        try:
            image = Image.open("images/anhnen.jpg").resize((900, 550))
            img = ImageTk.PhotoImage(image)
            lbl_image = tk.Label(frame_right, image=img, bg="white")
            lbl_image.image = img
            lbl_image.pack(pady=5)
        except Exception:
            lbl_error = tk.Label(frame_right, text="Không tìm thấy ảnh", fg="red", bg="white", font=label_font)
            lbl_error.pack(pady=10)

    # ==============================
    # ====== GIAO DIỆN CHÍNH ======
    # ==============================
    if username is None:
        def open_login():
            mainform.withdraw()
            login_gui.create_login_form(mainform)

        btn_frame = tk.Frame(frame_left, bg="white")
        btn_frame.pack(pady=20)

        tk.Label(btn_frame, text="Xin mời đăng nhập", bg="white", font=label_font).pack(pady=10)
        btn_login = tk.Button(btn_frame, text="Đăng nhập", width=20, command=open_login)
        btn_login.pack(pady=10)
        btn_exit = tk.Button(btn_frame, text="Thoát", width=20, command=mainform.destroy)
        btn_exit.pack(pady=10)
        anhnen()
    else:
        # Khi đăng nhập rồi thì clear 2 frame trước khi dựng lại
        for widget in frame_left.winfo_children():
            widget.destroy()
        for widget in frame_right.winfo_children():
            widget.destroy()

        create_frame_left()
        create_frame_right()
        anhnen()

    mainform.mainloop()


# ===== Khi chạy file này trực tiếp =====
if __name__ == "__main__":
    create_mainForm()