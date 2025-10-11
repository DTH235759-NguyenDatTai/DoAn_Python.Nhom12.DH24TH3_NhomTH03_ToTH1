import pyodbc

try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP_ASUS\\SQLEXPRESS;'
        'DATABASE=QLDiemSV;'
        'Trusted_Connection=yes;'
    )

    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    print("Kết nối thành công! Phiên bản SQL Server:", row[0])

except Exception as e:
    print("Lỗi kết nối:", e)
