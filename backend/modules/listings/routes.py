from flask import Blueprint, render_template, request


listings_bp = Blueprint("listings", __name__, url_prefix="/applications")


@listings_bp.get("/")
def list_applications():
    query = request.args.get("q", "")
    sort_by = request.args.get("sort", "deadline")
    applications = []
    return render_template(
        "internship/applied.html",
        internships=applications,
        query=query,
        sort_by=sort_by,
    )
