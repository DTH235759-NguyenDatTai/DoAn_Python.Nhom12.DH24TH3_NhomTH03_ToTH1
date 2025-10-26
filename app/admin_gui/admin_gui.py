from admin_gui.them_mh import add_mh
from admin_gui.Xem_mh import xem_mh

def create_admin_button(frame_right, username):
    def monHoc():
        add_mh(frame_right)

    def Xem():
        xem_mh(frame_right)
    
    def exit_app():
        frame_right.winfo_toplevel().destroy()
    buttons = [
        ("Thêm môn học", monHoc),
        
        ("Xem", Xem),
        ("Thoát", exit_app)
        
        ]
    return buttons


