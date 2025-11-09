import hashlib
import tkinter as tk
from tkinter import font, messagebox
import db_connect

global username
global password

def create_login_form(parent_window):
    # =====Hàm đăng nhập=====
    def on_login():
        username = entry_user.get().strip()
        password = entry_pass.get().strip()

        if username == "" or password == "":
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return

        conn = db_connect.get_db_connect()
        if conn is None:
            return
        cursor = conn.cursor()

        sql = "SELECT Role FROM TaiKhoan WHERE TenDangNhap=? AND MatKhauHash=?"
        hashpwd = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute(sql, (username.upper(), hashpwd))
        row = cursor.fetchone()

        if row:
            role = row[0]
            messagebox.showinfo("Đăng nhập thành công")
            loginForm.destroy()
            if parent_window:
                parent_window.destroy()
            import main_form
            main_form.create_mainForm(username, role)
        else:
            messagebox.showerror("Thông báo", "Tên đăng nhập hoặc mật khẩu không đúng!")

    def on_forgot(event=None):
        messagebox.showinfo("Quên mật khẩu", "Hướng dẫn khôi phục mật khẩu (demo).")

    def on_hover_in(event):
        btn_login.config(bg="#e8faff", relief="solid", bd=2)

    def on_hover_out(event):
        btn_login.config(bg="white", relief="solid", bd=2)

    # ========= Hàm căn giữa cửa sổ ============
    def center_window(win, w, h):
        """Căn giữa cửa sổ Tkinter"""
        win.update_idletasks()
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f"{w}x{h}+{x}+{y}")

    # Cửa sổ chính                  
    loginForm = tk.Toplevel(parent_window)
    loginForm.title("Login")
    center_window(loginForm, 800, 500)
    loginForm.resizable(False, False)
    loginForm.configure(bg="#f9fbfc")  # nền sáng dịu

    # Fonts (chuyển toàn bộ sang Times New Roman)
    title_font = font.Font(family="Times New Roman", size=42, weight="bold")
    label_font = font.Font(family="Times New Roman", size=16)
    entry_font = font.Font(family="Times New Roman", size=15)
    button_font = font.Font(family="Times New Roman", size=18, weight="bold")

    # Canvas viền ngoài
    canvas = tk.Canvas(loginForm, width=740, height=400, bg="#156bb1", highlightthickness=0)
    canvas.place(x=30, y=60)

    def round_rect(c, x1, y1, x2, y2, radius=20, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return c.create_polygon(points, smooth=True, **kwargs)

    # Viền nhẹ kiểu web
    round_rect(canvas, 5, 5, 735, 395, radius=20, fill="#d0f0f8")
    round_rect(canvas, 25, 25, 715, 375, radius=15, fill="white")

    # Frame nội dung
    frame = tk.Frame(loginForm, bg="white", width=700, height=360)
    frame.place(x=50, y=80)
    
    # Tiêu đề
    lbl_title = tk.Label(frame, text="Login", bg="white", fg="#222", font=title_font)
    lbl_title.place(relx=0.5, y=25, anchor="n")

    # Label và ô nhập
    lbl_user = tk.Label(frame, text="Tên đăng nhập:", bg="white", font=label_font, fg="#333")
    lbl_user.place(x=80, y=120)

    entry_user = tk.Entry(frame, font=entry_font, bg="#f9fdff", fg="#000",
                        relief="solid", bd=2, highlightcolor="#a9dbe9", highlightthickness=1)
    entry_user.place(x=280, y=118, width=320, height=35)

    lbl_pass = tk.Label(frame, text="Mật khẩu:", bg="white", font=label_font, fg="#333")
    lbl_pass.place(x=80, y=180)

    entry_pass = tk.Entry(frame, font=entry_font, bg="#f9fdff", fg="#000",
                        relief="solid", bd=2, highlightcolor="#a9dbe9", highlightthickness=1, show="*")
    entry_pass.place(x=280, y=178, width=320, height=35)

    # Quên mật khẩu
    lbl_forgot = tk.Label(frame, text="Quên mật khẩu?", fg="#007acc",
                        bg="white", cursor="hand2", font=("Times New Roman", 13, "underline"))
    lbl_forgot.place(relx=0.5, y=240, anchor="n")
    lbl_forgot.bind("<Button-1>", on_forgot)

    # Nút đăng nhập
    btn_login = tk.Button(frame, text="Đăng nhập", font=button_font,
                        bg="white", relief="solid", bd=2, cursor="hand2",
                        activebackground="#e8faff", command=on_login)
    btn_login.place(relx=0.5, y=290, anchor="n", width=180, height=50)

    btn_login.bind("<Enter>", on_hover_in)
    btn_login.bind("<Leave>", on_hover_out)

    entry_user.focus_set()