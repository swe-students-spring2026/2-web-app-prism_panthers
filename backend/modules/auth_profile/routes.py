from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os

from modules.auth_profile import service

auth_profile_bp = Blueprint("auth_profile", __name__)


# ── Helper functions ────────────────────────────────────

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


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
    # Handle profile picture upload
    profile_data = dict(request.form)
    
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file and file.filename and allowed_file(file.filename):
            # Generate a unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{current_user.id}_{filename}"
            
            # Save the file
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, unique_filename)
            file.save(filepath)
            
            # Store relative path in database
            profile_data['profile_picture'] = f"uploads/profile_pics/{unique_filename}"
        elif file and file.filename and not allowed_file(file.filename):
            flash("Invalid file type. Allowed types: png, jpg, jpeg, gif", "danger")
            return redirect(url_for("auth_profile.edit_profile"))
    
    ok, msg = service.update_profile(current_user.id, profile_data)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("auth_profile.view_profile"))


@auth_profile_bp.post("/profile/remove-picture")
@login_required
def remove_profile_picture():
    user = service.get_profile(current_user.id)
    
    # Delete the file if it exists
    if user and user.get('profile_picture'):
        filepath = os.path.join(current_app.root_path, '..', 'static', user.get('profile_picture'))
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                flash(f"Error deleting file: {str(e)}", "danger")
                return redirect(url_for("auth_profile.edit_profile"))
    
    # Remove the profile picture from database
    from modules.auth_profile import database as db
    db.update_user_profile(current_user.id, {"profile_picture": ""})
    
    flash("Profile picture removed successfully.", "success")
    return redirect(url_for("auth_profile.edit_profile"))


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

@auth_profile_bp.post("/profile/photo-demo")
@login_required
def photo_demo():
    flash("Profile photo updated successfully.", "success")
    return redirect(url_for("auth_profile.edit_profile"))

@auth_profile_bp.post("/profile/resume-demo")
@login_required
def resume_demo():
    flash("Resume updated!", "success")
    return redirect(url_for("auth_profile.view_profile"))

@auth_profile_bp.get("/profile/edit-links")
@login_required
def edit_links():
    user = service.get_profile(current_user.id)
    return render_template("profile/edit_links.html", user=user)

@auth_profile_bp.post("/profile/edit-links")
@login_required
def edit_links_submit():
    ok, msg = service.update_links(current_user.id, dict(request.form))
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("auth_profile.view_profile"))

@auth_profile_bp.get("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("auth_profile.view_profile"))
    return redirect(url_for("auth_profile.login"))

