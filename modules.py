# Database connection setup
from binascii import Error
from werkzeug.security import generate_password_hash, check_password_hash

import mysql.connector






def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@123",
            database="attendance"
        )
        print("Connecting to database...")
        if connection.is_connected():
            print("MySQL se successfully connected!")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        connection = None
def close_db(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed.")
    # finally:
        # if connection.is_connected():
            # connection.close()
            # print("MySQL connection close ho gayi.")
# Function to show all tables the table
def all_tables_details():
    
    connection = connect_db()
    if connection:
        try:
            mycursor = connection.cursor()
            # Check how many rows match the condition
            mycursor.execute("select * from teacher")
            count = mycursor.fetchall()
            for i in count:
                print(i)
        except Error as e:
            print(f"Error deleting rows: {e}")
all_tables_details()

#for update password of existing password

def update_password(username, new_password):
    try:
        connection=connect_db()
        mycursor = connection.cursor()
        hashed_password = generate_password_hash(new_password)
        # print(hashed_password)
        mycursor.execute("UPDATE registration SET password=%s WHERE name=%s", (hashed_password, username))
        connection.commit()
        # print(f"Password updated successfully for {username}")
    except Error as e:
        print(f"Error updating password: {e}")
    # finally:
    #     mycursor.close()
    #     close_db(connection)

def one_student(Enrollment):
    try:
        connection=connect_db()
        mycursor = connection.cursor()
        mycursor.execute("SELECT * FROM registration WHERE Enrollment_NO=%s", (Enrollment,))
        s = mycursor.fetchone()
        return list(s) if s else None
    except Error as e:
        print(f"Error fetching student: {e}")
        return None
    # finally:
    #     mycursor.close()
    #     close_db(connection)

def all_student():
    try:
        connection=connect_db()
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
 
def add_student(name, Enrollment, email, password,phone,address):
    try:
        connection=connect_db()
        mycursor = connection.cursor()
        hashed_password = generate_password_hash(password)
        mycursor.execute("INSERT INTO registration (Name, Enrollment_NO, Email, password,Phone_NO,Address) VALUES (%s, %s, %s, %s, %s, %s)", (name, Enrollment, email, hashed_password,phone,address))
        connection.commit()
        print(f"Student added successfully: {name}")
    except Error as e:
        print(f"Error adding student: {e}")
    all_student()
        # finally:
        #     mycursor.close()
        #     close_db(connection)
       
def check_name_pass(Enrollment, password):
    user = one_student(Enrollment)
    if user and check_password_hash(user[5], password):  # Adjust the index if necessary
        return True
    return False
