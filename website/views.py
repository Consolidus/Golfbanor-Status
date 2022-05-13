from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Golfcourse
from .forms import GolfcourseForm
from . import db
import datetime as dt

views = Blueprint("views", __name__)

# Color scheme for course status
color_scheme = {
    "ÖPPEN18 (18-hål. Alla ord.spelytor)": "#7CFC00",
    "Okänd/Ej Nyligen Uppdaterad": "#B7B7B7",
    "Öppning Planerad (Se fr.o.m. samt kommentarer)": "#F3F317",
    "Stängd Tillsvidare": "#EA6256",
    "Öppen (Alla hål. Undantag ord.spelytor. Se undantag/kommentarer)": "#B4E594",
    "Delöppen (Ej ord.spelytor. Ej alla hål. Se undantag/kommentarer)": "#CEF5B5",
    "Tillfälligt Stängd": "#FF9900",
    "ÖPPEN9 (9-17-hålsbana. Alla ord.spelytor)": "#73ED50",
    "Endast Drivingrange": "#9900FF",
}


@views.route("/", methods=["GET"])
def home():
    # Load courses from database
    courses = Golfcourse.query.order_by(Golfcourse.course_id).all()

    # Get values for filtering
    statuses = set([course.course_status for course in courses])
    countries = set([course.course_country for course in courses])
    regions = set([course.course_region for course in courses])

    # Render the page
    return render_template(
        "home.html",
        courses=courses,
        user=current_user,
        countries=countries,
        regions=regions,
        statuses=statuses,
        color_scheme=color_scheme,
    )


@views.route("/edit-course", methods=["GET", "POST"])
def edit_course():
    if request.method == "POST":
        course_id = request.form.get("course_id")
        course = Golfcourse.query.filter_by(course_id=course_id).first()

    form = GolfcourseForm()

    return render_template(
        "edit_course.html", course=course, form=form, user=current_user
    )


@views.route("/update-course", methods=["POST"])
def update_course():
    course_id = request.form.get("course_id")
    course_name = request.form.get("course_name")
    course_region = request.form.get("course_region")
    course_country = request.form.get("course_country")
    course_status = request.form.get("course_status")
    from_date = request.form.get("from_date")
    to_date = request.form.get("to_date")
    undantag = request.form.get("undantag")
    competition = request.form.get("competition")
    last_update = request.form.get("last_update")
    updated_by = request.form.get("updated_by")
    info_source = request.form.get("info_source")
    facebook_url = request.form.get("facebook_url")
    website_url = request.form.get("website_url")
    booking_system = request.form.get("booking_system")
    coordinates = request.form.get("coordinates")
    google_maps_url = request.form.get("google_maps_url")

    # Check if dates are valid
    if from_date and from_date != "None":
        try:
            from_date = dt.datetime.strptime(from_date, "%Y-%m-%d")
        except:
            from_date = None
    else:
        from_date = None

    if to_date and to_date != "None":
        try:
            to_date = dt.datetime.strptime(to_date, "%Y-%m-%d")
        except:
            to_date = None
    else:
        to_date = None

    # Load course from database
    course = (
        db.session.query(Golfcourse).filter(Golfcourse.course_id == course_id).one()
    )
    course.course_id = course_id
    course.course_name = course_name
    course.course_region = course_region
    course.course_country = course_country
    course.course_status = course_status
    course.from_date = from_date
    course.to_date = to_date
    course.undantag = undantag
    course.competition = competition
    course.last_update = dt.datetime.now()
    course.updated_by = updated_by
    course.info_source = info_source
    course.facebook_url = facebook_url
    course.website_url = website_url
    course.booking_system = booking_system
    course.coordinates = coordinates
    course.google_maps_url = google_maps_url

    # Update database with new information
    db.session.commit()
    flash("Bana uppdaterad!", category="success")

    # Load the course and render the edit page
    course = Golfcourse.query.filter_by(course_id=course_id).first()
    form = GolfcourseForm()

    return render_template(
        "edit_course.html", course=course, form=form, user=current_user
    )
