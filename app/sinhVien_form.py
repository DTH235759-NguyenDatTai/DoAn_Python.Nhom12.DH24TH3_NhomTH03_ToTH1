import tkinter as tk
from tkinter import ttk, messagebox
import db_connect

def get_data(mssv):
    # =====Kết nối tới sql=====
    conn = db_connect.get_db_connect()
    if conn == None:
        return
    # Tạo đối tượng để gửi lệnh đến cơ sở sữ liệu
    cursor = conn.cursor()

    # Truy vấn kiểm tra tài khoản
    sql = "SELECT MSSV, HoTen, NgaySinh, GioiTinh, Lop, Khoa FROM SinhVien WHERE MSSV = ?"
    cursor.execute(sql, (mssv))   #Thực thi lệnh sql
    sv_row = cursor.fetchone()     #trả về kết quả của Role
    return sv_row

def create_svForm(mssv):
    sv_data = get_data(mssv)

    svform = tk.Tk()
    svform.title("THÔNG TIN ĐIỂM SINH VIÊN")
    svform.geometry("1150x750")
    svform.configure(bg="#e8f0fe")  # Nền tổng thể xanh nhạt

    # ====== Style (Màu & Font) ======
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#e8f0fe", font=("Times New Roman", 11))
    style.configure("TEntry", padding=3)
    style.configure("Treeview.Heading", font=("Times New Roman", 11, "bold"), background="#d0e1ff")
    style.configure("Treeview", background="white", fieldbackground="white", rowheight=25, font=("Times New Roman", 11))
    style.map("Treeview", background=[("selected", "#c1d4ff")])

    # ====== KHUNG THÔNG TIN SINH VIÊN ======
    frame_info = tk.LabelFrame(svform, text=" Thông tin sinh viên ", bg="#bbdefb", font=("Times New Roman", 13, "bold"), padx=10, pady=10)
    frame_info.pack(fill="x", padx=10, pady=10)

    labels = [
        "Mã sinh viên:", "Tên sinh viên:", "Ngày sinh" ,"Phái:",
        "Lớp:"
    ]
    ngay_sinh = sv_data.NgaySinh
    ngay_sinh.strftime('%d/%m/%Y')
    sv_info = [
        sv_data.MSSV, sv_data.HoTen, ngay_sinh.strftime('%d/%m/%Y'), sv_data.GioiTinh, sv_data.Lop
    ]

    entries = {}
    for i, text in enumerate(labels):
        tk.Label(frame_info, text=text, bg="#62A6C4", font=("Times New Roman", 11, "bold")).grid(row=i//3, column=(i%3)*2, sticky="w", padx=8, pady=5)
        entry = ttk.Entry(frame_info, width=40)
        entry.grid(row=i//3, column=(i%3)*2 + 1, padx=5, pady=5)
        entry.insert(0, sv_info[i])
        entries[text] = entry

    # ====== KHUNG BẢNG ĐIỂM ======
    frame_table = tk.LabelFrame(svform, text=" Bảng điểm học kỳ ", bg="#bbdefb", font=("Times New Roman", 13, "bold"), padx=10, pady=10)
    frame_table.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("STT", "Mã Môn", "Tên Môn", "TC", "% KT", "% Thi",
            "Điểm Chuyên Cần", "Điểm Quá Trình", "Thi L1",
            "Thi L2", "Thi L3", "TK(10)", "TK(CH)")
    
    table = ttk.Treeview(frame_table, columns=columns, show="headings", height=8)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=85, anchor="center")

    # Thanh cuộn dọc
    scroll_y = ttk.Scrollbar(frame_table, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    table.pack(fill="both", expand=True)

    # ====== KHUNG TỔNG KẾT ======
    frame_summary = tk.LabelFrame(svform, text=" Tổng kết học kỳ ", bg="#bbdefb", font=("Times New Roman", 12, "bold"), padx=5, pady=5)
    frame_summary.pack(fill="x", padx=8, pady=6)

    summary_data = [
        "Điểm trung bình học kỳ hệ 10/100:",
        "Điểm trung bình học kỳ hệ 4:",
        "Điểm trung bình tích lũy (hệ 10):",
        "Điểm trung bình tích lũy (hệ 4):",
        "Số tín chỉ đạt:",
        "Số tín chỉ tích lũy:",
        "Phân loại điểm trung bình HK:"
    ]

    summary_entries = {}
    for i, label in enumerate(summary_data):
        tk.Label(frame_summary, text=label, bg="#bbdefb", font=("Times New Roman", 11, "bold")).grid(row=i, column=0, sticky="w", padx=5, pady=3)
        entry = ttk.Entry(frame_summary, width=25)
        entry.grid(row=i, column=1, sticky="w", padx=5, pady=2)
        entry.insert(0, "(nhập giá trị)")
        summary_entries[label] = entry

