from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"

# Secret key
app.config['SECRET_KEY'] = os.getenv("FORM_SECRET_KEY", "dev-secret")

# Initialise database
db = SQLAlchemy(app)

# Create User Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))

# Initialise LoginManager
login_manager = LoginManager(app)

login_manager.login_view = "login"
login_manager.login_message_category = "info"

# Create a sign-up form class
class SignUpForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a login form class
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("login"))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        hashed_pw = generate_password_hash(
            form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )

        user = Users(
            name=form.name.data, 
            email=form.email.data, 
            password=hashed_pw
        )
        
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    
    return render_template("signup.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Login failed. Check your username or password")
        
    return render_template("login.html", form=form)

@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", current_user=current_user)

@app.route('/dashboard/lesson_zero')
@login_required
def lesson_zero():
    return render_template("/lessons/lesson_zero.html")

@app.route('/dashboard/lesson_one')
@login_required
def lesson_one():
    return render_template("/lessons/lesson_one.html")

@app.route('/dashboard/lesson_two')
@login_required
def lesson_two():
    return render_template("/lessons/lesson_two.html")

@app.route('/dashboard/lesson_three')
@login_required
def lesson_three():
    return render_template("/lessons/lesson_three.html")

@app.route('/dashboard/lesson_four')
@login_required
def lesson_four():
    return render_template("/lessons/lesson_four.html")

@app.route('/dashboard/lesson_five')
@login_required
def lesson_five():
    return render_template("/lessons/lesson_five.html")

@app.route('/dashboard/lesson_six')
@login_required
def lesson_six():
    return render_template("/lessons/lesson_six.html")

@app.route('/dashboard/project_one')
@login_required
def project_one():
    return render_template("/lessons/project_one.html")

if __name__ == "__main__":
    app.run(debug=True)