from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from modules.listings import service

listings_bp = Blueprint("listings", __name__, url_prefix="/applications")


@listings_bp.get("/")
@login_required
def list_applications():
    query = request.args.get("q", "")
    sort_by = request.args.get("sort", "deadline")
    applications = service.list_applications(current_user.id, query, sort_by)
    return render_template(
        "internship/applied.html",
        internships=applications,
        query=query,
        sort_by=sort_by,
    )
