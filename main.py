from flask import Flask, render_template_string, request, redirect
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

creds_dict = json.loads(os.environ.get("GOOGLE_CREDENTIALS"))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

SHEET_ID = "1pGaQ1feaYIRjfBWdlJHufeRtQ1PaL9tZc9ZtBpHmvPc"
sheet = client.open_by_key(SHEET_ID).sheet1

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return render_template_string(HTML_FORM)

@app.route("/submit", methods=["POST"])
def submit():
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

    return "<h2>Registration Successful. EUROPAIR Team will contact you.</h2>"

# ---------------- UI ---------------- #

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
<title>EUROPAIR Registration</title>
<style>
body {
    font-family: Arial;
    background: linear-gradient(to right, #ffffff, #e6f0ff);
}
.container {
    width: 500px;
    margin: 80px auto;
    padding: 40px;
    background: white;
    border-radius: 12px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.1);
}
input, select {
    width: 100%;
    padding: 12px;
    margin: 8px 0;
    border-radius: 6px;
    border: 1px solid #ccc;
}
button {
    background: #0047ab;
    color: white;
    padding: 12px;
    width: 100%;
    border: none;
    border-radius: 6px;
    font-size: 16px;
}
h2 {
    text-align: center;
    color: #0047ab;
}
</style>
</head>
<body>
<div class="container">
<h2>EUROPAIR Candidate Registration</h2>
<form method="POST" action="/submit">
<input name="name" placeholder="Full Name" required>
<input name="email" placeholder="Email" required>
<input name="phone" placeholder="Phone Number" required>
<input name="country" placeholder="Country" required>
<input name="program" placeholder="Program" required>
<input name="age" placeholder="Age" required>
<input name="german" placeholder="German Level" required>
<input name="marital" placeholder="Marital Status" required>
<input name="rejection" placeholder="Visa Rejection (Yes/No)" required>
<input name="months" placeholder="If Yes, Months Ago" required>
<button type="submit">Submit</button>
</form>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    app.run()