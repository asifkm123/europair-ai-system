from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import os
import json

app = Flask(__name__)

# ---------------- GOOGLE AUTH ---------------- #

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds_json = os.environ.get("GOOGLE_CREDENTIALS")

if not creds_json:
    raise Exception("GOOGLE_CREDENTIALS environment variable not set.")

creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Replace with your real Sheet ID
SHEET_ID = "1pGaQ1feaYIRjfBWdlJHufeRtQ1PaL9tZc9ZtBpHmvPc"

sheet = client.open_by_key(SHEET_ID).sheet1


# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = [
            request.form["name"],
            request.form["email"],
            request.form["phone"],
            request.form["country"],
            request.form["program"],
            request.form["age"],
            request.form["german"],
            request.form["marital"],
            request.form["rejection"],
            request.form["months"],
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]

        sheet.append_row(data)

        return render_template("index.html", success=True)

    except Exception as e:
        return f"<h2>Error occurred: {str(e)}</h2>"


if __name__ == "__main__":
    app.run()