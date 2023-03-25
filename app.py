from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [
    {
        "id": 1,
        "title": "Electronics Engineer - Entry Level",
        "location": "Enugu, Nigeria",
        "salary": "NGN150,000"
    },
    
    {
        "id": 2,
        "title": "Production Engineer - Intermediate Level",
        "location": "Enugu, Nigeria",
        "salary": "NGN350,000"
    },

    {
        "id": 3,
        "title": "Sales Manager - Advanced Level",
        "location": "Enugu, Nigeria",
        "salary": "NGN400,000"
    },

    {
        "id": 4,
        "title": "Backend Engineer - Intermediate Level",
        "location": "Remote and On-site, Enugu, Nigeria"
    }
    
]

# Definning our route
@app.route("/")
def hello_world():

    # Using the render_template function from flask we render a html template as well as pass in data
    return render_template("home.html", jobs=JOBS)

# Let's create our portal api
@app.route("/api/jobs")
def list_jobs():
    return jsonify(JOBS)

# Running the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug="True")