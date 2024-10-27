from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Importing the User model
from models import User

# Login Route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        user = User.query.filter_by(username=username).first()
        if user:
            session["user_id"] = user.id
            return redirect(url_for("dashboard"))
        else:
            return "User not found", 404
    return render_template("login.html")

# Dashboard Route
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Fetch data for the user
    user_id = session["user_id"]
    # Placeholder data
    data_from_google_sheet = get_google_sheet_data(user_id)
    api_data = get_api_data()

    return render_template("dashboard.html", google_data=data_from_google_sheet, api_data=api_data)

def get_google_sheet_data(user_id):
    # Function to fetch data from Google Sheets
    # Replace with actual Google Sheets API logic
    return [{"data": "Sample Google Sheet Data"}]

def get_api_data():
    # Function to fetch data from various APIs
    # Replace with actual API calls
    return [{"data": "Sample API Data"}]

# Logout Route
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()  # Initialize the SQLite database
    app.run(debug=True)
