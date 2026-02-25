from flask import Blueprint, render_template, redirect,request, url_for,flash
from flask_login import login_required, current_user
from . import service
from modules import listings

applications_bp = Blueprint("applications", __name__, url_prefix="/applications")


@applications_bp.get("/add")
def create_form():
    return render_template("internship/add.html")

@applications_bp.post("/add")
def create_submit():
    # TODO: insert application into DB
    service.create_application(
        user_id = current_user.id,
        company_name = request.form.get("company"),
        job_title=request.form.get("title"),
        location=request.form.get("location"),
        salary_expectation=request.form.get("salary"),
        application_link=request.form.get("link"),
        deadline=request.form.get("deadline"),
        personal_notes=request.form.get("notes"),
        work_model=request.form.get("work_model"),
        status=request.form.get("status"),
    )
    flash("Application Created Successfully","Success")
    return redirect(url_for("listings.list_applications"))


@applications_bp.get("/<application_id>")
@login_required
def detail(application_id):
    # TODO: fetch application from DB
    application = service.get_application(application_id)
    return render_template("internship/details.html",internship = application)


@applications_bp.get("/<application_id>/edit")
@login_required
def edit_form(application_id):
    # TODO: fetch application for editing
    application = service.get_application(application_id)
    return render_template("internship/edit_intern.html", internship= application)


@applications_bp.post("/<application_id>/edit")
@login_required
def edit_submit(application_id):
     # TODO: update application in DB
    updates = {
        "company_name": request.form.get("company"),
        "job_title": request.form.get("title"),
        "location": request.form.get("location"),
        "salary_expectation": request.form.get("salary"),
        "application_link": request.form.get("link"),
        "work_model": request.form.get("work_model"),
        "deadline": request.form.get("deadline"),
        "personal_notes": request.form.get("notes"),
        "status": request.form.get("status"),
    }
    service.update_application(application_id,updates)
    flash("Application updated Successfully","success")
    return redirect(url_for("listings.list_applications"))

@applications_bp.post("/<application_id>/delete")
@login_required
def delete(application_id):
    # TODO: delete application from DB
    service.delete_application(application_id)
    flash("Application Deleted Succesfully","Success")
    return redirect(url_for("listings.list_applications"))
