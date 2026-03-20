from flask import Flask, render_template, request, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import secret
from flask_mail import Mail, Message

app = Flask(__name__) # this is the instance of the Flask app


# config files for db and email
app.config['SECRET_KEY'] = secret.SECRET_KEY # hackers would need this key to get in.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # data will be the name of the file we create
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = secret.EMAIL_KEY
app.config['MAIL_PASSWORD'] = secret.PASSWORD_KEY
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
db = SQLAlchemy(app)

mail = Mail(app)

# this class defines the form fields, sets parameters
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))

# this connects to the frontend web page - allowing for both get and post
# stores the inputs in the variables.
@app.route("/", methods=["GET", "POST"]) # if you just use "/" it knows it is your home page
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        # store the inputs in 'form', write to db table, and email, and send message
        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        message_body = (f"Thank you for your submission, {first_name}.\""
                        f"Here is what you submitted:\n"
                        f"{first_name}\n"
                        f"{last_name}\n"
                        f"{email}\n"
                        f"{date_obj}\n"
                        f"{occupation}\n"
                        f"Thank you.")

        message = Message("New Job Form Submitted",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        mail.send(message)
        flash(f"{first_name}, your message was submitted successfully!", "success")

    # this renders the HTML template on the frontend
    return render_template("index.html")

# running the app, create db, allow debugging, define port
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5000)