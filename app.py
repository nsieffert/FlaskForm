from flask import Flask, render_template, request, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # this is the instance of the Flask app

app.config['SECRET_KEY'] = 'mygreatapp100' # hackers would need this key to get in.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # data will be the name of the file we create
db = SQLAlchemy(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=["GET", "POST"]) # if you just use "/" it knows it is your home page
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        form = Form(first_name=first_name, last_name=last_name, email=email, date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()
        flash(f"{first_name}, your message was submitted successfully!", "success")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)

app.run(debug=True, port=5000)