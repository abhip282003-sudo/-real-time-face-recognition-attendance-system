import mysql.connector as conn
mydb=conn.connect(host="localhost",user="root",password="12345",database="attendancesheet")
db_cursor = mydb.cursor()
db_cursor.execute("SELECT * FROM attendance")
rows = db_cursor.fetchall()
for row in rows:
    print(row)
mydb.close()