# Listings database operations (query with filters, sort, text search).

from extensions import db

def _internships():
    return db["internships"]

def find_applications(user_id: str, query: str | None, status: str | None, exclude_status: str | None, sort_field: str, sort_order: int, page: int, per_page: int): 
    filter_query: dict = {"user_id": user_id}
    if status is not None: 
        filter_query["status"] = status 
    
    if exclude_status is not None: 
        filter_query["status"] = {"$ne": exclude_status}

    if query:
        filter_query["$or"] = [
            {"company_name": {"$regex": query, "$options": "i"}},
            {"job_title": {"$regex": query, "$options": "i"}},
            {"location": {"$regex": query, "$options": "i"}},
            {"work_model": {"$regex": query, "$options": "i"}},
            {"status": {"$regex": query, "$options": "i"}},
        ]
    
    cursor = (
        _internships().find(filter_query).sort(sort_field, sort_order).skip( max(page - 1, 0) * per_page ).limit(per_page)
    )

    total = _internships().count_documents(filter_query)

    return cursor, total
