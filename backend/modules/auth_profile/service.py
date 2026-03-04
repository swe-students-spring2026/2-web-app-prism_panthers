"""Auth & profile business logic."""

import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

from modules.auth_profile import database as db
from modules.auth_profile.models import User


# ── Authentication ──────────────────────────────────────

def authenticate(email: str, password: str) -> User | None:
    """Return a User if credentials are valid, else None."""
    doc = db.find_user_by_email(email.strip().lower())
    if doc and check_password_hash(doc["password"], password):
        return User(doc)
    return None


def register(email: str, password: str, confirm_password: str) -> tuple[bool, str]:
    """Create a new user account. Returns (success, message)."""
    email = email.strip().lower()

    if password != confirm_password:
        return False, "Passwords do not match."

    if db.find_user_by_email(email):
        return False, "An account with that email already exists."

    hashed = generate_password_hash(password)
    db.insert_user(email, hashed)
    return True, "Account created!"


# ── Password reset ──────────────────────────────────────

def request_password_reset(email: str) -> str | None:
    """Generate a reset token. Returns the token string, or None if no user found."""
    doc = db.find_user_by_email(email.strip().lower())
    if not doc:
        return None

    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=30)
    db.insert_reset_token(str(doc["_id"]), token, expires_at)
    return token


def reset_password(token: str, new_password: str, confirm_password: str) -> tuple[bool, str]:
    """Use a reset token to change the password. Returns (success, message)."""
    if new_password != confirm_password:
        return False, "Passwords do not match."

    reset = db.find_reset_token(token)
    if not reset:
        return False, "Invalid or expired reset link."

    if reset["expires_at"] < datetime.utcnow():
        return False, "Reset link has expired."

    hashed = generate_password_hash(new_password)
    db.update_user_password(reset["user_id"], hashed)
    db.mark_reset_token_used(token)
    return True, "Password updated!"


# ── Change password (logged-in user) ────────────────────

def change_password(user_id: str, current_password: str, new_password: str, confirm_password: str) -> tuple[bool, str]:
    """Change password for a logged-in user. Returns (success, message)."""
    if new_password != confirm_password:
        return False, "Passwords do not match."

    doc = db.find_user_by_id(user_id)
    if not doc or not check_password_hash(doc["password"], current_password):
        return False, "Current password is incorrect."

    hashed = generate_password_hash(new_password)
    db.update_user_password(user_id, hashed)
    return True, "Password updated!"


# ── Profile ─────────────────────────────────────────────

def get_profile(user_id: str) -> dict | None:
    """Return the user document for profile display."""
    return db.find_user_by_id(user_id)


def update_profile(user_id: str, data: dict) -> tuple[bool, str]:
    """Update allowed profile fields. Returns (success, message)."""
    allowed = {"email", "full_name", "university", "major", "grad_year", "bio", "profile_picture"}
    updates = {k: v for k, v in data.items() if k in allowed and v}
    if not updates:
        return False, "Nothing to update."
    db.update_user_profile(user_id, updates)
    return True, "Profile updated!"


def delete_account(user_id: str):
    """Delete the user account and related data."""
    db.delete_user(user_id)

def update_links(user_id: str, data: dict) -> tuple[bool, str]:
    """Update profile link fields (website, LinkedIn, portfolio). Returns (success, message)."""
    allowed = {"website_url", "linkedin_url", "portfolio_url"}
    # Allow empty strings so users can clear a link
    updates = {k: v.strip() for k, v in data.items() if k in allowed}
    if not updates:
        return False, "Nothing to update."
    db.update_user_profile(user_id, updates)
    return True, "Links updated!"