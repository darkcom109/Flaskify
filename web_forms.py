from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

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

class UpdateForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    bio = StringField("Profile Description", validators=[DataRequired()])
    aspiring_job = StringField("Aspiring Position")
    profile_pic = FileField("Profile Pic")
    submit = SubmitField("Submit")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")
