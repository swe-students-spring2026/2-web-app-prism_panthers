from flask_login import UserMixin
from bson.objectid import ObjectId


class User(UserMixin):
    """Wraps a MongoDB user document for Flask-Login."""

    def __init__(self, user_data: dict):
        self._id = user_data["_id"]
        self.email = user_data["email"]

    @property
    def id(self) -> str:
        return str(self._id)

    @staticmethod
    def from_doc(doc: dict | None):
        """Return a User instance or None if the document is missing."""
        return User(doc) if doc else None
