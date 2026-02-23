# Listings database operations (query with filters, sort, text search).

from extensions import db

def _internships():
    return db["internships"]

def find_applications(user_id: str, query: str | None, sort_field: str, sort_order: int): 
    filter_query = {"user_id": user_id}

    if query: 
        filter_query["company"] = {"$regex": query, "options": "i"}
    
    return _internships().find(filter_query).sort(sort_field, sort_order)
