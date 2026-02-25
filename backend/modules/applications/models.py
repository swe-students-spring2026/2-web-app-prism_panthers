# Application model or helper class.
from bson.objectid import ObjectId

class Application:
    '''
    Single Job Application in Database
    '''
    def __init__(self, user_id, company_name, job_title, location, salary_expectation, application_link, deadline, personal_notes, work_model="On-site", status="Yet to Apply", _id=None):
        self.user_id = user_id
        self.company_name = company_name
        self.job_title = job_title
        self.location = location
        self.salary_expectation = salary_expectation
        self.application_link = application_link
        self.work_model = work_model
        self.deadline = deadline
        self.personal_notes = personal_notes
        self.status = status
        self._id = ObjectId() if _id is None else ObjectId(_id)

    #turn data into doc, ready to be inserted into database
    def to_document(self):
        return{
            "user_id": self.user_id,
            "company_name": self.company_name,
            "job_title": self.job_title,
            "location": self.location,
            "salary_expectation": self.salary_expectation,
            "application_link": self.application_link,
            "work_model": self.work_model,
            "deadline": self.deadline,
            "personal_notes": self.personal_notes,
            "status": self.status,
        }

    #Extract data from doc in mongo
    @staticmethod
    def from_document(doc):
        return Application(
            user_id=doc.get("user_id"),
            company_name=doc.get("company_name"),
            job_title=doc.get("job_title"),
            location=doc.get("location"),
            salary_expectation=doc.get("salary_expectation"),
            application_link=doc.get("application_link"),
            work_model=doc.get("work_model"),
            deadline=doc.get("deadline"),
            personal_notes=doc.get("personal_notes"),
            status=doc.get("status"),
            _id=doc.get("_id"),
        )

