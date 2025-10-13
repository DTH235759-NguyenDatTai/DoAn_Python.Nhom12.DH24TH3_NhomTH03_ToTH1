CREATE DATABASE QLDiemSV
GO

USE QLDiemSV
GO

-- Luôn đảm bảo bạn đang sử dụng đúng cơ sở dữ liệu
USE QLDiemSV;
GO

-- =============================================
-- BẢNG 1: TAIKHOAN
-- Bảng này phải được tạo trước SinhVien và GiaoVien
-- =============================================
PRINT 'Đang tạo bảng TaiKhoan...';
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
PRINT 'Đang tạo bảng SinhVien...';
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
PRINT 'Đang tạo bảng GiaoVien...';
CREATE TABLE GiaoVien(
	MaGV NVARCHAR(20) PRIMARY KEY,
	HoTen NVARCHAR(100) NOT NULL,       -- Tăng độ dài
	GioiTinh NVARCHAR(10) NULL,
	SDT NVARCHAR(15) NULL,              -- Giảm độ dài cho phù hợp

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
PRINT 'Đang tạo bảng MonHoc...';
CREATE TABLE MonHoc(
	MaMH NVARCHAR(20) PRIMARY KEY,
	TenMH NVARCHAR(100) NOT NULL,       -- Tăng độ dài
	SoTinChi INT NOT NULL,
	MaGV NVARCHAR(20) NOT NULL,

	-- Ràng buộc khóa ngoại: MaGV phải tồn tại trong bảng GiaoVien (đã đúng từ trước)
	CONSTRAINT FK_MonHoc_GiaoVien FOREIGN KEY (MaGV) REFERENCES GiaoVien(MaGV)
);
GO

PRINT 'Tất cả các bảng đã được tạo thành công!';

--Khởi tại tài khoản 
INSERT INTO TaiKhoan(TenDangNhap, MatKhauHash, Role)
VALUES
(N'admin', N'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', N'admin'),
(N'gv001', N'da70dfa4d9f95ac979f921e8e623358236313f334afcd06cddf8a5621cf6a1e9', N'giaovien'),
(N'DTH235759', N'162e3973ecf8a77629bbf7c8faaf28c13f99d4e7f1affadc616731276ee1d07a', N'sinhvien'),
(N'DTH235758', N'21a450ca63e673188f62d47608211457ed9f61dc8184b39c38d8fdf4b9cbaa71', N'sinhvien');
GO

USE QLDiemSV
SELECT * FROM TaiKhoan
SELECT * FROM SinhVien
SELECT * FROM GiaoVien
SELECT * FROM MonHoc


