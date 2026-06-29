import mysql.connector as mysql
from datetime import datetime

def mark_attendance(name):
    connection = mysql.connect(
        host="localhost",
        user="root",
        password="12345",
        database="attendancesheet"
    )

    cursor = connection.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    cursor.execute(
        "SELECT * FROM attendance WHERE name=%s AND date=%s",
        (name, today)
    )
    data = cursor.fetchone()

    if data is None:
        cursor.execute(
            "INSERT INTO attendance(name, date, time, status) VALUES (%s, %s, %s, %s)",
            (name, today, current_time, "Present")
        )
        connection.commit()
        print(f"{name} Attendance Saved")
    else:
        print(f"{name} Attendance Already Marked")

    cursor.close()
    connection.close()