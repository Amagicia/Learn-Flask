# Database connection setup
from binascii import Error
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

import mysql.connector


def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="attendance"
        )
        print("Connecting to database...")
        if connection.is_connected():
            # print("MySQL se successfully connected!")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        connection = None


def close_db(connection):
    if connection.is_connected():
        connection.close()
        # print("MySQL connection closed.")

        # print("MySQL connection close ho gayi.")


# Function to show all tables the table
def all_tables_details():
    connection = connect_db()
    if connection:
        try:
            mycursor = connection.cursor()
            mycursor.execute("desc attendance")
            # mycursor.execute("delete from schedule where subject_code='BT301'")
            count = mycursor.fetchall()
            for i in count:
                print(i)

            mycursor.execute("select * from attendance")
            count = mycursor.fetchall()
            print(count)
            for i in count:
                print(i)
            # connection.commit()
            # print("Table created successfully")
            return True
        except Error as e:
            print(f"Error deleting rows: {e}")
        finally:
            close_db(connection)


# all_tables_details()
# print(a)


def update_password(
    username, new_password
):  # Yeh function password update karne ke liye hai
    try:
        connection = connect_db()  # Database se connection establish karte hain
        mycursor = connection.cursor()  # Cursor object banate hain
        hashed_password = generate_password_hash(
            new_password
        )  # Password ko hash karte hain
        mycursor.execute(
            "UPDATE registration SET password=%s WHERE name=%s",
            (hashed_password, username),
        )  # SQL query execute karte hain password update karne ke liye
        connection.commit()  # Changes ko commit karte hain
    except Error as e:  # Agar koi error aata hai to usko catch karte hain
        print(f"Error updating password: {e}")  # Error message print karte hain


def one_student(
    Enrollment,
):  # Yeh function ek student ki details fetch karne ke liye hai
    try:
        connection = connect_db()  # Database se connection establish karte hain
        mycursor = connection.cursor()  # Cursor object banate hain
        mycursor.execute(
            "SELECT * FROM registration WHERE Enrollment_NO=%s", (Enrollment,)
        )  # SQL query execute karte hain student details fetch karne ke liye
        s = mycursor.fetchone()  # Ek row fetch karte hain
        return (
            list(s) if s else None
        )  # Agar row milti hai to usko list mein convert karke return karte hain, nahi to None return karte hain
    except Error as e:  # Agar koi error aata hai to usko catch karte hain
        print(f"Error fetching student: {e}")  # Error message print karte hain
        return None  # None return karte hain agar error aata hai


def all_student():
    try:
        connection = connect_db()
        mycursor = connection.cursor()
        mycursor.execute("SELECT * FROM registration ORDER BY name DESC")
        all_student_data = mycursor.fetchall()
        mycursor.execute("SHOW COLUMNS FROM registration")
        columns = [column[0] for column in mycursor.fetchall()]
        return all_student_data, columns
    except Error as e:
        print(f"Error fetching all students: {e}")
        return [], []
    # finally:
    #     mycursor.close()
    #     close_db(connection)


def add_student(name, Enrollment, email, password, phone, address):
    try:
        connection = connect_db()
        mycursor = connection.cursor()
        hashed_password = generate_password_hash(password)
        mycursor.execute(
            "INSERT INTO registration (Name, Enrollment_NO, Email, password,Phone_NO,Address) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, Enrollment, email, hashed_password, phone, address),
        )
        connection.commit()
        print(f"Student added successfully: {name}")
    except Error as e:
        print(f"Error adding student: {e}")
    # all_student()
    # finally:
    #     mycursor.close()
    #     close_db(connection)


def check_name_pass(Enrollment, password):
    user = one_student(Enrollment)
    if user and check_password_hash(user[5], password):  # Adjust the index if necessary
        return True
    return False


def authenticate_user(username, password):
    connection = connect_db()
    cur = connection.cursor()
    cur.execute(
        "SELECT username,'admin' AS role FROM teacher WHERE username=%s AND password=%s",
        (username, password),
    )
    # return list(s) if s else None
    teacher = cur.fetchone()
    if teacher:
        return list(teacher)
    else:
        mycursor = connection.cursor()
        Cpass = check_name_pass(username, password)
        if Cpass:
            mycursor.execute(
                "SELECT name,'student' AS role FROM registration WHERE Enrollment_NO=%s",
                (username,),
            )
            s = mycursor.fetchone()
            # for i in s:
            #     print(i)
            if s:
                return list(s)
        else:
            return None

    return None


def add_subject(subject_code, start_time, end_time, day):
    try:
        connection = connect_db()
        if connection:
            mycursor = connection.cursor()
            # Check if subject_code exists in the subjects table
            mycursor.execute("ALTER TABLE schedule AUTO_INCREMENT = 1")

            connection.commit()
            mycursor.execute(
                "SELECT * FROM subject WHERE Subject_code=%s", (subject_code,)
            )
            subject = mycursor.fetchone()
            if not subject:
                print(f"Error: Subject code {subject_code} not found")
                # return "subject_not_found"
                return False

            # Insert into schedule table
            mycursor.execute(
                "INSERT INTO schedule (subject_code, start_time, end_time, day) VALUES (%s, %s, %s, %s)",
                (subject_code, start_time, end_time, day),
            )
            connection.commit()
            print(f"Subject Added Successfully: {subject_code}")
            return True
    except Error as e:
        if e.errno == 1062:  # Duplicate entry error code
            print(f"Error: Duplicate entry for subject {subject_code} on {day}")
            return "duplicate_entry"

        else:
            print(f"Error: {e}")
            return False
    finally:
        close_db(connection)

        # ALTER TABLE subjects AUTO_INCREMENT = 1;


def get_subject_by_current_day_and_time():
    try:
        connection = connect_db()
        if connection:
            mycursor = connection.cursor()
            current_day = datetime.now().strftime("%A")
            current_time = datetime.now().strftime("%H:%M:%S")
            print(current_day)
            print(current_time)
            mycursor.execute(
                """
                SELECT subject_code 
                FROM schedule 
                WHERE day=%s AND start_time <= %s AND end_time >= %s
            """,
                (current_day, current_time, current_time),
            )
            subject = mycursor.fetchone()
            if not subject:
                print(
                    f"Error: No subject scheduled for {current_day} at {current_time}"
                )
                return None
            s = subject[0]
            # mycursor.execute("SELECT * from subject where Subject_code=%s",(s,))
            mycursor.execute(
                "SELECT Subject_name from subject where Subject_code=%s", (s,)
            )
            subjectname = mycursor.fetchone()
            return subjectname[0] if subject else None
    except Error as e:
        print(f"Error fetching subject: {e}")
        return None
    finally:
        close_db(connection)


# a=get_subject_by_current_day_and_time()
# print(a)


def RFID_A(timestamp, RFID):
    try:
        connection = connect_db()
        if connection:
            mycursor = connection.cursor()
            mycursor.execute("SELECT * FROM registration WHERE RFID=%s", (RFID,))
            student = mycursor.fetchone()
            if not student:
                print(f"Error: Student with RFID {RFID} not found")
                return False
            mycursor.execute(
                "SELECT * FROM attendance WHERE RFID=%s AND Date=%s", (RFID, timestamp)
            )
            attendance = mycursor.fetchone()
            if attendance:
                print(f"Error: Attendance already marked for {RFID} on {timestamp}")
                return False
            mycursor.execute(
                "SELECT * FROM schedule WHERE day=%s AND start_time <= %s AND end_time >= %s",
                (
                    datetime.now().strftime("%A"),
                    datetime.now().strftime("%H:%M:%S"),
                    datetime.now().strftime("%H:%M:%S"),
                ),
            )
            subject = mycursor.fetchone()
            if not subject:
                print(
                    f"Error: No subject scheduled for {datetime.now().strftime('%A')} at {datetime.now().strftime('%H:%M:%S')}"
                )
                return False
            mycursor.execute(
                "INSERT INTO attendance (RFID, Date, Subject_code) VALUES (%s, %s, %s)",
                (RFID, timestamp, subject[0]),
            )
            connection.commit()
            print(f"Attendance marked successfully for {RFID} on {timestamp}")
            return True
    except Error as e:
        print(f"Error marking attendance: {e}")
        return False
    finally:
        close_db(connection)


# def add_rfid(RFID, Enrollment):
#     try:
#         connection = connect_db()
#         if connection:
#             mycursor = connection.cursor()
#             mycursor.execute(
#                 "SELECT * FROM registration WHERE Enrollment_NO=%s", (Enrollment,)
#             )
#             student = mycursor.fetchone()
#             if not student:
#                 print(f"Error: Student with Enrollment {Enrollment} not found")
#                 return False
#             mycursor.execute("SELECT * FROM registration WHERE RFID_ID=%s", (RFID,))
#             rfid = mycursor.fetchone()
#             if rfid:
#                 print(f"Error: RFID {RFID} already assigned to {rfid[1]}")
#                 return False
#             mycursor.execute(
#                 "UPDATE registration SET RFID_ID=%s WHERE Enrollment_NO=%s",
#                 (RFID, Enrollment),
#             )
#             connection.commit()
#             print(f"RFID {RFID} assigned to {student[1]} successfully")
#             return True
#     except Error as e:
#         print(f"Error assigning RFID: {e}")
#         return False
#     finally:
#         close_db(connection)
