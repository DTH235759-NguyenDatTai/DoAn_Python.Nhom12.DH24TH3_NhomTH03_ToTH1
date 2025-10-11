CREATE DATABASE QLDiemSV
GO

USE QLDiemSV
GO

--=====Table: Tài khoản user =====
CREATE TABLE TaiKhoan(
	TenDangNhap NVARCHAR(50) PRIMARY KEY,
	MatKhauHash NVARCHAR(256) NOT NULL,
	Role NVARCHAR(10) DEFAULT N'sinhvien'   --admin, giaovien, sinhvien
);
Go

INSERT INTO TaiKhoan(TenDangNhap, MatKhauHash, Role)
VALUES
(N'admin', N'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', N'admin'),
(N'gv001', N'da70dfa4d9f95ac979f921e8e623358236313f334afcd06cddf8a5621cf6a1e9', N'giangvien'),
(N'DTH235759', N'162e3973ecf8a77629bbf7c8faaf28c13f99d4e7f1affadc616731276ee1d07a', N'sinhvien'),
(N'DTH235758', N'21a450ca63e673188f62d47608211457ed9f61dc8184b39c38d8fdf4b9cbaa71', N'sinhvien');
GO

USE QLDiemSV
SELECT * FROM TaiKhoan


