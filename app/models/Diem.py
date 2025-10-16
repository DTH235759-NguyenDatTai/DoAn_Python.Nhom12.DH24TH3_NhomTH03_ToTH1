from app.forms import db_connect

class Diem:
    def __init__(self, mssv, ma_mh, ten_mh = None, tin_chi = None, pt_kt = None, pt_thi = None, diem_qt = None, diem_thi = None, hoc_ky = None, nam_hoc = None):
        # Tạo thuộc tính dữ liệu
        self.mssv = mssv
        self.ma_mh = ma_mh
        self.ten_mh = ten_mh
        self.tin_chi = tin_chi
        self.pt_kt = pt_kt
        self.pt_thi = pt_thi
        self.diem_qt = diem_qt
        self.diem_thi = diem_thi
        self.hoc_ky = hoc_ky
        self.nam_hoc = nam_hoc
        self.diem_tk = self.tinh_diem_tk()

    # Phương thức tính điểm tổng kết
    def tinh_diem_tk(self):
        if self.pt_kt is not None and self.diem_qt is not None and self.pt_thi is not None and self.diem_thi is not None:
            return (self.pt_kt * self.diem_qt) + (self.pt_thi * self.diem_thi)
    
    # Lưu vào db
    def luu_db(self):
        conn = db_connect.get_db_connect()
        sql = """
            INSERT INTO Diem (MSSV, MaMH, TenMH, TinChi, PhanTram_KT, PhanTram_Thi, DiemQuaTrinh, DiemThi, DiemTongKet, HocKy, NamHoc)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        conn.cursor().execute(sql, self.mssv, self.ma_mh, self.ten_mh, self.tin_chi, self.pt_kt, self.pt_thi, self.diem_qt,
                               self.diem_thi,self.diem_tk, self.hoc_ky, self.nam_hoc)
        conn.commit() # Lưu vĩnh viễn
    