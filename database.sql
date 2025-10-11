CREATE DATABASE QLDiemSV
GO

USE QLDiemSV
GO

--=====Table: Tài khoản user =====
CREATE TABLE users(
	userName NVARCHAR(50) PRIMARY KEY,
	pass NVARCHAR(50) NOT NULL
);