from flask import Blueprint, render_template, redirect, url_for


applications_bp = Blueprint("applications", __name__, url_prefix="/applications")


@applications_bp.get("/new")
def create_form():
    return render_template("internship/add.html")


@applications_bp.post("/new")
def create_submit():
    # TODO: insert application into DB
    return redirect(url_for("listings.list_applications"))


@applications_bp.get("/<application_id>")
def detail(application_id):
    # TODO: fetch application from DB
    return "Not implemented", 501


@applications_bp.get("/<application_id>/edit")
def edit_form(application_id):
    # TODO: fetch application for editing
    return render_template("internship/edit_intern.html", internship={})


@applications_bp.post("/<application_id>/edit")
def edit_submit(application_id):
    # TODO: update application in DB
    return redirect(url_for("applications.detail", application_id=application_id))


@applications_bp.get("/<application_id>/delete")
def delete_confirmation(application_id):
    # TODO: fetch the internship for deletion
    return render_template("internship/delete_internship.html", internship={})

@applications_bp.post("/<application_id>/delete")
def delete(application_id):
    # TODO: delete application from DB
    return redirect(url_for("listings.list_applications"))
