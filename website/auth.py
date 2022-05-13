from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .forms import UserForm
from flask_login import login_user, login_required, logout_user, current_user

import json


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Log in user if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password.", category="error")
        else:
            flash("No user with that e-mail exists.", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Check if user already exists and validate information
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Användare med den e-postadressen existerar redan.", category="error")

        elif password1 != password2:
            flash("Lösenord matchar inte.", category="error")

        else:
            # Creat new user
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password1, method="sha256"),
            )

            # Save user to database
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created.", category="success")

            # Render home page after creating user
            return redirect(url_for("views.home"))

    form = UserForm()
    return render_template("sign_up.html", user=current_user, form=form)


@auth.route("/delete-user", methods=["POST"])
@login_required
def delete_user():
    user = json.loads(request.data)
    user_id = user["userId"]
    user_to_delete = User.query.get(user_id)


    # Delete user if not trying to delete one self
    if user_to_delete:
        if user_to_delete.id == current_user.id:
            flash("Du kan inte radera dig själv!", category="error")
        else:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash(f"Användare {user_to_delete.id} är raderad.", category="success")

    return jsonify({})
