import mysql.connector as conn
print("my sql connected")
mydb=conn.connect(host="localhost",user="root",password="12345",database="attendancesheet")
print(mydb,"connection established")
db_cursor=mydb.cursor()
#1 creat database
db_cursor.execute("DROP database IF EXISTS attendancesheet")
db_cursor.execute("create database attendancesheet")
print("database is scuccessfully created")
db_cursor.execute("use attendancesheet")
db_cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name TEXT,
    date TEXT,
    time TEXT,
    status TEXT
)
""")
mydb.commit()
mydb.close()
print("Database Created Successfully")