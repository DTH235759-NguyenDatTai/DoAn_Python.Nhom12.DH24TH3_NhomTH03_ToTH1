from tkinter import messagebox
from .qlmh import qlMonHoc


def create_gv_form(frame_right, username):
    def exit_app():
        frame_right.winfo_toplevel().destroy()
    
    def Ql():
        qlMonHoc(frame_right, username)

    buttons = [
        ("Quản Lí Môn Học", Ql),
        ("Thoát", exit_app)
    ]
    return buttons 