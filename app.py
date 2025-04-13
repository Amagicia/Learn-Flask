import os
from flask import (
    Flask,
    flash,
    render_template,
    request,
    redirect,
    send_file,
    url_for,
    session,
)
from fpdf import FPDF
from flask_debugtoolbar import DebugToolbarExtension
from mysql.connector import Error
from datetime import timedelta
from modules import *
from werkzeug.security import generate_password_hash, check_password_hash

# from rfiid import *


# Initialize the Flask app

app = Flask(__name__)
toolbar = DebugToolbarExtension(app)

app.secret_key = "12688fuy234y512cy5c12ucf"  # Secret key for session management
app.permanent_session_lifetime = timedelta(minutes=10)  # Set session lifetime to 7 days

from dotenv import load_dotenv
import os

# Load .env vars
load_dotenv()


@app.route("/new")
def new():
    """Home page with attendance list"""
    attendance_records = fetch_all_attendance()
    return render_template("new.html", attendance_records=attendance_records)


@app.route("/", methods=["GET", "POST"])
def login():
    print("Connected to DB as:", os.getenv("MYSQL_USER"))
    if "Name" in session:
        # print(f"Session Name: {session['Name']}, Role: {session.get('Role')}")
        if session.get("Role") == "admin":
            return redirect(
                url_for("teacher"),
            )
        else:

            # name=session['Name']
            return redirect(url_for("student"))

    if request.method == "POST":
        Enrollment = request.form.get("name")
        password = request.form.get("password")
        if Enrollment and password:
            u = authenticate_user(Enrollment, password)
            # print(u)
            if u == None:

                flash("Invalid Username or Password !!", "warning")
                return render_template("login.html")
            else:
                session["Name"] = u[0]
                session["Role"] = u[1]
                session.permanent = True
                if u[1] == "student":
                    return redirect(url_for("student"))
                elif u[1] == "admin":
                    return redirect(url_for("teacher"))
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # if 'Name' in session:
    #     return redirect(url_for('index'))
    if request.method == "POST":
        name = request.form.get("name")
        Enrollment = request.form.get("Enrollment")
        email = request.form.get("email")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")
        phone = request.form.get("Phone")
        address = request.form.get("address")
        if password != cpassword:
            flash("Password and Confirm Password do not match !!", "warning")
            return redirect(url_for("register"))
        add_student(name, Enrollment, email, password, phone, address)
        flash("Registration Successful !!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    if "Name" not in session:
        return redirect(url_for("login"))
    role = session["Role"]
    if role == "admin":
        name = session["Name"]
        allstd, columns = all_student()
        classname = get_subject_by_current_day_and_time()
        # result = mycursor.fetchall()  # or .fetchone()

        # print(classname)
        if classname:
            return render_template(
                "teacherprofile.html",
                classname=classname,
                columns=columns,
                data=allstd,
                Name=name,
            )
        else:
            # return render_template('teacherprofile.html')
            return render_template(
                "teacherprofile.html",
                classname=classname,
                columns=columns,
                data=allstd,
                Name=name,
            )
    return redirect(url_for("login"))


# ====================================
# TODO: SUBJECT Save kar raha hai but show nahi kar raha
# ====================================


@app.route("/subject", methods=["GET", "POST"])
def subject():
    if "Name" not in session:
        return redirect(url_for("login"))
    role = session["Role"]
    if role == "admin":
        # name=session["Name"]
        if request.method == "POST":
            subjectcode = request.form.get("subjectcode")
            Stime = request.form.get("Stime")
            Etime = request.form.get("Etime")
            day = request.form.get("day")
            status = add_subject(subjectcode, Stime, Etime, day)
            if status == True:
                flash("Subject Added Successfully !!", "success")
            elif status == "subject_not_found":
                flash("Subject Code Not Found !!", "danger")
            elif status == "duplicate_entry":
                flash(
                    "Duplicate Entry: Subject already exists for the given day !!",
                    "warning",
                )
            else:
                flash("An error occurred while adding the subject !!", "danger")

        try:
            connection = connect_db()
            if connection:
                mycursor = connection.cursor()
                mycursor.execute("SELECT * FROM schedule")
                schedules = mycursor.fetchall()
                print(schedules)
                # return schedules
        except Error as e:
            print(f"Error fetching schedules: {e}")
            # return None
        finally:
            close_db(connection)

        return render_template("subject.html", schedules=schedules)
    return redirect(url_for("login"))


# @app.route("/register_student", methods=["GET", "POST"])
# def register_student_route():
#     if "Name" not in session:
#         return redirect(url_for("login"))
#     role = session["Role"]
#     if role == "admin":
#         if request.method == "POST":
#             enrollment_no = request.form.get("enrollment_no")
#             session["enrollment_no"] = enrollment_no
#             abc = one_student(enrollment_no)
#             print(abc[4])
#             # if False:
#             if abc[4] != None:
#                 flash("Enrollment Number already Have RFID !!", "danger")
#                 # return redirect(url_for("register_student_route"))
#             else:

#                 # flash("Please scan the RFID tag.", "success")
#                 status = read_rfid_from_arduino()
#                 if status == "duplicate_entry":
#                     flash("RFID tag already registered !!", "danger")
#                 # elif status:
#                 flash("RFID tag registered successfully !!", "success")
#                 # else:
#                 #     flash("Error registering RFID tag !!", "danger")
#                 session.pop("enrollment_no", None)

#                 print(f"Enrollment number: {enrollment_no}")
#                 # flash("Enrollment Number Stored", "success")
#                 return render_template("registerrfid.html")
#     return render_template("registerrfid.html")


def generate_pdf(rows):
    # Initialize PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=8)

    # Add title to the PDF
    pdf.cell(200, 10, txt="Database Table Data", ln=True, align="C")
    pdf.ln(10)
    connection = connect_db()
    cursor = connection.cursor()

    # Query to fetch data (adjust to your table)
    query = "SELECT * FROM registration"
    cursor.execute(query)
    # Get column headers dynamically from the rows
    if rows:
        headers = [
            i[0] for i in cursor.description
        ]  # Get column names from the first row

        # Remove the column with index 5 (6th column)
        headers = [header for idx, header in enumerate(headers) if idx != 5]

        # Add table headers, excluding the 6th column
        column_width = 30
        for header in headers:
            pdf.cell(column_width, 10, header, border=1, align="C")
        pdf.ln()

        # Add table rows, excluding the 6th column (index 5)
        for row in rows:
            row = [
                item for idx, item in enumerate(row) if idx != 5
            ]  # Remove the 6th column value
            for item in row:
                pdf.cell(column_width, 10, str(item), border=1, align="C")
            pdf.ln()  # Ensure each row starts on a new line

    # Save the PDF to a file
    pdf_file = "table_data.pdf"
    pdf.output(pdf_file)

    return pdf_file


# Route to generate and download the PDF
@app.route("/download")
def download_pdf():
    # Connect to the database
    connection = connect_db()
    cursor = connection.cursor()

    # Query to fetch data (adjust to your table)
    query = "SELECT * FROM registration"
    cursor.execute(query)
    rows = cursor.fetchall()
    # for i in rows:
    # print(i)

    # Check if rows exist
    if not rows:
        return "No data available to generate PDF."

    # Generate PDF and save to file
    pdf_file = generate_pdf(rows)

    # cursor.close()
    # connection.close()

    # Send the generated PDF as a response for download
    return send_file(
        pdf_file,
        as_attachment=True,
        download_name="table_data.pdf",
        mimetype="application/pdf",
    )


@app.route("/search", methods=["GET", "POST"])
def search():
    if "Name" not in session:
        return redirect(url_for("login"))
    role = session["Role"]
    if role == "admin":
        try:
            if request.method == "POST":
                Enrollment = request.form.get("Enrollment")
                combined = []
                if Enrollment:
                    search = one_student(Enrollment)
                    connection = connect_db()
                    mycursor = connection.cursor()
                    mycursor.execute("SHOW COLUMNS FROM registration")
                    columns = [column[0] for column in mycursor.fetchall()]
                    if not search:
                        flash(f"Not Found Enrollment {Enrollment}")
                        return redirect(url_for("search"))
                    combined = zip(columns, search)
                    return render_template("search.html", combined=combined)
        except KeyError:
            print("Error: 'name' field is missing in the form data")
            return "<h1>Form data error</h1>"
        except Error as e:
            print(f"Error: {e}")
            print(f"Error processing form data: {e}")
            return "<h1>Internal Server Error</h1>"
    return render_template("search.html")


@app.route("/index", methods=["GET", "POST"])
def index():
    if "Name" not in session:
        return redirect(url_for("login"))
    allstd, columns = all_student()
    search = None
    combined = []
    if request.method == "POST":
        try:
            name = request.form.get("name")
            search = one_student(name)
            if not search:
                flash(f"Not Found Name {name}")
                return redirect(url_for("index"))
            combined = zip(columns, search)
        except KeyError:
            print("Error: 'name' field is missing in the form data")
            return "<h1>Form data error</h1>"
        except Error as e:
            print(f"Error processing form data: {e}")
            return "<h1>Internal Server Error</h1>"
    return render_template(
        "index.html", columns=columns, data=allstd, combined=combined, search=search
    )


@app.route("/student", methods=["GET", "POST"])
def student():
    if "Name" not in session:
        return redirect(url_for("login"))
    # one=one_student()
    name = session["Name"]
    # print(name)
    connection = connect_db()
    mycursor = connection.cursor()
    mycursor.execute("SELECT Enrollment_NO FROM registration WHERE name=%s", (name,))
    s = mycursor.fetchone()
    # print(s)
    en = str(s[0])
    # print(en)
    one = one_student(en)
    connection = connect_db()
    mycursor = connection.cursor()
    mycursor.execute("SHOW COLUMNS FROM registration")
    columns = [column[0] for column in mycursor.fetchall()]
    # cone=one.capitalize()
    # print(columns)

    return render_template("studentProfile.html", one=one, columns=columns, zip=zip)


@app.route("/logout")
def logout():
    session.pop("Name", None)
    return redirect(url_for("login"))


@app.route("/update", methods=["GET", "POST"])
def update_password_route():
    if request.method == "POST":
        password = request.form["current_password"]
        name = request.form["name"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        if new_password != confirm_password:
            return "<h1>New passwords do not match</h1>"
        user = one_student(name)
        # print(user)
        if user and check_password_hash(user[5], password):
            # update_password(name, new_password)
            return "<h1>Password updated successfully</h1>"
        else:
            return "<h1>Current password is incorrect</h1>"

    return render_template("updatw.html")


@app.route("/session_data")
def session_data():
    if "Name" not in session:
        return redirect(url_for("login"))

    session_items = {key: session[key] for key in session}
    return render_template("session.html", session_items=session_items)


# if __name__ == "__main__":
# app.run(debug=True)
