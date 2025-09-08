from flask_login import UserMixin
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_ckeditor import CKEditor

app = Flask(__name__)
ckeditor = CKEditor(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Blog Post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(999))
    content = db.Column(db.Text)
    author = db.Column(db.String(999))
    date_posted = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    slug = db.Column(db.String(255))
    user_id = db.Column(db.Integer)

# Create User Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    bio = db.Column(db.String(9999), default="Hello, I am using Flaskify!")
    profile_pic = db.Column(db.String(), default="https://static.vecteezy.com/system/resources/previews/036/280/650/large_2x/default-avatar-profile-icon-social-media-user-image-gray-avatar-icon-blank-profile-silhouette-illustration-vector.jpg")
    aspiring_job = db.Column(db.String(9999))