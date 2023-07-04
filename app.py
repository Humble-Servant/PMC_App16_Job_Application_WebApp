from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date_avail = request.form["date_avail"]
        occupation = request.form["occupation"]
        # print(f"{last_name}, {first_name}  {email}")
        # print(f"Date available: {date_avail}")
        # print(f"Occupation: {occupation}")
    return render_template("index.html")

app.run(debug=True, port=5001)
