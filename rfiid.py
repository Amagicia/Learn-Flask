from flask import Flask, session
import serial
from mysql.connector import Error
from modules import connect_db, close_db, get_subject_by_current_day_and_time
from datetime import datetime

app = Flask(__name__)
app.secret_key = "12688fuy234y512cy5c12ucf"  # Secret key for session management

# Set up the serial connection (update COM port to match your system)
arduino_port = "COM5"  # Update this to your Arduino's port
baud_rate = 9600  # Must match the baud rate in the Arduino code


# Function to handle RFID card logic and mark attendance
def process_card(uid, ser):
    try:
        connection = connect_db()
        if connection:
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM registration WHERE RFID_ID = %s"
            cursor.execute(query, (uid,))
            student = cursor.fetchone()

            if student:
                enrollment_no = student["Enrollment_NO"]
                subject_code = get_subject_by_current_day_and_time()

                if subject_code:
                    attendance_date = datetime.now().strftime("%Y-%m-%d")
                    check_query = """
                        SELECT * FROM attendance 
                        WHERE enrollment_no = %s AND subject_code = %s AND attendance_date = %s
                    """
                    cursor.execute(
                        check_query, (enrollment_no, subject_code, attendance_date)
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
                                subject_code,
                                attendance_date,
                                rfid_scan_time,
                                attendance_status,
                            ),
                        )
                        connection.commit()
                        print("Attendance marked successfully")
                        # Send success signal to Arduino
                        ser.write(b"1")
                    else:
                        print("Attendance already marked for this subject")
                        # Send already marked signal to Arduino
                        ser.write(b"2")
                else:
                    print("No current subject found")
                    # Send no subject signal to Arduino
                    ser.write(b"3")
            else:
                print("RFID not registered")
                # Send not registered signal to Arduino
                ser.write(b"4")
    except Error as e:
        print(f"Error processing card: {e}")
        # Send error signal to Arduino
        ser.write(b"5")
    finally:
        close_db(connection)


# Function to read RFID data from Arduino
def read_rfid_from_arduino():
    try:
        ser = serial.Serial(arduino_port, baud_rate)
        print("Connected to Arduino")
        while True:
            if ser.in_waiting > 0:
                rfid_uid = ser.readline().decode("utf-8").strip()
                print(f"RFID UID: {rfid_uid}")
                process_card(rfid_uid, ser)
    except serial.SerialException as e:
        print(f"Error reading from Arduino: {e}")
        # list_serial_ports()


if __name__ == "__main__":
    read_rfid_from_arduino()
