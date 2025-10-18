from tkinter import messagebox
from sinhvien_gui.show_sv_info import show  

def create_sv_gui(frame_right, username):
    def info_sv():
        show(frame_right, username)

    def exit_app():
        frame_right.winfo_toplevel().destroy()

    buttons = [
        ("Xem thông tin", info_sv),
        ("Xem điểm", lambda: messagebox.showinfo("Thông báo", "Chức năng đang phát triển")),
        ("Xem điểm tổng kết", lambda: messagebox.showinfo("Thông báo", "Chức năng đang phát triển")),
        ("Thoát", exit_app)
    ]
    return buttons
