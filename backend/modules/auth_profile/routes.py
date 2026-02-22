from flask import Blueprint, render_template, redirect, url_for


auth_profile_bp = Blueprint("auth_profile", __name__)


@auth_profile_bp.get("/login")
def login():
    return render_template("auth/login.html")


@auth_profile_bp.post("/login")
def login_submit():
    # TODO: authenticate user
    return redirect(url_for("listings.list_applications"))


@auth_profile_bp.get("/register")
def register():
    return render_template("auth/register.html")


@auth_profile_bp.post("/register")
def register_submit():
    # TODO: create user account
    return redirect(url_for("auth_profile.login"))


@auth_profile_bp.get("/forgot-password")
def forgot_password():
    return render_template("auth/forgot_password.html")


@auth_profile_bp.post("/forgot-password")
def forgot_password_submit():
    # TODO: handle password reset request
    return redirect(url_for("auth_profile.login"))


@auth_profile_bp.get("/update-password")
def update_password():
    return render_template("auth/update_password.html")


@auth_profile_bp.post("/update-password")
def update_password_submit():
    # TODO: update user password
    return redirect(url_for("auth_profile.login"))


@auth_profile_bp.get("/profile")
def view_profile():
    return render_template("profile/profile.html")


@auth_profile_bp.get("/profile/edit")
def edit_profile():
    return render_template("profile/edit_profile.html")


@auth_profile_bp.post("/profile/edit")
def edit_profile_submit():
    # TODO: update user profile in DB
    return redirect(url_for("auth_profile.view_profile"))
