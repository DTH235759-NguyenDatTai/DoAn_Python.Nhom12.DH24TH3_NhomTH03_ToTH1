from admin_gui.them_mh import add_mh
from admin_gui.them_hp import add_hp
from admin_gui.them_sv import add_sv
from admin_gui.Xem_mh import xem_mh

def create_admin_button(frame_right, username):
    def monHoc():
        add_mh(frame_right)

    def hocPhan():
        add_hp(frame_right)

    def sv():
        add_sv(frame_right)

    def Xem():
        xem_mh(frame_right)
    
    def exit_app():
        frame_right.winfo_toplevel().destroy()
    buttons = [
        ("Thêm môn học", monHoc),
        ("Thêm học phần", hocPhan),
        ("Ghi danh học phần", sv),
        ("Xem", Xem),
        ("Thoát", exit_app)
        
        ]
    return buttons


