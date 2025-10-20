from tkinter import messagebox
from sinhvien_gui.show_sv_info import show_info
from sinhvien_gui.show_diem_sv import show_diem

def create_sv_gui(frame_right, username):
    def info_sv():
        show_info(frame_right, username)

    def diem_sv():
        show_diem(frame_right, username)

    def exit_app():
        frame_right.winfo_toplevel().destroy()

    buttons = [
        ("Xem thông tin", info_sv),
        ("Xem điểm", diem_sv),
        ("Xem điểm tổng kết", lambda: messagebox.showinfo("Thông báo", "Chức năng đang phát triển")),
        ("Thoát", exit_app)
    ]
    return buttons
