import pyodbc
from tkinter import messagebox

def get_db_connect():
    try:
        # ====Kết nối tới sql server====
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP_ASUS\SQLEXPRESS;'
            'DATABASE=QLDiemSV;'
            'UID=sa;'
            'PWD=123123;'
        )
        return conn
    except Exception as e:
        messagebox.showerror("Lỗi kết nối", str(e))
        return None
