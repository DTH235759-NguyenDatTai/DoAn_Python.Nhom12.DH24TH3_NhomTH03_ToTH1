from admin_gui.them_mh import add_mh
from admin_gui.them_sv import add_sv
from admin_gui.them_diem import add_diem

def create_admin_button(frame_right, username):
    def monHoc():
        add_mh(frame_right)

    def sv():
        add_sv(frame_right)

    def Diem():
        add_diem(frame_right)
    
    def exit_app():
        frame_right.winfo_toplevel().destroy()
    buttons = [
        ("Thêm môn học", monHoc),
        ("Ghi danh học phần", sv),
        ("Nhập điểm", Diem),
        ("Thoát", exit_app)
        
        ]
    return buttons


