import tkinter as tk
from tkinter import ttk, font
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

# ====== CỬA SỔ CHÍNH ======
adminform = tk.Tk()
adminform.title("Chương Trình Quản Lý Điểm Sinh Viên")
adminform.geometry("1350x550")
adminform.configure(bg="#f4f6f9")

# ====== ĐỊNH NGHĨA FONT ======
label_font = font.Font(family="Times New Roman", size=12, weight="bold")
button_font = font.Font(family="Times New Roman", size=12, weight="bold")
hello_font = font.Font(family="Times New Roman", size=14)
role_font = font.Font(family="Times New Roman", size=12, underline=1)
name_font = font.Font(family="Times New Roman", size=12, weight="bold")
giangvien_font = font.Font(family="Times New Roman", size=12)

# ====== KHUNG TRÁI ======
frame_left = tk.Frame(adminform, bg="white", bd=1, relief="solid")
frame_left.place(x=30, y=40, width=250, height=450)

lbl_info = tk.Label(frame_left, text="Thông tin người dùng", bg="white", font=label_font)
lbl_info.pack(pady=(10, 5))

lbl_hello = tk.Label(frame_left, text="Xin Chào", bg="white", fg="black", font=hello_font)
lbl_hello.pack(pady=2)
lbl_role = tk.Label(frame_left, text="role", bg="white", fg="#0078D7", cursor="hand2", font=role_font)
lbl_role.pack(pady=2)
lbl_name = tk.Label(frame_left, text="role".upper(), bg="white", fg="#003366", font=name_font)
lbl_name.pack(pady=5)

ttk.Separator(frame_left, orient="horizontal").pack(fill="x", padx=10, pady=10)
lbl_function = tk.Label(frame_left, text="Chức năng - Quyền hạn", bg="white", font=label_font)
lbl_function.pack(pady=(0, 10))

style = ttk.Style()
style.configure("TButton", font=button_font, padding=6)
style.map("TButton", background=[("active", "#cce6ff")])

btn_add_sv = ttk.Button(frame_left, text="Thêm Sinh Viên")
btn_add_sv.pack(pady=5, padx=10, fill = "x")

btn_add_mh = ttk.Button(frame_left, text="Thêm Môn Học")
btn_add_mh.pack(pady=5, padx=10, fill = "x")

btn_add_gv = ttk.Button(frame_left, text="Thêm Giảng Viên")
btn_add_gv.pack(pady=5, padx=10, fill = "x")

btn_add_xemdiem = ttk.Button(frame_left, text="Xem Điểm Sinh Viên")
btn_add_xemdiem.pack(pady=5, padx=10, fill = "x")

btn_exit = ttk.Button(frame_left, text="Thoát", command=adminform.destroy)
btn_exit.pack(pady=5, padx=10, fill = "x")

# ====== KHUNG PHẢI (ẢNH) ======
frame_right = tk.Frame(adminform, bg="white", bd=1, relief="solid")
frame_right.place(x=310, y=40, width=1000, height=450)

lbl_title = tk.Label(
    frame_right,
    text="PHẦN MỀM QUẢN LÍ ĐIỂM SINH VIÊN\nKHOA CNTT - TRƯỜNG ĐẠI HỌC AN GIANG",
    bg="white", fg="black",
    font=("Times New Roman", 12, "bold"),
    justify="center"
)
lbl_title.pack(pady=(10, 10))

try:
    image = Image.open("image/h1.jpg")
    image = image.resize((520, 300))
    img = ImageTk.PhotoImage(image)
    lbl_image = tk.Label(frame_right, image=img, bg="white")
    lbl_image.image = img
    lbl_image.pack(pady=5)
except Exception as e:
    lbl_error = tk.Label(frame_right, text="Không tìm thấy ảnh", fg="red", bg="white", font=label_font)
    lbl_error.pack(pady=10)


# ====== HÀM MỞ FORM THÊM SINH VIÊN ======
def open_add_student_form():
    # Xóa toàn bộ nội dung cũ trong khung phải
    for widget in frame_right.winfo_children():
        widget.destroy()

    # ====== Tiêu đề ======
    title = tk.Label(frame_right, text="Quản lý sinh viên", font=("Times New Roman", 20, "bold"), fg="blue", bg="white")
    title.pack(pady=10)

    # ====== Frame thông tin chi tiết ======
    frame_info = tk.LabelFrame(frame_right, text="Thông tin chi tiết", font=label_font, bg="white", padx=10, pady=10)
    frame_info.pack(fill="x", padx=20, pady=5)


    tk.Label(frame_info, text="Giới tính:", bg="white", font=hello_font).grid(row=0, column=2, sticky="w", padx=10)
    gender_var = tk.StringVar(value="Nam")
    tk.Radiobutton(frame_info, text="Nam", variable=gender_var, value="Nam", bg="white").grid(row=0, column=3)
    tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ", bg="white").grid(row=0, column=4)

    tk.Label(frame_info, text="Ngày sinh:", bg="white", font=hello_font).grid(row=1, column=2, sticky="w", padx=10)
    entry_dob = ttk.Combobox(frame_info, values=["01/01/2000", "02/02/2001", "03/03/2002"], width =22)
    entry_dob.grid(row=1, column=3, columnspan=2, pady=5)

    tk.Label(frame_info, text="Khoa:", bg="white", font=hello_font).grid(row=2, column=2, sticky="w", padx=10)
    cb_khoa = ttk.Combobox(frame_info, values=["Công nghệ thông tin","Sư phạm","Nông nghiệp","Luật","Ngoại ngữ"], width=22)
    cb_khoa.grid(row=2, column=3, columnspan=2, pady=5)
    cb_khoa.current(0)

    # ====== Mã số sinh viên ======
    lbl_mssv = tk.Label(frame_info, text="Mã số sinh viên:", bg="white", font=hello_font, fg="#333")
    lbl_mssv.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    entry_mssv = tk.Entry(frame_info, font=hello_font, bg="#ffffff", fg="#000",
                      relief="solid", bd=1 )
    entry_mssv.grid(row=0, column=1, pady=2, ipady=0, ipadx=1)

    # ====== Họ tên ======
    lbl_name = tk.Label(frame_info, text="Họ tên:", bg="white", font=hello_font, fg="#333")
    lbl_name.grid(row=1, column=0, sticky="w", padx=10, pady=5) 

    entry_name = tk.Entry(frame_info, font=hello_font, bg="#ffffff", fg="#000",
                      relief="solid", bd=1)
    entry_name.grid(row=1, column=1, pady=2, ipady=0, ipadx=1)

    # ====== Lớp ======
    lbl_class = tk.Label(frame_info, text="Lớp:", bg="white", font=hello_font, fg="#333")
    lbl_class.grid(row=2, column=0, sticky="w", padx=10, pady=5)

    entry_class = tk.Entry(frame_info, font=hello_font, bg="#ffffff", fg="#000",
                       relief="solid", bd=1)
    entry_class.grid(row=2, column=1, pady=2, ipady=0, ipadx=1)

    # ====== Frame nút chức năng ======
    frame_buttons = tk.Frame(frame_right, bg="white")
    frame_buttons.pack(pady=10)

    btn_add = tk.Button(frame_buttons, text="Thêm", bg="#0078D7", fg="white", font=button_font, width=10)
    btn_add.grid(row=0, column=0, padx=10)

    btn_delete = tk.Button(frame_buttons, text="Xóa", bg="#0078D7", fg="white", font=button_font, width=10)
    btn_delete.grid(row=0, column=1, padx=10)

    btn_edit = tk.Button(frame_buttons, text="Sửa", bg="#0078D7", fg="white", font=button_font, width=10)
    btn_edit.grid(row=0, column=2, padx=10)

    # ====== Bảng danh sách ======
    frame_table = tk.LabelFrame(frame_right, text="Thông tin chung", font=label_font, bg="white", padx=10, pady=10)
    frame_table.pack(fill="both", expand=True, padx=20, pady=5)

    columns = ("mssv", "hoten", "ngaysinh", "gioitinh", "lop", "khoa")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=5)
    tree.pack(fill="both", expand=True)

    for col, text in zip(columns, ["MSSV", "Họ và tên", "Ngày sinh", "Giới tính", "Lớp", "Khoa"]):
        tree.heading(col, text=text)
        tree.column(col, width=100)

    # Dữ liệu mẫu
    sample_data = [
        ("SV001", "Nguyễn Văn An", "01/01/2000", "Nam", "DH20TH1", "CNTT"),
        ("SV002", "Trần Thị B", "02/02/2001", "Nữ", "DH20TH2", "CNTT"),
        ("DTH235758", "Nguyễn Võ Thanh Sơn", "08/01/2005", "Nam", "DH24TH3", "CNTT"),
    ]
    for row in sample_data:
        tree.insert("", "end", values=row)

    # ====== HÀM TÌM KIẾM SINH VIÊN ======
    def search_student():
        keyword = simpledialog.askstring("Tìm kiếm SV", "Nhập MSSV cần tìm:")
        if not keyword:
            return
        found = False
        for item in tree.get_children():
            values = tree.item(item, "values")
            if keyword.lower() in values[0].lower():
                tree.selection_set(item)
                tree.focus(item)
                found = True
                break
        if not found:
            messagebox.showinfo("Kết quả", f"Không tìm thấy sinh viên có MSSV: {keyword}")

    # ====== Nút tìm kiếm sinh viên ======
    btn_search = tk.Button(frame_buttons, text="Tìm kiếm SV", bg="#0078D7", fg="white", font=button_font, width=15, command=search_student)
    btn_search.grid(row=0, column=3, padx=10)
# ====== GÁN SỰ KIỆN CHO NÚT "THÊM SINH VIÊN" ======
btn_add_sv.config(command=open_add_student_form)

# ====== HÀM MỞ FORM THÊM MÔN HỌC  ======
def open_add_subject_form():
    for widget in frame_right.winfo_children():
        widget.destroy()

    title = tk.Label(frame_right, text="Quản lý môn học", font=("Times New Roman", 20, "bold"), fg="blue", bg="white")
    title.pack(pady=10)

    frame_info = tk.LabelFrame(frame_right, text="Thông tin chi tiết", font=label_font, bg="white", padx=10, pady=10)
    frame_info.pack(fill="x", padx=20, pady=5)

# --- CỘT BÊN TRÁI ---
    tk.Label(frame_info, text="Mã môn học:", bg="white", font=hello_font).grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entry_mamh = tk.Entry(frame_info, font=hello_font, relief="solid", bd=1, width=30)
    entry_mamh.grid(row=0, column=1, pady=5, ipady=2, padx=5)

    tk.Label(frame_info, text="Tên môn học:", bg="white", font=hello_font).grid(row=1, column=0, sticky="w", padx=5, pady=5)
    entry_tenmh = tk.Entry(frame_info, font=hello_font, relief="solid", bd=1, width=30)
    entry_tenmh.grid(row=1, column=1, pady=5, ipady=2, padx=5)

    # --- CỘT BÊN PHẢI ---
    tk.Label(frame_info, text="Số tín chỉ:", bg="white", font=hello_font).grid(row=0, column=2, sticky="w", padx=(50, 5), pady=5)
    entry_tinchi = tk.Entry(frame_info, font=hello_font, relief="solid", bd=1, width=30)
    entry_tinchi.grid(row=0, column=3, pady=5, ipady=2, padx=5)

    tk.Label(frame_info, text="Giảng viên phụ trách:", bg="white", font=hello_font).grid(row=1, column=2, sticky="w", padx=(50, 5), pady=5)
    cb_giangvien = ttk.Combobox(frame_info, values=["ThS. Trần Văn A", "TS. Nguyễn Thị B", "PGS.TS Lê Hoàng C"], width=31, font=giangvien_font)
    cb_giangvien.grid(row=1, column=3, pady=5, ipady=2, padx=5)

    frame_buttons = tk.Frame(frame_right, bg="white")
    frame_buttons.pack(pady=10)

    # ... (Các hàm xử lý logic thêm, xóa, sửa môn học ở đây)

    btn_add = tk.Button(frame_buttons, text="Thêm", bg="#0078D7", fg="white", font=button_font, width=10).grid(row=0, column=0, padx=10)
    btn_delete = tk.Button(frame_buttons, text="Xóa", bg="#0078D7", fg="white", font=button_font, width=10).grid(row=0, column=1, padx=10)
    btn_edit = tk.Button(frame_buttons, text="Sửa", bg="#0078D7", fg="white", font=button_font, width=10).grid(row=0, column=2, padx=10)

    frame_table = tk.LabelFrame(frame_right, text="Thông tin chung", font=label_font, bg="white", padx=10, pady=10)
    frame_table.pack(fill="both", expand=True, padx=20, pady=5)

    columns = ("mamh", "tenmh", "sotc")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=5)
    tree.pack(fill="both", expand=True)

    tree.heading("mamh", text="Mã Môn Học")
    tree.heading("tenmh", text="Tên Môn Học")
    tree.heading("sotc", text="Số tín chỉ")

    tree.column("mamh", width=150, anchor="center")
    tree.column("tenmh", width=300)
    tree.column("sotc", width=100, anchor="center")

    sample_data = [
        ("IT001", "Nhập môn Lập trình", "3"),
        ("IT002", "Kỹ thuật Lập trình", "3"),
        ("MA001", "Toán cao cấp A1", "4"),
        ("CE101", "Kiến trúc Máy tính", "4"),
    ]
    for row in sample_data:
        tree.insert("", "end", values=row)
# ====== HÀM TÌM KIẾM MÔN HỌC ======
    def search_subject():
        keyword = simpledialog.askstring("Tìm kiếm Môn học", "Nhập Mã Môn học cần tìm:")
        if not keyword: return
        for item in tree.get_children():
            values = tree.item(item, "values")
            if keyword.lower() in values[0].lower():
                tree.selection_set(item)
                tree.focus(item)
                return
        messagebox.showinfo("Kết quả", f"Không tìm thấy môn học có mã: {keyword}")

    btn_search = tk.Button(frame_buttons, text="Tìm kiếm MH", bg="#0078D7", fg="white", font=button_font, width=15, command=search_subject).grid(row=0, column=3, padx=10)

# ====== GÁN SỰ KIỆN CHO CÁC NÚT ======
btn_add_mh.config(command=open_add_subject_form)

# ====== HÀM MỞ FORM THÊM GIẢNG VIÊN  ======
def open_add_lecturer_form():
    for widget in frame_right.winfo_children():
        widget.destroy()
    
    title = tk.Label(frame_right, text="Quản lý Giảng viên", font=("Times New Roman", 20, "bold"), fg="#003366", bg="white")
    title.pack(pady=10)

    frame_info = tk.LabelFrame(frame_right, text="Thông tin chi tiết", font=label_font, bg="white", padx=10, pady=10)
    frame_info.pack(fill="x", padx=20, pady=5)

    # --- CỘT BÊN TRÁI ---
    tk.Label(frame_info, text="Mã Giảng viên:", bg="white", font=hello_font).grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entry_magv = tk.Entry(frame_info, font=hello_font, relief="solid", bd=1, width=25)
    entry_magv.grid(row=0, column=1, pady=5, ipady=2, padx=5)

    tk.Label(frame_info, text="Tên Giảng viên:", bg="white", font=hello_font).grid(row=1, column=0, sticky="w", padx=5, pady=5)
    entry_tengv = tk.Entry(frame_info, font=hello_font, relief="solid", bd=1, width=25)
    entry_tengv.grid(row=1, column=1, pady=5, ipady=2, padx=5)

    tk.Label(frame_info, text="Khoa:", bg="white", font=hello_font).grid(row=2, column=0, sticky="w", padx=5, pady=5)
    cb_khoa_gv = ttk.Combobox(frame_info, values=["Công nghệ thông tin", "Sư phạm", "Nông nghiệp", "Luật", "Ngoại ngữ"], width=26, font=("Times New Roman", 12))
    cb_khoa_gv.grid(row=2, column=1, pady=5, ipady=2, padx=5)
    cb_khoa_gv.current(0)
    
    # --- CỘT BÊN PHẢI (MỚI) ---
    tk.Label(frame_info, text="Số điện thoại:", bg="white", font=hello_font).grid(row=0, column=2, sticky="w", padx=(50, 5), pady=5)
    entry_sdt = tk.Entry(frame_info, font=hello_font, relief="solid", bd=1, width=25)
    entry_sdt.grid(row=0, column=3, pady=5, ipady=2, padx=5)

    tk.Label(frame_info, text="Email:", bg="white", font=hello_font).grid(row=1, column=2, sticky="w", padx=(50, 5), pady=5)
    entry_email = tk.Entry(frame_info, font=hello_font, relief="solid", bd=1, width=25)
    entry_email.grid(row=1, column=3, pady=5, ipady=2, padx=5)
    
    frame_buttons = tk.Frame(frame_right, bg="white")
    frame_buttons.pack(pady=15)

    btn_add = tk.Button(frame_buttons, text="Thêm", bg="#0078D7", fg="white", font=button_font, width=10).grid(row=0, column=0, padx=10)
    btn_delete = tk.Button(frame_buttons, text="Xóa", bg="#0078D7", fg="white", font=button_font, width=10).grid(row=0, column=1, padx=10)
    btn_edit = tk.Button(frame_buttons, text="Sửa", bg="#0078D7", fg="white", font=button_font, width=10).grid(row=0, column=2, padx=10)

    frame_table = tk.LabelFrame(frame_right, text="Thông tin chung", font=label_font, bg="white", padx=10, pady=10)
    frame_table.pack(fill="both", expand=True, padx=20, pady=5)

    columns = ("magv", "tengv", "khoa", "sdt", "email")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=5)
    tree.pack(fill="both", expand=True)

    tree.heading("magv", text="Mã GV")
    tree.heading("tengv", text="Tên Giảng viên")
    tree.heading("khoa", text="Khoa")
    tree.heading("sdt", text="Số điện thoại")
    tree.heading("email", text="Email")

    tree.column("magv", width=120, anchor="center")
    tree.column("tengv", width=200)
    tree.column("khoa", width=200, anchor="center")
    tree.column("sdt", width=150, anchor="center")
    tree.column("email", width=250)

    sample_data = [
        ("GV001", "ThS. Nguyễn Văn Thắng", "Công nghệ thông tin"),
        ("GV002", "TS. Lê Thị Huệ", "Sư phạm"),
        ("GV003", "PGS.TS. Phạm Văn Trung", "Nông nghiệp"),
    ]
    for row in sample_data:
        tree.insert("", "end", values=row)

    def search_lecturer():
        keyword = simpledialog.askstring("Tìm kiếm Giảng viên", "Nhập Mã Giảng viên cần tìm:")
        if not keyword: return
        for item in tree.get_children():
            values = tree.item(item, "values")
            if keyword.lower() in values[0].lower():
                tree.selection_set(item)
                tree.focus(item)
                return
        messagebox.showinfo("Kết quả", f"Không tìm thấy giảng viên có mã: {keyword}")

    btn_search = tk.Button(frame_buttons, text="Tìm kiếm GV", bg="#0078D7", fg="white", font=button_font, width=15, command=search_lecturer).grid(row=0, column=3, padx=10)

# ====== GÁN SỰ KIỆN CHO CÁC NÚT ======
btn_add_gv.config(command=open_add_lecturer_form)


# ====== HÀM MỞ FORM XEM ĐIỂM  ======
def open_view_scores_form():
    for widget in frame_right.winfo_children():
        widget.destroy()

    # ===== TIÊU ĐỀ =====
    title = tk.Label(
        frame_right,
        text="Tra Cứu Điểm Sinh Viên",
        font=("Times New Roman", 20, "bold"),
        fg="#003366",
        bg="white"
    )
    title.pack(pady=(15, 5))

    # ===== KHUNG TÌM KIẾM =====
    frame_search = tk.LabelFrame(
        frame_right,
        text="Thông tin tìm kiếm",
        font=("Times New Roman", 12, "bold"),
        bg="white",
        padx=20,
        pady=15,
        bd=2,            # viền đậm
        relief="groove"  # kiểu viền
    )
    frame_search.pack(fill="x", padx=20, pady=10)

    # --- Cột trái: Mã SV và Họ tên ---
    tk.Label(frame_search, text="Mã số sinh viên:", bg="white",
             font=("Times New Roman", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_masv = tk.Entry(frame_search, font=("Times New Roman", 12),
                          width=25, relief="solid", bd=1)
    entry_masv.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_search, text="Họ tên:", bg="white",
             font=("Times New Roman", 12, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_hoten = tk.Entry(frame_search, font=("Times New Roman", 12),
                           width=25, relief="solid", bd=1)
    entry_hoten.grid(row=1, column=1, padx=10, pady=5)

    # --- Cột phải: nút tìm kiếm nằm giữa 2 ô ---
    btn_search = tk.Button(frame_search,text="Tìm kiếm",font=("Times New Roman", 12, "bold"),bg="#007ACC", fg="white",padx=10, pady=5,relief="solid",bd = 2)
    btn_search.grid(row=0, column=2, rowspan=2, padx=20, pady=5, sticky="ns")  # canh giữa trên–dưới

    # ===== KHUNG BẢNG ĐIỂM =====
    frame_scores_table = tk.LabelFrame(frame_right, text="Bảng điểm chi tiết",font=("Times New Roman", 12, "bold"),bg="white",padx=10, pady=10, bd=3, relief="groove")
    frame_scores_table.pack(fill="both", expand=True, padx=20, pady=10)

    table_container = tk.Frame(frame_scores_table, bg="white")
    table_container.pack(fill="both", expand=True)

    # --- Không cần thanh cuộn ngang vì ta làm vừa khung ---
    scroll_y = tk.Scrollbar(table_container, orient="vertical")

    columns = ("ma_mh", "ten_mh", "so_tc", "diem_cc", "diem_gk", "diem_ck", "diem_tk", "diem_chu")
    tree = ttk.Treeview(
        table_container,
        columns=columns,
        show="headings",
        yscrollcommand=scroll_y.set
    )

    scroll_y.config(command=tree.yview)
    scroll_y.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    # --- Cấu hình tiêu đề & độ rộng cột vừa khung ---
    tree.heading("ma_mh", text="Mã Môn Học")
    tree.heading("ten_mh", text="Tên Môn Học")
    tree.heading("so_tc", text="Số TC")
    tree.heading("diem_cc", text="ĐCC")
    tree.heading("diem_gk", text="ĐGK")
    tree.heading("diem_ck", text="ĐCK")
    tree.heading("diem_tk", text="ĐTK")
    tree.heading("diem_chu", text="Điểm Chữ")

    # --- Giãn đều theo khung, không cần kéo ngang ---
    tree.column("ma_mh", width=100, anchor="center")
    tree.column("ten_mh", width=250, anchor="w")
    tree.column("so_tc", width=80, anchor="center")
    tree.column("diem_cc", width=80, anchor="center")
    tree.column("diem_gk", width=80, anchor="center")
    tree.column("diem_ck", width=80, anchor="center")
    tree.column("diem_tk", width=80, anchor="center")
    tree.column("diem_chu", width=100, anchor="center")
    # --- Nâng chiều cao khung cho cân đối ---
    frame_right.update()
    frame_scores_table.configure(height=int(frame_right.winfo_height() * 0.55))

# ====== GÁN SỰ KIỆN CHO CÁC NÚT ======
btn_add_xemdiem.config(command=open_view_scores_form)   

# ====== CHẠY VÒNG LẶP CHÍNH ======
adminform.mainloop()
