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
	PtKt INT NOT NULL,
	PtThi INT NOT NULL,
	HocKy INT NOT NULL,
	NamHoc NVARCHAR(20) NOT NULL,
	MaGV NVARCHAR(20) NOT NULL,

	-- Rằng buộc học kỳ chỉ có 3 học kỳ 1, 2, hè
	CONSTRAINT CK_MonHoc_HocKy CHECK (HocKy IN ('1', '2', '3')),
	-- Rằng buộc khóa ngoại
	CONSTRAINT FK_MonHoc_GiangVien FOREIGN KEY (MaGV) REFERENCES GiangVien(MaGV)
);
GO

-- =============================================
-- BẢNG 5: DIEM
-- =============================================
CREATE TABLE Diem (
    MSSV NVARCHAR(20) NOT NULL,
    MaMH NVARCHAR(20) NOT NULL,

    DiemQT FLOAT NULL,
    DiemCK FLOAT NULL,


	CONSTRAINT PK_Diem PRIMARY KEY (MSSV, MaMH),
    -- Rằng buộc khóa ngoại
	CONSTRAINT FK_Diem_SinhVien FOREIGN KEY (MSSV) REFERENCES SinhVien(MSSV),
	CONSTRAINT FK_Diem_MaMH FOREIGN KEY (MaMH) REFERENCES MonHoc(MaMH)
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

(N'GV007', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'giangvien'),
(N'GV008', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'giangvien'),
(N'GV009', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'giangvien'),
(N'GV010', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'giangvien'),
(N'GV011', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'giangvien'),

(N'DMT234941', N'162e3973ecf8a77629bbf7c8faaf28c13f99d4e7f1affadc616731276ee1d07a', N'sinhvien'),
(N'DTH235759', N'162e3973ecf8a77629bbf7c8faaf28c13f99d4e7f1affadc616731276ee1d07a', N'sinhvien'),
(N'DTH235758', N'21a450ca63e673188f62d47608211457ed9f61dc8184b39c38d8fdf4b9cbaa71', N'sinhvien'),
(N'DTH235829', N'114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', N'sinhvien'),
(N'DKH234819', N'114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', N'sinhvien'),
(N'DKH234801', N'114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', N'sinhvien'),

('DTH235701', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DKT235702', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DNN235703', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DDL235704', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DSP235705', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DTH235706', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DKT235707', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DNN235708', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DDL235709', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DTH235710', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DNN235711', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DTH235712', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DKT235713', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DDL235714', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DNN235715', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DTH235716', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DTA235717', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DKT235718', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DSP235719', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien'),
('DTH235720', '114bd151f8fb0c58642d2170da4ae7d7c57977260ac2cc8905306cab6b2acabc', 'sinhvien');


INSERT INTO SinhVien(MSSV, HoTen, NgaySinh, GioiTinh, Lop, Khoa, TenDangNhap)
VALUES
(N'DMT234941', N'Võ Thị Huỳnh Trân', N'2005-12-17', N'Nữ', N'DH24MT', N'Kỹ Thuật - Công nghệ - Môi Trường', N'DMT234941'),
(N'DTH235759', N'Nguyễn Đạt Tài', N'2005-10-27', N'Nam', N'DH24TH3', N'Công nghệ thông tin', N'DTH235759'),
(N'DTH235758', N'Nguyễn Võ Thanh Sơn', N'2005-01-08', N'Nam', N'DH24TH3', N'Công nghệ thông tin', N'DTH235758'),
(N'DTH235829', N'Lưu Trọng Quý', N'2004-02-01', N'Nam', N'DH24TH3', N'Công nghệ thông tin', N'DTH235829'),
(N'DKH234819', N'Đặng Nguyễn Bảo Thiên', N'2005-02-09', N'Nam', N'DH24KH', N'Kỹ Thuật - Công nghệ - Môi Trường', N'DKH234819'),
(N'DKH234801', N'Nguyễn Hoàng Minh Anh', N'2005-01-01', N'Nữ', N'DH24KH', N'Kỹ Thuật - Công nghệ - Môi Trường', N'DKH234801'),

('DTH235701', N'Nguyễn Văn An', '2005-03-14', N'Nam', N'DH24TH1', N'Công nghệ thông tin', 'DTH235701'),
('DKT235702', N'Trần Thị Mỹ Duyên', '2005-07-22', N'Nữ', N'DH24KT1', N'Kế toán', 'DKT235702'),
('DNN235703', N'Lê Minh Tâm', '2004-12-11', N'Nam', N'DH24NN1', N'Nông nghiệp', 'DNN235703'),
('DDL235704', N'Võ Quốc Huy', '2005-01-08', N'Nam', N'DH24DL1', N'Du lịch', 'DDL235704'),
('DSP235705', N'Nguyễn Ngọc Hân', '2005-06-29', N'Nữ', N'DH24SP1', N'Sư phạm Toán', 'DSP235705'),
('DTH235706', N'Phạm Hoàng Phúc', '2005-05-20', N'Nam', N'DH24TH2', N'Công nghệ thông tin', 'DTH235706'),
('DKT235707', N'Huỳnh Thị Mỹ Linh', '2005-02-25', N'Nữ', N'DH24KT1', N'Kế toán', 'DKT235707'),
('DNN235708', N'Trần Đức Toàn', '2004-09-09', N'Nam', N'DH24NN2', N'Nông nghiệp', 'DNN235708'),
('DDL235709', N'Lâm Gia Huy', '2005-10-15', N'Nam', N'DH24DL2', N'Du lịch', 'DDL235709'),
('DTH235710', N'Võ Thanh Phương', '2005-08-04', N'Nam', N'DH24TH3', N'Công nghệ thông tin', 'DTH235710'),
('DNN235711', N'Lý Bảo Trân', '2005-11-12', N'Nữ', N'DH24NN2', N'Nông nghiệp', 'DNN235711'),
('DTH235712', N'Nguyễn Đức Lộc', '2005-09-18', N'Nam', N'DH24TH2', N'Công nghệ thông tin', 'DTH235712'),
('DKT235713', N'Trương Minh Khải', '2005-07-05', N'Nam', N'DH24KT2', N'Kế toán', 'DKT235713'),
('DDL235714', N'Võ Nhật Hào', '2005-02-08', N'Nam', N'DH24DL2', N'Du lịch', 'DDL235714'),
('DNN235715', N'Nguyễn Thị Cẩm Tiên', '2005-04-25', N'Nữ', N'DH24NN1', N'Nông nghiệp', 'DNN235715'),
('DTH235716', N'Đoàn Minh Khang', '2005-01-14', N'Nam', N'DH24TH3', N'Công nghệ thông tin', 'DTH235716'),
('DTA235717', N'Phan Thị Thu Thảo', '2005-03-19', N'Nữ', N'DH24TA1', N'Ngôn ngữ Anh', 'DTA235717'),
('DKT235718', N'Lưu Minh Đức', '2005-12-09', N'Nam', N'DH24KT2', N'Kế toán', 'DKT235718'),
('DSP235719', N'Nguyễn Thanh Tùng', '2005-06-10', N'Nam', N'DH24SP1', N'Sư phạm Toán', 'DSP235719'),
('DTH235720', N'Hồ Ngọc Yến', '2005-08-21', N'Nữ', N'DH24TH1', N'Công nghệ thông tin', 'DTH235720');
GO

INSERT INTO GiangVien(MaGV,HoTen, GioiTinh, TenDangNhap)
VALUES
(N'GV001', N'H.T.Việt', N'Nam', N'GV001'),
(N'GV002', N'P.V.L.Em', N'Nam', N'GV002'),
(N'GV003', N'N.T.L.Quyên', N'Nữ', N'GV003'),
(N'GV004', N'N.T.N.Loan', N'Nữ', N'GV004'),
(N'GV005', N'L.V.Dót', N'Nam', N'GV005'),
(N'GV006', N'H.T.Thành', N'Nam', N'GV006'),

(N'GV007', N'L.T.H. Trang', N'Nữ', N'GV007'),
(N'GV008', N'T.V.L. Phúc', N'Nam', N'GV008'),
(N'GV009', N'N.T.K. Duyên', N'Nữ', N'GV009'),
(N'GV010', N'P.H. Nghĩa', N'Nam', N'GV010'),
(N'GV011', N'T.T. Đạt', N'Nam', N'GV011');
GO

INSERT INTO MonHoc (MaMH, TenMH, SoTinChi, PtKt, PtThi, HocKy, NamHoc, MaGV)
VALUES
('PHY109', N'Vật lý đại cương', 4, 40, 60, '1', '2023-2024', 'GV006'),
('TEC511', N'Hóa đại cương', 4, 40, 60, '1', '2023-2024', 'GV006'),
('MAT104', N'Toán A1', 3, 40, 60, '1', '2023-2024', 'GV002'),
('COS106', N'Lập trình căn bản', 3, 40, 60, '1', '2023-2024', 'GV001'),
('PHT154', N'Bóng chuyền 1', 3, 40, 60, '2', '2023-2024', 'GV004'),
('PHI104', N'Triết học Mác-Lenin', 2, 50, 50, '2', '2023-2024', 'GV005'),
('MAT105', N'Toán A2', 3, 40, 60, '1', '2024-2025', 'GV002'),
('MAX309', N'Kinh tế chính trị Mác-Lenin', 2, 50, 50, '1', '2024-2025', 'GV005'),
('MAT106', N'Toán A3', 3, 40, 60, '2', '2024-2025', 'GV002'),
('MAX310', N'Chủ nghĩa xã hội', 2, 50, 50, '2', '2024-2025', 'GV003'),
('PRS302', N'Xác suất thống kê', 3, 40, 60, '2', '2024-2025', 'GV002');
GO

USE QL_Diem
SELECT * FROM TaiKhoan
SELECT * FROM GiangVien
SELECT * FROM SinhVien
SELECT * FROM MonHoc
SELECT * FROM Diem
