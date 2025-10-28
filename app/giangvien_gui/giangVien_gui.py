from tkinter import messagebox

def create_gv_form(frame_right):
    def exit_app():
        frame_right.winfo_toplevel().destroy()

    buttons = [
        ("Xem điểm", lambda: messagebox.showinfo("Thông báo", "Chức năng đang phát triển")),
        ("Thoát", exit_app)
    ]
    return buttons 