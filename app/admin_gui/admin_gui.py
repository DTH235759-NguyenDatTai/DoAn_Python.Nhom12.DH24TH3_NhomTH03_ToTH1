from tkinter import messagebox
from admin_gui.them_mh import add_mh

def create_admin_button(frame_right, username):
    def monHoc():
        add_mh(frame_right, username)
    
    def exit_app():
        frame_right.winfo_toplevel().destroy()
    buttons = [
        ("Thêm Môn Học", monHoc),
        ("Thêm Học phần", lambda: messagebox.showinfo("Thông báo", "Chức năng đang phát triển")),
        ("Xem", lambda: messagebox.showinfo("Thông báo", "Chức năng đang phát triển")),
        ("Thoát", exit_app)
        ]
    return buttons