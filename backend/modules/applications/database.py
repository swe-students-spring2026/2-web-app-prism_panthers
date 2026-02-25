# Application CRUD database operations (insert, find_one, update, delete).
from bson.objectid import ObjectId
from extensions import db

def applications_collection():
    return db.internship

def insert_application(application):
    #insert new application and return _id
    return applications_collection().insert_one(application.to_document())

def find_application_by_id(application_id):
    #find application by _id return doc
    return applications_collection().find_one({"_id":ObjectId(application_id)})

def update_application_by_id(application_id,updates):
    #update application with set "updates", return
    return applications_collection().update_one({"_id":application_id},{"$set":updates})

def delete_application_by_id(application_id):
    return applications_collection().delete_one({"_id":application_id})

