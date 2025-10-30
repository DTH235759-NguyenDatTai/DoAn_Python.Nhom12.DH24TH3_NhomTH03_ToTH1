from tkinter import messagebox
from .them_Diem import add_diem
from .xem_Thongtin import xem_ttin


def create_gv_form(frame_right):
    def exit_app():
        frame_right.winfo_toplevel().destroy()

    def them_diem():
        add_diem(frame_right)

    def them_thongtin():
        xem_ttin(frame_right)

    buttons = [
        ("Thêm điểm", them_diem),
        ("Xem thông tin", them_thongtin),
        ("Thoát", exit_app)
    ]
    return buttons 