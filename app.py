from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_mail import Mail, Message


PASSWORD = os.getenv('PASSWORD')

app = Flask(__name__)

app.config['SECRET_KEY'] = "r!GrH9X9$4_@AwgQUTqafA3qSG_t-m9NjA6r_Qn-Gk_GWdWswBFQB!8VE7CAg@NC"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
# app.config['MAIL_PORT'] = 465  # For use with SSL
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "darrellswarner@gmail.com"
app.config['MAIL_DEFAULT_SENDER'] = "darrellswarner@gmail.com"
app.config['MAIL_PASSWORD'] = PASSWORD

db = SQLAlchemy(app)
mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date_avail = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date_avail"]
        date_avail = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]
        
        form = Form(first_name=first_name, last_name=last_name, email=email, date_avail=date_avail,
                    occupation=occupation)
        db.session.add(form)
        db.session.commit()
        flash(f"{first_name}, your form was submitted successfully!", "success")
        message_body = f"Thank you for your submission, {first_name}.\n\n" \
                       f"Here is what you submitted:\n" \
                       f"{last_name}, {first_name}\n{email}\nDate available: {date}\nOccupation: {occupation}\n\n" \
                       f"Thank you again!  We will be in touch shortly.\n\nVery Respectfully,\nHR"
        message = Message(subject="Form Submission",
                          recipients=[email],
                          body=message_body)
        mail.send(message)
        
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
