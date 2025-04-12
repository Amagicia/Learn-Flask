# Database connection setup
from binascii import Error
from datetime import datetime
import serial
from werkzeug.security import generate_password_hash, check_password_hash

import mysql.connector


# Set up the serial connection (update COM port to match your system)
arduino_port = "COM5"  # Update this to your Arduino's port
baud_rate = 9600  # Must match the baud rate in the Arduino code

# Arduino RFID reader
try:
    arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
    print("\n=== RFID Attendance System ===")
    print("✓ RFID Reader Connected!")
    print("Waiting for cards...")
except:
    print("✗ Could not connect to RFID Reader!")
    arduino = None


def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="attendance"
        )
        print("Connecting to database...")
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        connection = None


def close_db(connection):
    if connection.is_connected():
        connection.close()


# Function to show all tables the table
def cheack_database():
    connection = connect_db()
    if connection:
        print("ho gya connect")
        try:
            mycursor = connection.cursor()
            mycursor.execute("desc attendance")
            # mycursor.execute("delete from schedule where subject_code='BT301'")
            count = mycursor.fetchall()
            for i in count:
                print(i)

            # mycursor.execute("DELETE FROM registration WHERE Enrollment_NO ='20'")
            # count = mycursor.fetchall()
            # connection.commit()
            print("Data deleted successfully")

            # print(count)
            # for i in count:
            # print(i)
            # connection.commit()
            # print("Table created successfully")
            return True
        except Error as e:
            print(f"Error deleting rows: {e}")
        finally:
            close_db(connection)


cheack_database()
# cheack_database()
# all_tables_details()
# print(a)


# def update_password(
#     username, new_password
# ):  # Yeh function password update karne ke liye hai
#     try:
#         connection = connect_db()  # Database se connection establish karte hain
#         mycursor = connection.cursor()  # Cursor object banate hain
#         hashed_password = generate_password_hash(
#             new_password
#         )  # Password ko hash karte hain
#         mycursor.execute(
#             "UPDATE registration SET password=%s WHERE name=%s",
#             (hashed_password, username),
#         )  # SQL query execute karte hain password update karne ke liye
#         connection.commit()  # Changes ko commit karte hain
#     except Error as e:  # Agar koi error aata hai to usko catch karte hain
#         print(f"Error updating password: {e}")  # Error message print karte hain


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
    if user and check_password_hash(user[5], password):  # Check password hash
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
            # mycursor.execute("ALTER TABLE schedule AUTO_INCREMENT = 1")
            # connection.commit()
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
            # print(current_day)
            # print(current_time)
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
            subjectname = mycursor.fetchall()
            return subjectname[0] if subject else None
    except Error as e:
        print(f"Error fetching subject: {e}")
        return None
    finally:
        close_db(connection)


def get_subject_by_code(subject_code):
    try:
        connection = (
            connect_db()
        )  # Ensure you have a function to establish DB connection
        mycursor = connection.cursor()

        # Fetch the subject name based on the subject code
        mycursor.execute(
            "SELECT Subject_name FROM subject WHERE Subject_code = %s", (subject_code,)
        )
        subjectname = mycursor.fetchone()

        return subjectname[0] if subjectname else None
    except Error as e:
        print(f"Error fetching subject: {e}")
        return None
    finally:
        if connection:
            close_db(connection)  # Ensure the connection is closed properly


# Example usage:
# subject_name = get_subject_by_code('SUB123')
# print(subject_name)


def fetch_all_attendance():
    try:
        connection = (
            connect_db()
        )  # Ensure you have a function to establish DB connection
        mycursor = connection.cursor()

        # Fetch all attendance records
        mycursor.execute("SELECT * FROM attendance")
        attendance_records = mycursor.fetchall()

        return attendance_records
    except Error as e:
        print(f"Error fetching attendance: {e}")
        return None
    finally:
        if connection:
            close_db(connection)  # Ensure the connection is closed properly


def fetch_all_attendance():
    try:
        connection = connect_db()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT a.enrollment_no, r.name, a.subject_code, a.attendance_date, a.RFID_SCAN, a.attendance_status
                FROM attendance a
                JOIN registration r ON a.enrollment_no = r.Enrollment_NO
            """
            cursor.execute(query)
            attendance_records = cursor.fetchall()
            return attendance_records
    except Error as e:
        print(f"Error fetching attendance records: {e}")
        return None
    finally:
        close_db(connection)


def mark_attendance(card_id):
    """Mark attendance for the student"""
    db = connect_db()
    if not db:
        print("✗ Database connection failed")
        return False, "Database connection failed"

    try:
        cursor = connect_db.cursor(dictionary=True)

        # Find student by RFID
        cursor.execute("SELECT * FROM registration WHERE RFID_ID = %s", (card_id,))
        student = cursor.fetchone()

        if not student:
            print(f"✗ Unknown Card: No student registered with ID {card_id}")
            return False, "No student found with this card"

        print(f"✓ Student Found: {student['Name']} ({student['Enrollment_NO']})")

        # Check if already marked today
        today = datetime.now().date()
        cursor.execute(
            """
            SELECT * FROM attendance 
            WHERE enrollment_no = %s 
            AND attendance_date = %s
        """,
            (student["Enrollment_NO"], today),
        )

        if cursor.fetchone():
            print(
                f"! Already Present: {student['Name']} was marked present earlier today"
            )
            return False, f"{student['Name']} already marked present today"

        # Mark attendance
        current_time = datetime.now().time()
        cursor.execute(
            """
            INSERT INTO attendance 
            (enrollment_no, attendance_date, RFID_SCAN, attendance_status)
            VALUES (%s, %s, %s, 'P')
        """,
            (student["Enrollment_NO"], today, current_time),
        )

        # Update total present
        cursor.execute(
            """
            UPDATE registration 
            SET Total_Present = Total_Present + 1 
            WHERE Enrollment_NO = %s
        """,
            (student["Enrollment_NO"],),
        )

        db.commit()
        print(
            f"✓ Marked Present: {student['Name']} at {current_time.strftime('%I:%M:%S %p')}"
        )
        print(f"  Total Present: {student['Total_Present'] + 1} days")
        print("-" * 40)
        return True, f"Marked {student['Name']} present"

    except Exception as e:
        print(f"✗ Error: {e}")
        return False, "Error marking attendance"
    finally:
        db.close()


def read_rfid():
    """Read RFID card number"""
    if arduino and arduino.in_waiting:
        try:
            card_id = arduino.readline().decode("utf-8").strip()
            if card_id:
                print(
                    f"\n[{datetime.now().strftime('%I:%M:%S %p')}] Card Detected: {card_id}"
                )
                return card_id
        except:
            print("Error reading card!")
    return None
