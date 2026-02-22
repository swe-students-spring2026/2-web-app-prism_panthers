from flask_login import LoginManager
from pymongo import MongoClient

login_manager = LoginManager()
login_manager.login_view = "auth_profile.login"

mongo_client: MongoClient = None
db = None


def init_extensions(app):
    global mongo_client, db

    login_manager.init_app(app)

    mongo_client = MongoClient(app.config["MONGO_URI"])
    db = mongo_client[app.config["DB_NAME"]]

    from modules.auth_profile.models import User
    from modules.auth_profile.database import find_user_by_id

    @login_manager.user_loader
    def load_user(user_id):
        doc = find_user_by_id(user_id)
        return User.from_doc(doc)
