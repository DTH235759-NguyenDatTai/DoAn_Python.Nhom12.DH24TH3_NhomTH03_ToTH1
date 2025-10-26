CREATE DATABASE QL_Diem

USE QL_Diem
GO

-- =============================================
-- BẢNG 1: TAIKHOAN
-- =============================================
CREATE TABLE TaiKhoan(
	TenDangNhap NVARCHAR(50) PRIMARY KEY,
	MatKhauHash NVARCHAR(256) NOT NULL,
	Role NVARCHAR(10) NOT NULL,

	-- Thêm ràng buộc CHECK để đảm bảo Role chỉ nhận các giá trị hợp lệ
	CONSTRAINT CK_TaiKhoan_Role CHECK (Role IN ('admin', 'giangvien', 'sinhvien'))
);
GO

-- =============================================
-- BẢNG 2: SINHVIEN
-- =============================================
CREATE TABLE SinhVien(
	MSSV NVARCHAR(20) PRIMARY KEY,
	HoTen NVARCHAR(100) NOT NULL,   
	NgaySinh DATE NULL,
	GioiTinh NVARCHAR(10) NULL,
	Lop NVARCHAR(50) NULL,
	Khoa NVARCHAR(100) NULL,

	-- Thêm cột để liên kết với TaiKhoan, không được null và phải là duy nhất
	TenDangNhap NVARCHAR(50) NOT NULL UNIQUE,

	-- Ràng buộc CHECK cho Giới tính
	CONSTRAINT CK_SinhVien_GioiTinh CHECK (GioiTinh IN (N'Nam', N'Nữ', N'Khác')),

	-- Ràng buộc khóa ngoại: TenDangNhap phải tồn tại trong bảng TaiKhoan
	CONSTRAINT FK_SinhVien_TaiKhoan FOREIGN KEY (TenDangNhap) REFERENCES TaiKhoan(TenDangNhap)
);
GO

-- =============================================
-- BẢNG 3: GIANGVIEN
-- =============================================
CREATE TABLE GiangVien(
	MaGV NVARCHAR(20) PRIMARY KEY,
	HoTen NVARCHAR(100) NOT NULL, 
	GioiTinh NVARCHAR(10) NULL, 

	-- Thêm cột để liên kết với TaiKhoan, không được null và phải là duy nhất
	TenDangNhap NVARCHAR(50) NOT NULL UNIQUE,

	-- Ràng buộc CHECK cho Giới tính
	CONSTRAINT CK_GiangVien_GioiTinh CHECK (GioiTinh IN (N'Nam', N'Nữ')),

	-- Ràng buộc khóa ngoại: TenDangNhap phải tồn tại trong bảng TaiKhoan
	CONSTRAINT FK_GiangVien_TaiKhoan FOREIGN KEY (TenDangNhap) REFERENCES TaiKhoan(TenDangNhap)
);
GO

-- =============================================
-- BẢNG 4: MONHOC
-- =============================================
CREATE TABLE MonHoc(
	MaMH NVARCHAR(20) PRIMARY KEY,
	TenMH NVARCHAR(100) NOT NULL,
	SoTinChi INT NOT NULL,
	Phong NVARCHAR(50) NULL,
    HocKy INT NULL,              -- Ví dụ: 1, 2
    NamHoc NVARCHAR(20) NULL,
	MaGV NVARCHAR(20) NOT NULL,
	-- Ràng buộc khóa ngoại: MaGV phải tồn tại trong bảng GiaoVien
	CONSTRAINT FK_MonHoc_GiangVien FOREIGN KEY (MaGV) REFERENCES GiangVien(MaGV)
);
GO

-- =============================================
-- BẢNG 5: DIEM
-- Bảng này lưu điểm của sinh viên cho từng môn học.
-- Khóa chính là sự kết hợp của MSSV và MaMH, đảm bảo mỗi sinh viên
-- chỉ có một hàng điểm duy nhất cho mỗi môn học.
-- =============================================
CREATE TABLE Diem (
    -- Khóa chính kết hợp (Composite Primary Key)
    MSSV NVARCHAR(20) NOT NULL,
    MaMH NVARCHAR(20) NOT NULL,
	TenMH NVARCHAR(100) NOT NULL, 

    -- Các cột điểm
	TinChi INT NULL,
	PhanTram_KT INT NULL,
	PhanTram_Thi INT NULL,
    DiemQuaTrinh FLOAT NULL,
    DiemThi FLOAT NULL,  
    DiemTongKet FLOAT NULL, 

    -- Thông tin thêm
    HocKy INT NULL,       
    NamHoc NVARCHAR(20) NULL,    

    -- Thiết lập khóa chính
    CONSTRAINT PK_Diem PRIMARY KEY (MSSV, MaMH),

    -- Thiết lập các khóa ngoại để liên kết
    CONSTRAINT FK_Diem_SinhVien FOREIGN KEY (MSSV) REFERENCES SinhVien(MSSV),
    CONSTRAINT FK_Diem_MonHoc FOREIGN KEY (MaMH) REFERENCES MonHoc(MaMH)
);
GO

--Khởi tại Giá trị

INSERT INTO TaiKhoan(TenDangNhap, MatKhauHash, Role)
VALUES
(N'ADMIN', N'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', N'admin'),
(N'GV001', N'da70dfa4d9f95ac979f921e8e623358236313f334afcd06cddf8a5621cf6a1e9', N'giangvien'),
(N'GV002', N'da70dfa4d9f95ac979f921e8e623358236313f334afcd06cddf8a5621cf6a1e9', N'giangvien'),
(N'GV003', N'da70dfa4d9f95ac979f921e8e623358236313f334afcd06cddf8a5621cf6a1e9', N'giangvien'),
(N'GV004', N'da70dfa4d9f95ac979f921e8e623358236313f334afcd06cddf8a5621cf6a1e9', N'giangvien'),
(N'GV005', N'da70dfa4d9f95ac979f921e8e623358236313f334afcd06cddf8a5621cf6a1e9', N'giangvien'),
(N'GV006', N'da70dfa4d9f95ac979f921e8e623358236313f334afcd06cddf8a5621cf6a1e9', N'giangvien'),
(N'DMT234941', N'162e3973ecf8a77629bbf7c8faaf28c13f99d4e7f1affadc616731276ee1d07a', N'sinhvien'),
(N'DTH235759', N'162e3973ecf8a77629bbf7c8faaf28c13f99d4e7f1affadc616731276ee1d07a', N'sinhvien'),
(N'DTH235758', N'21a450ca63e673188f62d47608211457ed9f61dc8184b39c38d8fdf4b9cbaa71', N'sinhvien'),
(N'DTH235829', N'114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', N'sinhvien'),
(N'DKH234819', N'114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', N'sinhvien'),
(N'DKH234801', N'114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', N'sinhvien');
GO

INSERT INTO SinhVien(MSSV, HoTen, NgaySinh, GioiTinh, Lop, Khoa, TenDangNhap)
VALUES
(N'DMT234941', N'Võ Thị Huỳnh Trân', N'2005-12-17', N'Nữ', N'DH24MT', N'Kỹ Thuật - Công nghệ - Môi Trường', N'DMT234941'),
(N'DTH235759', N'Nguyễn Đạt Tài', N'2005-10-27', N'Nam', N'DH24TH3', N'Công nghệ thông tin', N'DTH235759'),
(N'DTH235758', N'Nguyễn Võ Thanh Sơn', N'2005-01-08', N'Nam', N'DH24TH3', N'Công nghệ thông tin', N'DTH235758'),
(N'DTH235829', N'Lưu Trọng Quý', N'2004-02-01', N'Nam', N'DH24TH3', N'Công nghệ thông tin', N'DTH235829'),
(N'DKH234819', N'Đặng Nguyễn Bảo Thiên', N'2005-02-09', N'Nam', N'DH24KH', N'Kỹ Thuật - Công nghệ - Môi Trường', N'DKH234819'),
(N'DKH234801', N'Nguyễn Hoàng Minh Anh', N'2005-01-01', N'Nữ', N'DH24KH', N'Kỹ Thuật - Công nghệ - Môi Trường', N'DKH234801');
Go

INSERT INTO GiangVien(MaGV,HoTen, GioiTinh, TenDangNhap)
VALUES
(N'GV001', N'H.T.Việt', N'Nam', N'GV001'),
(N'GV002', N'P.V.L.Em', N'Nam', N'GV002'),
(N'GV003', N'N.T.L.Quyên', N'Nữ', N'GV003'),
(N'GV004', N'N.T.N.Loan', N'Nữ', N'GV004'),
(N'GV005', N'L.V.Dót', N'Nam', N'GV005'),
(N'GV006', N'H.T.Thành', N'Nam', N'GV006');
Go

INSERT INTO MonHoc(MaMH, TenMH, SoTinChi, Phong, HocKy, NamHoc, Nhom, MaGV)
VALUES
(N'PHY109', N'Vật lý đại cương', N'4', 'NA101', '1', '2023-2024', '2', N'GV005'),
(N'TEC511', N'Hóa đại cương', N'4', 'NA201', '1', '2023-2024', '1', N'GV006'),
(N'MAT104', N'Toán A1', N'3', 'ND101', '1', '2023-2024', '3', N'GV002'),
(N'COS106', N'Lập trình căn bản', N'3', 'ND401', '1', '2023-2024', '1', N'GV001'),
(N'PHT154', N'Bóng chuyền 1', N'3', 'ND309', '2', '2023-2024', '3', N'GV004'),
(N'PHI104', N'Triết học Mác-Lenin', N'2', 'ND202', '2', '2023-2024', '5', N'GV005'),
(N'MAT105', N'Toán A2', N'3', 'NA303', '2', '2023-2024', '2', N'GV002'),
(N'MAT106', N'Toán A3', N'3', 'NA303', '1', '2024-2025', '5', N'GV002'),
(N'MAX309', N'Kinh tế chính trị Mác-Lenin', N'2', 'NC203', '1', '2024-2025', '3', N'GV005'),
(N'MAX310', N'Chủ nghĩa xã hội', N'2', 'NA303', '2', '2024-2025', '2', N'GV003'),
(N'PRS302', N'Xác xuất thống kê', N'3', 'ND403', '2', '2024-2025', '1', N'GV003');
GO


USE QL_Diem
SELECT * FROM TaiKhoan
SELECT * FROM GiangVien
SELECT * FROM SinhVien
SELECT * FROM MonHoc
SELECT * FROM Diem

DELETE MonHoc WHERE MaMH = 'CON503'