import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# ===============================
# GOOGLE SHEETS CONNECTION
# ===============================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def connect_sheet():
    try:
        creds_json = os.environ.get("GOOGLE_CREDENTIALS")

        if not creds_json:
            raise Exception("GOOGLE_CREDENTIALS environment variable not found")

        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        client = gspread.authorize(creds)

        # 🔥 CHANGE THIS IF YOUR SHEET NAME IS DIFFERENT
        sheet = client.open("AI DATABASE").sheet1

        return sheet

    except Exception as e:
        print("Google Sheet Connection Error:", e)
        return None


# ===============================
# ROUTES
# ===============================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    sheet = connect_sheet()

    if not sheet:
        return "Sheet connection failed. Check credentials.", 500

    # Get form values
    name = request.form.get("name")
    email = request.form.get("email")
    number = request.form.get("number")
    land = request.form.get("land")
    program = request.form.get("program")
    age = request.form.get("age")
    language = request.form.get("language")
    marital = request.form.get("marital")
    rejection = request.form.get("rejection")
    rejection_when = request.form.get("rejection_when")

    try:
        existing_records = sheet.get_all_records()
    except:
        existing_records = []

    # ===============================
    # DUPLICATE EMAIL CHECK
    # ===============================

    for record in existing_records:
        if str(record.get("MAIL ID", "")).strip().lower() == str(email).strip().lower():
            return redirect(url_for("duplicate"))

    # ===============================
    # APPEND NEW ROW
    # ===============================

    try:
        sheet.append_row([
            name,
            email,
            number,
            land,
            program,
            age,
            language,
            marital,
            rejection,
            rejection_when,
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "NEW LEAD"
        ])
    except Exception as e:
        print("Append Error:", e)
        return "Error saving data", 500

    return redirect(url_for("success"))


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/duplicate")
def duplicate():
    return render_template("duplicate.html")


# ===============================
# RUN APP
# ===============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)