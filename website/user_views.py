import datetime as dt
import json
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    jsonify,
    send_file,
    redirect,
    url_for,
)
from flask_login import login_required, current_user
from .models import Golfcourse, User
from .forms import GolfcourseForm
from . import db


user_views = Blueprint("user_views", __name__)


# @login_required
@user_views.route("/add-course", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
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

        # Check if course already exists
        course = Golfcourse.query.filter_by(course_name=course_name).first()
        if course:
            flash("En bana med det namnet existerar redan.", category="error")

        elif len(course_name) < 3:
            flash("Bannamn är för kort.", category="error")
        else:
            new_course = Golfcourse(
                course_id=course_id,
                course_name=course_name,
                course_region=course_region,
                course_country=course_country,
                course_status=course_status,
                from_date=from_date,
                to_date=to_date,
                undantag=undantag,
                competition=competition,
                last_update=last_update,
                updated_by=updated_by,
                info_source=info_source,
                facebook_url=facebook_url,
                website_url=website_url,
                booking_system=booking_system,
                coordinates=coordinates,
                google_maps_url=google_maps_url,
            )

            # Save course to database
            db.session.add(new_course)
            db.session.commit()
            flash("Course added!", category="success")

        # Render home page after creating course
        return redirect(url_for("views.home"))

    # Render page to add course if method is GET
    form = GolfcourseForm()
    return render_template("add_course.html", form=form, user=current_user)


@login_required
@user_views.route("/users")
def users():
    # Load users from database
    all_users = User.query.order_by(User.id).all()

    # Render user page
    return render_template("users.html", user=current_user, all_users=all_users)


@login_required
@user_views.route("/profile")
def profile():
    # Render user profile page
    return render_template("profile.html", user=current_user)


@user_views.route("/update-user", methods=["POST"])
@login_required
def update_user():
    user_id = request.form.get("user_id")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")

    # Validate user information
    if len(email) < 5:
        flash("E-postadressen är inte godkänd.", category="error")

    elif password1 != password2:
        flash("Lösenorden matchar inte.", category="error")

    elif 0 < len(password1) < 6:
        flash("Lösenord måste vara minst 6 tecken.", category="error")

    else:
        user = db.session.query(User).filter(User.id == user_id).one()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if len(password1) > 0:
            user.password = generate_password_hash(password1, method="sha256")

        # Save user to database
        db.session.commit()
        flash("Användare uppdaterad!", category="success")

    return render_template("profile.html", user=current_user)


@user_views.route("/delete-course", methods=["POST"])
@login_required
def delete_course():
    course = json.loads(request.data)
    golfcourseId = course["golfcourseId"]
    course = Golfcourse.query.get(golfcourseId)
    if course:
        if course.user_id == current_user.id or current_user.id == 1:
            db.session.delete(course)
            db.session.commit()

    return jsonify({})
