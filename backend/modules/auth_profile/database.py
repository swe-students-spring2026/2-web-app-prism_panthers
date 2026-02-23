"""Auth & profile database operations."""

from bson.objectid import ObjectId
import extensions


# ── helpers ──────────────────────────────────────────────

def _users():
    return extensions.db["users"]

def _password_resets():
    return extensions.db["password_resets"]


# ── user CRUD ────────────────────────────────────────────

def find_user_by_email(email: str) -> dict | None:
    return _users().find_one({"email": email})


def find_user_by_id(user_id: str) -> dict | None:
    return _users().find_one({"_id": ObjectId(user_id)})


def insert_user(email: str, password_hash: str) -> str:
    result = _users().insert_one({
        "email": email,
        "password": password_hash,
    })
    return str(result.inserted_id)


def update_user_password(user_id: str, new_password_hash: str):
    _users().update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password": new_password_hash}},
    )


def update_user_profile(user_id: str, updates: dict):
    _users().update_one(
        {"_id": ObjectId(user_id)},
        {"$set": updates},
    )


def delete_user(user_id: str):
    _users().delete_one({"_id": ObjectId(user_id)})
    _password_resets().delete_many({"user_id": user_id})


# ── password reset tokens ───────────────────────────────

def insert_reset_token(user_id: str, token: str, expires_at):
    _password_resets().delete_many({"user_id": user_id})
    _password_resets().insert_one({
        "user_id": user_id,
        "token": token,
        "expires_at": expires_at,
        "used": False,
    })


def find_reset_token(token: str) -> dict | None:
    return _password_resets().find_one({"token": token, "used": False})


def mark_reset_token_used(token: str):
    _password_resets().update_one(
        {"token": token},
        {"$set": {"used": True}},
    )
