from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import UserMixin, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import login_manager, mongo

auth = Blueprint("auth", __name__)


# --- User Class for Flask-Login ---
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]
        self.role = user_data.get("role", "analyst")  # Default role

    @staticmethod
    def get_by_username(username):
        user_data = mongo.db.users.find_one({"username": username})
        if user_data:
            return User(user_data)
        return None

    @staticmethod
    def get_by_id(user_id):
        from bson.objectid import ObjectId

        try:
            user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if user_data:
                return User(user_data)
        except:
            return None
        return None


# --- Flask-Login Loader ---
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


# --- Routes ---


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get(
            "role", "analyst"
        )  # Optional: let them pick admin/analyst

        # 1. Check if user already exists
        user = mongo.db.users.find_one({"username": username})
        if user:
            flash("Username already exists.", "warning")
            return redirect(url_for("auth.signup"))

        # 2. Hash the password (Security Best Practice)
        hashed_password = generate_password_hash(password)

        # 3. Create new user in MongoDB
        new_user = {"username": username, "password": hashed_password, "role": role}
        mongo.db.users.insert_one(new_user)

        flash("Account created successfully! Please sign in.", "success")
        return redirect(url_for("auth.signin"))

    return render_template("signup.html")


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 1. Find user by username
        user_data = mongo.db.users.find_one({"username": username})

        # 2. Check password hash
        if user_data and check_password_hash(user_data["password"], password):
            user_obj = User(user_data)
            login_user(user_obj)
            flash("Logged in successfully.", "success")

            # Redirect to Dashboard if logged in
            return redirect(url_for("views.dashboard"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("signin.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("views.index"))
