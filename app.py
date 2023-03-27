import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort, jsonify

app = Flask(__name__)
# Create a secret key for client browser sessions
app.config['SECRET_KEY'] = 'eSQ92-2i23#As1985/1'

def get_db_connection():
    # Open connection to the database.db
    conn = sqlite3.connect("database.db")
    # Create a dictionary cursor instead of the default tuple
    conn.row_factory = sqlite3.Row
    return conn



# Definning our route
@app.route("/")
def hello_world():

    # Call the get_db_connection method we defined above
    conn = get_db_connection()

    # Fetch all the data in the posts table
    jobs_fetched = conn.execute("SELECT * FROM jobs").fetchall()
    # Close the database connection
    conn.close()

    # Using the render_template function from flask we render a html template as well as pass in data
    return render_template("home.html", jobs=jobs_fetched)

# Let's create our portal api
@app.route("/api/jobs")
def list_jobs():
    return jsonify(JOBS)

# This block of code ensures that app.py starts the server when run
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug="True")