# Listings business logic (search filtering, sorting, pagination).

from modules.listings import database as db

_ALLOWED_SORT_FIELDS = {
    "deadline": "deadline", 
    "company": "company", 
    "status": "status", 
    "created": "created_at"
}

def list_applications(user_id: str, query: str, sort: str): 
    sort_by = "deadline"
    sort_order = 1

    if "_" in sort: 
        field, direction = sort.split("_", 1)
        if field in _ALLOWED_SORT_FIELDS: 
            sort_by = _ALLOWED_SORT_FIELDS[field]
        sort_order = 1 if direction == "asc" else -1 
    
    return db.find_applications(user_id, query, sort_by, sort_order)
    
