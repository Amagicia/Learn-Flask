from flask import session
import serial
import mysql.connector
from mysql.connector import Error
from modules import *
from datetime import datetime

# Set up the serial connection (update COM port to match your system)
arduino_port = "COM5"  # Update this to your Arduino's port
baud_rate = 9600  # Must match the baud rate in the Arduino code


def add_rfid(uid):
    try:
        enrollment_no = session["enrollment_no"]
        if not enrollment_no:
            print("Enrollment number not found in session")
            return

        connection = connect_db()
        if connection:
            cursor = connection.cursor()
            query = "UPDATE registration SET RFID_ID = %s WHERE Enrollment_NO = %s"
            cursor.execute(query, (uid, enrollment_no))
            connection.commit()
            print("RFID tag registered successfully with enrollment number")
    except mysql.connector.errors.IntegrityError as e:
        if e.errno == 1062:  # Duplicate entry error code
            print(f"Error: Duplicate entry for RFID tag {uid}")
            return "duplicate_entry"
        else:
            print(f"Error registering RFID tag: {e}")
            return False
    finally:
        close_db(connection)


# Function to handle RFID card logic and mark attendance
def process_card(uid, ser):
    try:
        connection = connect_db()
        if connection:
            cursor = connection.cursor(dictionary=True)

            # Check if the card exists in the registration table
            query = "SELECT * FROM registration WHERE RFID_ID = %s"
            cursor.execute(query, (uid,))
            student = cursor.fetchone()

            if student:
                enrollment_no = student["Enrollment_NO"]
                subject_name = get_subject_by_current_day_and_time()
                cursor = connection.cursor(dictionary=True)
                cursor.execute(
                    "SELECT subject_code FROM subject WHERE Subject_name = %s",
                    (subject_name,),
                )
                subject_code = cursor.fetchone()
                print(f"Subject code: {subject_code['subject_code']}")
                Sub_code = subject_code["subject_code"]
                if subject_code:
                    # Check if subject_code exists in the subject table
                    cursor.execute(
                        "SELECT * FROM subject WHERE Subject_code = %s", (Sub_code,)
                    )
                    subject = cursor.fetchone()
                    if not subject:
                        print(
                            f"Error: Subject Code {Sub_code} not found in subject table"
                        )
                        ser.write(b"0")
                        return

                    # Check if attendance is already marked for this subject
                    attendance_date = datetime.now().strftime("%Y-%m-%d")
                    check_query = """
                        SELECT * FROM attendance 
                        WHERE enrollment_no = %s AND subject_code = %s AND attendance_date = %s
                    """
                    cursor.execute(
                        check_query, (enrollment_no, Sub_code, attendance_date)
                    )
                    attendance = cursor.fetchone()

                    if not attendance:
                        # Mark attendance
                        rfid_scan_time = datetime.now().strftime("%H:%M:%S")
                        attendance_status = "P"  # Assuming 'P' for present
                        insert_query = """
                            INSERT INTO attendance (enrollment_no, subject_code, attendance_date, RFID_SCAN, attendance_status)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                        cursor.execute(
                            insert_query,
                            (
                                enrollment_no,
                                Sub_code,
                                attendance_date,
                                rfid_scan_time,
                                attendance_status,
                            ),
                        )
                        connection.commit()
                        print("Attendance marked successfully")
                        # Activate buzzer
                        ser.write(b"1")
                    else:
                        print("Attendance already marked for this subject")
                        # Deactivate buzzer
                        ser.write(b"0")
                else:
                    print("No current subject found")
                    # Deactivate buzzer
                    ser.write(b"0")
            else:
                print("RFID not registered")
                # Deactivate buzzer
                ser.write(b"0")
    except Error as e:
        print(f"Error processing card: {e}")
    finally:
        close_db(connection)


def is_hexadecimal(input_string):
    # """Checks if a string is a valid hexadecimal representation."""
    try:
        int(input_string, 16)  # Try converting to integer with base 16
        return True
    except ValueError:
        return False


# Function to read RFID data from Arduino
def read_rfid_from_arduino():
    try:
        ser = serial.Serial(arduino_port, baud_rate)
        print("Connected to Arduino")
        while True:
            if ser.in_waiting > 0:
                rfid_uid = ser.readline().decode("utf-8").strip()
                print(f"RFID UID: {rfid_uid}")
                # if not enrollment_no:
                #     print("Enrollment number not found in session")
                #     return
                if is_hexadecimal(rfid_uid):
                    print("Valid RFID data")

                    if "enrollment_no" in session:
                        add_rfid(rfid_uid)
                        break

                    process_card(rfid_uid, ser)

                # process_card(rfid_uid, ser)
    except serial.SerialException as e:
        print(f"Error reading from Arduino: {e}")


# Call the function to read RFID data from Arduino
# read_rfid_from_arduino()
