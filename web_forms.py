from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

# Create a sign-up form class
class SignUpForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=1, max=100)])
    email = StringField("Email", validators=[DataRequired(), Length(min=1, max=100)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=1, max=999)])
    submit = SubmitField("Submit")

# Create a login form class
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(min=1, max=100)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=1, max=999)])
    submit = SubmitField("Submit")

class UpdateForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=1, max=100)])
    email = StringField("Email", validators=[DataRequired(), Length(min=1, max=100)])
    bio = StringField("Profile Description", validators=[DataRequired(), Length(min=1, max=200)])
    aspiring_job = StringField("Aspiring Position", default="Flaskify Enthusiast", validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField("Submit")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=1, max=30)])
    content = StringField("Content", validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")
