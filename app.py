import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort, jsonify

app = Flask(__name__)
# Create a secret key for client browser sessions
app.config['SECRET_KEY'] = 'add your key here'

def get_db_connection():
    # Open connection to the database.db
    conn = sqlite3.connect("database.db")
    # Create a dictionary cursor instead of the default tuple
    conn.row_factory = sqlite3.Row
    return conn

def fetch_jobs():
    # Call the get_db_connection method we defined above
    conn = get_db_connection()

    # Fetch all the data in the posts table
    jobs_fetched = conn.execute("SELECT * FROM jobs").fetchall()
    # Close the database connection
    conn.close()

    return jobs_fetched

# Definning our route
@app.route("/")
def index():

    jobs_fetched = fetch_jobs()

    # Using the render_template function from flask we render a html template as well as pass in data
    return render_template("index.html", jobs=jobs_fetched)

# Let's create our portal api
@app.route("/api/jobs/<id>/")
def jsonify_jobs(id):

    jobs_fetched = fetch_jobs()

    # Create a list to hold jobs which will be pass in rows to the jsonify function
    json_list = []
    for job in jobs_fetched:
        json_list.append(job)

    if int(id)-1 > len(jobs_fetched):
        return jsonify({"message":"Not found"})
    else:
        return jsonify(dict(json_list[int(id)-1]))

# Let's create a route for generating dynamic pages for each job
@app.route("/jobs/<id>/")
def jobs_item_page(id):

    jobs_fetched = fetch_jobs()

    # Create a list to hold jobs which will be pass in rows to the jsonify function
    job_list = []
    for job in jobs_fetched:
        job_list.append(job)

    if int(id)-1 > len(jobs_fetched):
        return "Not found", 404
    else:
        return render_template("jobpage.html", job=job_list[int(id)-1])

# This block of code ensures that app.py starts the server when run
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug="True")