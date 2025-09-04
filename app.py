from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"

# Secret key
app.config['SECRET_KEY'] = os.getenv("FORM_SECRET_KEY")

# Initialise database
db = SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))

# Create a sign-up form class
class SignUpForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a login form class
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    name = None
    form = SignUpForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data

        form.name.data = ''
        form.email.data = ''
        form.password.data = ''
    return render_template("signup.html", form=form, name=name)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)