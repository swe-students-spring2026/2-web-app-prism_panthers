from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from modules.auth_profile import service

auth_profile_bp = Blueprint("auth_profile", __name__)


# ── Authentication ──────────────────────────────────────

@auth_profile_bp.get("/login")
def login():
    return render_template("auth/login.html")


@auth_profile_bp.post("/login")
def login_submit():
    email = request.form["email"]
    password = request.form["password"]

    user = service.authenticate(email, password)
    if user:
        login_user(user)
        return redirect(url_for("auth_profile.view_profile"))

    flash("Invalid credentials", "danger")
    return redirect(url_for("auth_profile.login"))


@auth_profile_bp.get("/register")
def register():
    return render_template("auth/register.html")


@auth_profile_bp.post("/register")
def register_submit():
    ok, msg = service.register(
        request.form["email"],
        request.form["password"],
        request.form["confirm_password"],
    )
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("auth_profile.login") if ok else url_for("auth_profile.register"))


@auth_profile_bp.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_profile.login"))


@auth_profile_bp.get("/forgot-password")
def forgot_password():
    return render_template("auth/forgot_password.html")


@auth_profile_bp.post("/forgot-password")
def forgot_password_submit():
    email = request.form["email"]
    token = service.request_password_reset(email)

    reset_link = None
    if token:
        reset_link = url_for("auth_profile.reset_password", token=token, _external=True)

    flash("If that email exists, a reset link has been sent.", "success")
    return render_template("auth/forgot_password.html", reset_link=reset_link)


@auth_profile_bp.get("/reset-password/<token>")
def reset_password(token):
    return render_template("auth/update_password.html", token=token)


@auth_profile_bp.post("/reset-password/<token>")
def reset_password_submit(token):
    ok, msg = service.reset_password(
        token,
        request.form["new_password"],
        request.form["confirm_password"],
    )
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("auth_profile.login") if ok else url_for("auth_profile.reset_password", token=token))


# ── Profile ─────────────────────────────────────────────

@auth_profile_bp.get("/profile")
@login_required
def view_profile():
    from extensions import db as mongo_db

    user = service.get_profile(current_user.id)
    internships = mongo_db["internships"]
    uid = current_user.id

    total = internships.count_documents({"user_id": uid})
    interviews = internships.count_documents({"user_id": uid, "status": "Interviewing"})
    offers = internships.count_documents({"user_id": uid, "status": "Offer"})
    rejected = internships.count_documents({"user_id": uid, "status": "Rejected"})

    return render_template(
        "profile/profile.html",
        user=user,
        total=total,
        interviews=interviews,
        offers=offers,
        rejected=rejected,
    )


@auth_profile_bp.get("/profile/edit")
@login_required
def edit_profile():
    user = service.get_profile(current_user.id)
    return render_template("profile/edit_profile.html", user=user)


@auth_profile_bp.post("/profile/edit")
@login_required
def edit_profile_submit():
    ok, msg = service.update_profile(current_user.id, dict(request.form))
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("auth_profile.view_profile"))

<<<<<<< HEAD
@auth_profile_bp.get("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("auth_profile.view_profile"))
    return redirect(url_for("auth_profile.login"))
=======

@auth_profile_bp.get("/profile/update-password")
@login_required
def update_password():
    return render_template("auth/update_password.html")


@auth_profile_bp.post("/profile/update-password")
@login_required
def update_password_submit():
    ok, msg = service.change_password(
        current_user.id,
        request.form["current_password"],
        request.form["new_password"],
        request.form["confirm_password"],
    )
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("auth_profile.view_profile") if ok else url_for("auth_profile.update_password"))


@auth_profile_bp.get("/profile/delete")
@login_required
def delete_profile():
    return render_template("profile/delete_profile.html")


@auth_profile_bp.post("/profile/delete")
@login_required
def delete_profile_submit():
    service.delete_account(current_user.id)
    logout_user()
    flash("Your account has been deleted.", "warning")
    return redirect(url_for("auth_profile.login"))

>>>>>>> af46af77b2400c37da764ff75089d352587353a9
