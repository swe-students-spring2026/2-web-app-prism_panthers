# Listings business logic (search filtering, sorting, pagination).

from modules.listings import database as db

_ALLOWED_SORT_FIELDS = {
    "deadline": "deadline",
    "company": "company_name",
    "title": "job_title",
    "location": "location",
    "salary": "salary_expectation",
    "status": "status",
    "work_model": "work_model",
}

_DEFAULT_FIELD = "deadline"
_DEFAULT_ORDER = "asc"

# helper for pagination
def _normalize_int(value: str | None, default: int, minimum: int, maximum: int) -> int:
    try: 
        n = int(value)
    except (TypeError, ValueError): 
        return default
    return max(minimum, min(maximum, n))

def _parse_sort(sort: str | None, order: str | None):
    sort_field = _DEFAULT_FIELD
    sort_order = 1

    # default order
    direction = (order or _DEFAULT_ORDER).strip().lower()
    if direction not in ("asc", "desc"):
        direction = _DEFAULT_ORDER

    # keep previous compatability (e.g. "deadline_asc")
    if sort:
        s = sort.strip().lower()
        if "_" in s:
            field_key, dir_from_sort = s.split("_", 1)
            if dir_from_sort in ("asc", "desc"):
                direction = dir_from_sort
        else:
            field_key = s

        sort_field = _ALLOWED_SORT_FIELDS.get(field_key, _DEFAULT_FIELD)

    sort_order = 1 if direction == "asc" else -1
    return sort_field, sort_order, (sort or _DEFAULT_FIELD).strip().lower(), direction

def list_applications(user_id: str, view: str, query: str | None, sort: str | None, order: str | None, page: str | None, per_page: str | None): 
    page_n = _normalize_int(page, default=1, minimum=1, maximum=10_000)
    per_page_n = _normalize_int(per_page, default=10, minimum=1, maximum=50)

    sort_field, sort_order, sort_key, order_key = _parse_sort(sort, order)

    status = None
    exclude_status = None 

    v = (view or "").strip().lower()
    if v == "home": 
        status = "not_applied"
    elif v == "applied": 
        exclude_status = "not_applied"
    elif v == "search":
        status = None
        exclude_status = None
    
    cursor, total = db.find_applications(user_id=user_id,
        query=(query or "").strip() or None,
        status=status,
        exclude_status=exclude_status,
        sort_field=sort_field,
        sort_order=sort_order,
        page=page_n,
        per_page=per_page_n,
    )

    total_pages = max((total + per_page_n - 1) // per_page_n, 1)
    page_n = min(page_n, total_pages)

    return {
        "items": list(cursor),
        "total": total,
        "page": page_n,
        "per_page": per_page_n,
        "total_pages": total_pages,
        "sort": sort_key or _DEFAULT_FIELD,
        "order": order_key or _DEFAULT_ORDER,
        "query": query or "",
        "view": v,
    }

def allowed_sort_options():
    return list(_ALLOWED_SORT_FIELDS.keys())