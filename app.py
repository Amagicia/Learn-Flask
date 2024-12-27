from flask import Flask, flash, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
from datetime import timedelta
from modules import *
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '12688fuy234y512cy5c12ucf'  # Secret key for session management
app.permanent_session_lifetime = timedelta(minutes=10)  # Set session lifetime to 7 days


@app.route("/", methods=["GET", "POST"])
def login():
    # print("login")
    if 'Enrollment' in session:
        return redirect(url_for('index'))
    if request.method == "POST":
        Enrollment = request.form.get("name")
        password = request.form.get("password")
        if Enrollment and password and check_name_pass(Enrollment, password):
            session['Enrollment'] = Enrollment
            session['username'] = one_student(Enrollment)[0]
            session.permanent = True  # Make the session permanent
            flash('Login Successful !!', 'success')  # Flash message for successful login
          
            return redirect(url_for('index'))
        else:
            flash('Invalid Username or Password !!', 'warning')  # Flash message for unauthorized access

            return redirect(url_for('login'))
            # return "<h1>Invalid credentials</h1>"
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if 'Enrollment' in session:
        return redirect(url_for('index'))
    if request.method == "POST":
        name = request.form.get("name")
        Enrollment = request.form.get("Enrollment")
        email = request.form.get("email")
        password = request.form.get("password")
        cpassword=request.form.get("cpassword")
        phone=request.form.get("Phone")
        address=request.form.get("address")
        if password != cpassword:
            flash('Password and Confirm Password do not match !!', 'warning')
            return redirect(url_for('register'))
        add_student(name, Enrollment, email, password,phone,address)
        flash('Registration Successful !!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html")
@app.route("/search", methods=["GET", "POST"])
def search():
    if 'Enrollment' not in session:
        return redirect(url_for('login'))
    try:
        if request.method == "POST":
            Enrollment = request.form.get("Enrollment")
            combined=[]
            if Enrollment:
                search = one_student(Enrollment)
                connection=connect_db()
                mycursor = connection.cursor()
                mycursor.execute("SHOW COLUMNS FROM registration")
                columns = [column[0] for column in mycursor.fetchall()]
                # print(search)
                # print(columns)
                # if search:
                if not search:
                    flash (f"Not Found Enrollment {Enrollment}")
                    return redirect(url_for('search'))
                combined = zip(columns,search)
                print(12333333,combined)

                # pr
                return render_template("search.html", combined=combined)
    except KeyError:
            # print("Error: 'name' field is missing in the form data")
        return "<h1>Form data error</h1>"
    except Error as e:
            # print(f"Error processing form data: {e}")
        return "<h1>Internal Server Error</h1>"
    return render_template("search.html")
    # return rendallstd, columns = all_student()
#     search = None
#     combined = []
    
#     if request.method == "POST":
#         try:
#             name = request.form.get("name")
#             search = one_student(name)
#             if not search:
#                 flash (f"Not Found Name {name}")
#                 return redirect(url_for('index'))
#             print(allstd)
#             combined = zip(columns,search)

#         except KeyError:
#             print("Error: 'name' field is missing in the form data")
#             return "<h1>Form data error</h1>"
#         except Error as e:
#             print(f"Error processing form data: {e}")
#             return "<h1>Internal Server Error</h1>"
#     return render_template("index.html", columns=columns, data=allstd,combined=combined, search=search)

# er_template("search.html")
        
        
        
        
        
        
        

@app.route("/index", methods=["GET", "POST"])
def index():
    if 'Enrollment' not in session:
        return redirect(url_for('login'))
    
    allstd, columns = all_student()
    search = None
    combined = []
    
    if request.method == "POST":
        try:
            name = request.form.get("name")
            search = one_student(name)
            if not search:
                flash (f"Not Found Name {name}")
                return redirect(url_for('index'))
            # print(allstd)
            combined = zip(columns,search)

        except KeyError:
            # print("Error: 'name' field is missing in the form data")
            return "<h1>Form data error</h1>"
        except Error as e:
            # print(f"Error processing form data: {e}")
            return "<h1>Internal Server Error</h1>"
    return render_template("index.html", columns=columns, data=allstd,combined=combined, search=search)



@app.route("/logout")
def logout():
    session.pop('Enrollment', None)
    return redirect(url_for('login'))
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
        if user and check_password_hash(user[5],password):  # Adjust the index if necessary
        # if user :  # Adjust the index if necessary
            update_password(name, new_password)
            return "<h1>Password updated successfully</h1>"
        else:
            return "<h1>Current password is incorrect</h1>"
    
    return render_template("updatw.html")

@app.route("/session_data")
def session_data():
    if 'Enrollment' not in session:
        return redirect(url_for('login'))
    
    session_items = {key: session[key] for key in session}
    return render_template("session.html", session_items=session_items)

if __name__ == "__main__":
    app.run(debug=True)