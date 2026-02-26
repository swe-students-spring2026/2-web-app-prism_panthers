# Application CRUD business logic (validate, create, update, delete).
from . import database
from .models import Application

def create_application(user_id, company_name, job_title, location, salary_expectation, application_link, deadline, personal_notes, work_model, status):
    application = Application(user_id, company_name, job_title, location, salary_expectation, application_link, deadline, personal_notes, work_model,status)
    result = database.insert_application(application)
    return str(result.inserted_id)

def get_application(application_id):
    doc = database.find_application_by_id(application_id)
    return Application.from_document(doc)

def update_application(application_id,updates):
    database.update_application_by_id(application_id,updates)
    return get_application(application_id)

def delete_application(application_id):
    return database.delete_application_by_id(application_id)