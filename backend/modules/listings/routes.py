from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from modules.listings import service

listings_bp = Blueprint("listings", __name__, url_prefix="/applications")


@listings_bp.get("/")
@login_required
def home(): 
    data = service.list_applications(
        user_id=current_user.id, 
        view="home",
        query=None,
        sort=request.args.get("sort", "deadline_asc"), 
        page=request.args.get("page", "1"),
        per_page=request.args.get("per_page", "10")
    )

    return render_template(
        "internship/apply.html",
        internships=data["items"], 
        query=data["query"], 
        sort=data["sort"],
        page=data["page"],
        per_page=data["per_page"],
        total=data["total"],
        total_pages=data["total_pages"],
        sort_options=service.allowed_sort_options()
    )

@listings_bp.get("/applied")
@login_required
def list_applications():
    data = service.list_applications(
        user_id=current_user.id,
        view="applied",
        query=request.args.get("q", ""),
        sort=request.args.get("sort", "deadline_asc"),
        page=request.args.get("page", "1"),
        per_page=request.args.get("per_page", "10"),
    )

    return render_template(
        "internship/applied.html",
        internships=data["items"],
        query=data["query"],
        sort=data["sort"],
        page=data["page"],
        per_page=data["per_page"],
        total=data["total"],
        total_pages=data["total_pages"],
        sort_options=service.allowed_sort_options(),
    )

@listings_bp.get("/apply")
def list_not_applied_applications():
    data = service.list_applications(
        user_id=current_user.id,
        view="apply",
        query=request.args.get("q", ""),
        sort=request.args.get("sort", "deadline_asc"),
        page=request.args.get("page", "1"),
        per_page=request.args.get("per_page", "10"),
    )

    return render_template(
        "internship/apply.html",
        internships=data["items"],
        query=data["query"],
        sort=data["sort"],
        page=data["page"],
        per_page=data["per_page"],
        total=data["total"],
        total_pages=data["total_pages"],
        sort_options=service.allowed_sort_options(),
    )

@listings_bp.get("/search")
@login_required
def search():
    data = service.list_applications(
        user_id=current_user.id,
        view="search",
        query=request.args.get("q", ""),
        sort=request.args.get("sort", "deadline_asc"),
        page=request.args.get("page", "1"),
        per_page=request.args.get("per_page", "10"),
    )

    return render_template(
        "internship/search.html",
        internships=data["items"],
        query=data["query"],
        sort=data["sort"],
        page=data["page"],
        per_page=data["per_page"],
        total=data["total"],
        total_pages=data["total_pages"],
        sort_options=service.allowed_sort_options(),
    )