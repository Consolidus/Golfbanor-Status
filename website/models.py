from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

# Course database model
class Golfcourse(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), unique=True)
    course_region = db.Column(db.String(50))
    course_country = db.Column(db.String(50))
    course_status = db.Column(db.String(50))
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    undantag = db.Column(db.String(100))
    competition = db.Column(db.String(20))
    last_update = db.Column(db.Date, default=func.now())
    updated_by = db.Column(db.String(50))
    info_source = db.Column(db.String(50))
    facebook_url = db.Column(db.String(100))
    website_url = db.Column(db.String(100))
    booking_system = db.Column(db.String(100))
    coordinates = db.Column(db.String(40))
    google_maps_url = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


# User database model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    golfcourses = db.relationship("Golfcourse")
