from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String, unique=True, nullable=False)
    fullname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String, nullable=False)
    report_type = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default="Active")
    location = db.Column(db.String, nullable=False)
    date_reported = db.Column(db.Date, nullable=False)
    contact_info = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)