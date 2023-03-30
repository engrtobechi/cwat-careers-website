import re
import time
import sqlite3
from functools import wraps
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, url_for, flash, redirect, abort, jsonify, session, logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'add your key here'

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def fetch_jobs():
    conn = get_db_connection()
    jobs_fetched = conn.execute("SELECT * FROM jobs").fetchall()
    conn.close()
    return jobs_fetched

def get_job_by_id(id):
    conn = get_db_connection()
    job = conn.execute("SELECT * FROM jobs WHERE id=?", (id,)).fetchone()
    conn.close()
    return job

# Define the function to control user roles
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, please login.", "danger")
            return redirect(url_for("login"))
        
    return wrap

@app.route("/")
def index():
    jobs_fetched = fetch_jobs()
    return render_template("index.html", jobs=jobs_fetched)

@app.route("/api/jobs/<id>/")
def jsonify_jobs(id):
    job = get_job_by_id(id)
    if job:
        return jsonify(dict(job))
    else:
        return jsonify({"message":"Not found"})

@app.route("/jobs/<id>/")
def jobs_item_page(id):
    job = get_job_by_id(id)
    if job:
        return render_template("jobpage.html", job=job)
    else:
        abort(404)

@app.route('/job/<id>/apply', methods=("POST",))
def apply_to_job(id):
    job = get_job_by_id(id)
    if not job:
        abort(404)

    data = request.form
    if not data.get('first_name'):
        flash("First name is required!")
    elif not data.get('email'):
        flash("Email is required!")
    else:
        conn = get_db_connection()
        conn.execute("INSERT INTO applications (job_id, first_name, last_name, email, linkedin_url, education, work_experience, resume_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (id, data['first_name'], data['last_name'], data['email'], data['linkedin_url'], data['education'], data['work_experience'], data['resume_url']))
        conn.commit()
        conn.close()

        return render_template("application_submitted.html", job=job, first_name=data['first_name'], last_name=data['last_name'])


# Add a new route to the Flask application to handle the user signup form.
@app.route("/signup/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Handle form submission
        username = request.form.get("username")
        raw_password = request.form.get("password")
        email = request.form.get("email")
        joined_at = time.time()

        # Validate the data
        if not username or not raw_password or not email:
            flash("All fields are required!")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Please enter a valid email address!")
        else:
            # Hash paswword
            password = sha256_crypt.hash(raw_password)
            # Create the user
            conn = get_db_connection()
            try:
                conn.execute("INSERT INTO 'users' (username, password, email, joined_at) VALUES (?, ?, ?, ?)",
                        (username, password, email, joined_at))
                conn.commit()
                flash("You have successfully registered!")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("The email address is already in use!", "danger")
            conn.close()
    return render_template("signup.html")


# Add a new route to the Flask application to handle the user login form.
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle form submission
        username = request.form["username"]
        password_supplied = str(request.form["password"])

        # Check if the user exists
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM 'users' WHERE username=?",
                [username]).fetchone()
        
        conn.close()

        if user is not None:

            password = user["password"]
            app.logger.info(password)
            app.logger.info(password_supplied)
            # Validate the data
            if sha256_crypt.verify(password_supplied, password):

                # Log the user in
                session["logged_in"] = True
                session["username"] = username

                flash("You are now logged in.", "success")
                return redirect(url_for("dashboard"))
            else:
                app.logger.info("I got here.")
                flash("Invalid username or password")
                return redirect(url_for("login"))

        else:
            error = "Username does not exist"
            return render_template("login.html", error=error)

    return render_template("login.html")

# Logout route
@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You are now logged out", "success")
    return redirect(url_for("index"))

# Add a new route to the Flask application to handle the user dashboard page.
@app.route("/dashboard/")
@login_required
def dashboard():
    # Fetch the user's applications
    #conn = get_db_connection()
    #applications = conn.execute("SELECT * FROM 'Applications' WHERE user_id=?", (session["user_id"],)).fetchall()
    #conn.close()

    return render_template("dashboard.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug="True")
