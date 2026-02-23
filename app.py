from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import secrets
from datetime import timedelta
import os

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI) if MONGO_URI else None
db = client[DB_NAME] if (client is not None and DB_NAME is not None) else None

users_collection = db["users"] if db is not None else None
internships_collection = db["internships"] if db is not None else None
password_resets = db["password_resets"] if db is not None else None


### UI Demo routes -frontend 
@app.route("/ui/login")
def ui_login():
    return render_template("auth/login.html")

@app.route("/ui/register")
def ui_register():
    return render_template("auth/register.html")

@app.route("/ui/update-password")
def ui_update_password():
    return render_template("auth/update_password.html")

@app.route("/update-password-demo", methods=["POST"])
def update_password_demo():
    flash("Password updated successfully.", "success")
    return redirect(url_for("ui_profile"))

@app.route("/ui/profile")
def ui_profile():
    return render_template(
        "profile/profile.html",
        total=12,
        interviews=3,
        offers=1,
        rejected=4
    )
    
@app.route("/ui/edit-profile")
def ui_edit_profile():
    return render_template("profile/edit_profile.html")

@app.route("/ui/update-profile", methods=["POST"])
def ui_update_profile():
    flash("Profile successfully updated.", "success")
    return redirect(url_for("ui_profile"))

@app.route("/ui/change-photo", methods=["POST"])
def demo_change_photo():
    flash("Photo changed successfully.", "success")
    return redirect(url_for("ui_profile"))

@app.route("/ui/update-resume", methods=["POST"])
def ui_update_resume():
    flash("Resume updated successfully.", "success")
    return redirect(url_for("ui_profile"))

@app.route("/ui/update-links", methods=["POST"])
def ui_update_links():
    flash("Links updated successfully.", "success")
    return redirect(url_for("ui_profile"))

@app.route("/ui/delete-profile")
def ui_delete_profile():
    return render_template("profile/delete_profile.html")

@app.route("/ui/delete-account", methods=["POST"])
def delete_account_demo():
    flash("Account deleted successfully.", "success")
    return redirect(url_for("login"))


@app.route("/ui/apply")
def ui_apply():
    internships = [
        {"company": "Google", "role": "SWE Intern", "status": "Yet to Apply"},
        {"company": "Apple", "role": "ML Intern", "status": "Yet to Apply"},
    ]
    return render_template("internship/apply.html", internships=internships)

@app.route("/ui/applied")
def ui_applied():
    internships = [
        {"company": "Meta", "role": "Backend Intern", "status": "Interviewing", "deadline": "2026-03-01"},
        {"company": "Stripe", "role": "SWE Intern", "status": "Rejected", "deadline": "2026-02-20"},
    ]
    return render_template("internship/applied.html", internships=internships)

@app.route("/ui/search")
def ui_search():
    internships = [
        {"company": "Amazon", "role": "SDE Intern", "status": "Offer"},
    ]
    return render_template("internship/search.html", internships=internships)

@app.route("/ui/add")
def ui_add():
    return render_template("internship/add.html")

@app.route("/ui/edit-intern")
def ui_edit():
    internship = {
        "company": "Netflix",
        "role": "SWE Intern",
        "status": "Applied",
        "notes": "Follow up next week"
    }
    return render_template("internship/edit_intern.html", internship=internship)


#############################
#login setup
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.email = user_data["email"]
        
@login_manager.user_loader
def load_user(user_id):
    if users_collection is None:
        return None
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

#Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = users_collection.find_one({"email": email})

        if user and user["password"] == password:  # hash in real app
            login_user(User(user))
            return redirect(url_for("home"))

        flash("Invalid credentials", "danger")

    return render_template("auth/login.html")

#Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("register"))

        users_collection.insert_one({
            "email": email,
            "password": password
        })

        flash("Account created!", "success")
        return redirect(url_for("login"))

    return render_template("auth/register.html")

#Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

#Forgot password
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    reset_link = None

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        user = users_collection.find_one({"email": email})

        if user:
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(minutes=30)

            # delete old pass
            password_resets.delete_many({"user_id": str(user["_id"])})

            password_resets.insert_one({
                "user_id": str(user["_id"]),
                "token": token,
                "expires_at": expires_at,
                "used": False,
                "created_at": datetime.utcnow()
            })

            reset_link = url_for("reset_password", token=token, _external=True)
            # email this link
            print("RESET LINK:", reset_link)

        flash("If that email exists, a reset link has been sent.", "success")
        return render_template("auth/forgot_password.html", reset_link=reset_link)

    return render_template("auth/forgot_password.html", reset_link=reset_link)

#update password
#@app.route("/update/demo-token")
#def reset_demo():
#   return render_template("auth/update_password.html")
# make updates on this route after databases; currently using demo route
 
#Profile page
@app.route("/profile")
@login_required
def profile():
    total = internships_collection.count_documents({"user_id": current_user.id})
    interviews = internships_collection.count_documents({
        "user_id": current_user.id,
        "status": "Interviewing"
    })
    offers = internships_collection.count_documents({
        "user_id": current_user.id,
        "status": "Offer"
    })
    rejected = internships_collection.count_documents({
        "user_id": current_user.id,
        "status": "Rejected"
    })

    return render_template(
        "profile/profile.html",
        total=total,
        interviews=interviews,
        offers=offers,
        rejected=rejected
    )
    
#delete account
@app.route("/delete-account", methods=["POST"])
@login_required
def delete_account():
    users_collection.delete_one({"_id": ObjectId(current_user.id)})
    logout_user()
    flash("Account deleted successfully.", "success")
    return redirect(url_for("login"))


#Apply
@app.route("/")
@login_required
def home():
    internships = internships_collection.find({
        "user_id": current_user.id,
        "status": "Yet to Apply"
    })

    return render_template("internship/apply.html", internships=internships)

#Applied
@app.route("/applied")
@login_required
def applied():
    sort_option = request.args.get("sort", "deadline_asc")

    sort_order = 1 if sort_option == "deadline_asc" else -1

    internships = internships_collection.find({
        "user_id": current_user.id,
        "status": {"$ne": "Yet to Apply"}
    }).sort("deadline", sort_order)

    return render_template("internship/applied.html", internships=internships)

#Search
@app.route("/search")
@login_required
def search():
    query = request.args.get("q")

    if query:
        internships = internships_collection.find({
            "user_id": current_user.id,
            "company": {"$regex": query, "$options": "i"}
        })
    else:
        internships = []

    return render_template("internship/search.html", internships=internships)

#Add internship
@app.route("/internships/new", methods=["GET", "POST"])
@login_required
def new_internship():
    if request.method == "POST":
        internships_collection.insert_one({
            "user_id": current_user.id,
            "company": request.form["company"],
            "role": request.form["role"],
            "status": request.form["status"],
            "deadline": datetime.strptime(request.form["deadline"], "%Y-%m-%d"),
            "notes": request.form["notes"],
            "created_at": datetime.utcnow()
        })

        flash("Internship added!", "success")
        return redirect(url_for("home"))

    return render_template("internship/add.html")

#Edit internship
@app.route("/internships/<id>/edit", methods=["GET", "POST"])
@login_required
def edit_internship(id):
    internship = internships_collection.find_one({"_id": ObjectId(id),"user_id": current_user.id})

    if request.method == "POST":
        internships_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "company": request.form["company"],
                "role": request.form["role"],
                "status": request.form["status"],
                "deadline": datetime.strptime(request.form["deadline"], "%Y-%m-%d"),
                "notes": request.form["notes"]
            }}
        )
        return redirect(url_for("applied"))

    return render_template("internship/edit_intern.html", internship=internship)

#Delete internship
@app.route("/internships/<id>/delete", methods=["POST"])
@login_required
def delete_internship(id):
    internships_collection.delete_one({"_id": ObjectId(id),"user_id": current_user.id})
    flash("Deleted successfully", "warning")
    return redirect(url_for("applied"))

######################################

#Main
if __name__ == "__main__":
    app.run(debug=True)