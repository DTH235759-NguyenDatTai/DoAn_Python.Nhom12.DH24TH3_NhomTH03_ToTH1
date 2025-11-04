from tkinter import messagebox
from .xem_Thongtin import xem_thongtin


def create_gv_form(frame_right, username):
    def exit_app():
        frame_right.winfo_toplevel().destroy()
    
    def them_thongtin():
        xem_thongtin(frame_right, username)

    buttons = [
        ("Xem thông tin\nNhập điểm", them_thongtin),
        ("Thoát", exit_app)
    ]
    return buttons 