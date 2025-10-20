CREATE DATABASE QLDiemSV
GO

USE QLDiemSV
GO

-- Luôn đảm bảo bạn đang sử dụng đúng cơ sở dữ liệu
USE QLDiemSV;
GO

-- =============================================
-- BẢNG 1: TAIKHOAN
-- =============================================
CREATE TABLE TaiKhoan(
	TenDangNhap NVARCHAR(50) PRIMARY KEY,
	MatKhauHash NVARCHAR(256) NOT NULL,
	Role NVARCHAR(10) NOT NULL,

	-- Thêm ràng buộc CHECK để đảm bảo Role chỉ nhận các giá trị hợp lệ
	CONSTRAINT CK_TaiKhoan_Role CHECK (Role IN ('admin', 'giaovien', 'sinhvien'))
);
GO
Drop table TaiKhoan

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
-- BẢNG 3: GIAOVIEN
-- =============================================
CREATE TABLE GiaoVien(
	MaGV NVARCHAR(20) PRIMARY KEY,
	HoTen NVARCHAR(100) NOT NULL, 
	GioiTinh NVARCHAR(10) NULL,
	SDT NVARCHAR(15) NULL,    

	-- Thêm cột để liên kết với TaiKhoan, không được null và phải là duy nhất
	TenDangNhap NVARCHAR(50) NOT NULL UNIQUE,

	-- Ràng buộc CHECK cho Giới tính
	CONSTRAINT CK_GiaoVien_GioiTinh CHECK (GioiTinh IN (N'Nam', N'Nữ', N'Khác')),

	-- Ràng buộc khóa ngoại: TenDangNhap phải tồn tại trong bảng TaiKhoan
	CONSTRAINT FK_GiaoVien_TaiKhoan FOREIGN KEY (TenDangNhap) REFERENCES TaiKhoan(TenDangNhap)
);
GO

-- =============================================
-- BẢNG 4: MONHOC
-- =============================================
CREATE TABLE MonHoc(
	MaMH NVARCHAR(20) PRIMARY KEY,
	TenMH NVARCHAR(100) NOT NULL,
	SoTinChi INT NOT NULL,
	MaGV NVARCHAR(20) NOT NULL,

	-- Ràng buộc khóa ngoại: MaGV phải tồn tại trong bảng GiaoVien
	CONSTRAINT FK_MonHoc_GiaoVien FOREIGN KEY (MaGV) REFERENCES GiaoVien(MaGV)
);
GO
-- Thêm cột phòng học lỳ và năm học
ALTER TABLE MonHoc
ADD Phong NVARCHAR(50) NULL,
    HocKy INT NULL,              -- Ví dụ: 1, 2
    NamHoc NVARCHAR(20) NULL;

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
    DiemQuaTrinh FLOAT NULL,     -- Điểm quá trình/giữa kỳ
    DiemThi FLOAT NULL,          -- Điểm thi cuối kỳ
    DiemTongKet FLOAT NULL,      -- Điểm tổng kết (có thể được tính tự động)

    -- Thông tin thêm
    HocKy INT NULL,              -- Ví dụ: 1, 2
    NamHoc NVARCHAR(20) NULL,    -- Ví dụ: '2023-2024'

    -- Thiết lập khóa chính
    CONSTRAINT PK_Diem PRIMARY KEY (MSSV, MaMH),

    -- Thiết lập các khóa ngoại để liên kết
    CONSTRAINT FK_Diem_SinhVien FOREIGN KEY (MSSV) REFERENCES SinhVien(MSSV),
    CONSTRAINT FK_Diem_MonHoc FOREIGN KEY (MaMH) REFERENCES MonHoc(MaMH)
);
GO


--Khởi tại tài khoản
INSERT INTO TaiKhoan(TenDangNhap, MatKhauHash, Role)
VALUES
(N'ADMIN', N'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', N'admin'),
(N'GV001', N'da70dfa4d9f95ac979f921e8e623358236313f334afcd06cddf8a5621cf6a1e9', N'giaovien'),
(N'GV002', N'da70dfa4d9f95ac979f921e8e623358236313f334afcd06cddf8a5621cf6a1e9', N'giaovien'),
(N'GV003', N'da70dfa4d9f95ac979f921e8e623358236313f334afcd06cddf8a5621cf6a1e9', N'giaovien'),
(N'GV004', N'da70dfa4d9f95ac979f921e8e623358236313f334afcd06cddf8a5621cf6a1e9', N'giaovien'),
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
--Chưa insert dữ liệu

USE QLDiemSV
SELECT * FROM TaiKhoan
SELECT * FROM SinhVien
SELECT * FROM GiaoVien
SELECT * FROM MonHoc
SELECT * FROM Diem

