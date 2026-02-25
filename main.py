from flask import Flask, render_template, request, redirect, url_for
import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# ==========================
# GOOGLE AUTHENTICATION
# ==========================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(os.environ.get("GOOGLE_CREDENTIALS"))
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

# Open your Google Sheet
sheet = client.open("EUROPAIR AI DATABASE").sheet1


# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def index():
    return render_template("index.html")


# ==========================
# SUBMIT FORM
# ==========================

@app.route("/submit", methods=["POST"])
def submit():

    # Get form data
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    country = request.form.get("country")
    program = request.form.get("program")
    age = request.form.get("age")
    german_level = request.form.get("german_level")
    marital_status = request.form.get("marital_status")
    visa_rejection = request.form.get("visa_rejection")

    # ==========================
    # PREVENT DUPLICATES
    # ==========================

    existing_records = sheet.get_all_records()

    for row in existing_records:
        if row["Full Name"] == name and row["Phone Number"] == phone:
            return redirect(url_for("success"))

    # ==========================
    # ADD TIMESTAMP
    # ==========================

    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # ==========================
    # APPEND ROW TO SHEET
    # ==========================

    sheet.append_row([
        timestamp,
        name,
        email,
        phone,
        country,
        program,
        age,
        german_level,
        marital_status,
        visa_rejection
    ])

    return redirect(url_for("success"))


# ==========================
# SUCCESS PAGE
# ==========================

@app.route("/success")
def success():
    return render_template("success.html")


# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":
    app.run(debug=True)