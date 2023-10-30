import base64
from flask import Flask, render_template, g, request, redirect
import sqlite3
import datetime
import time


app = Flask(__name__)
app.config["SECRET_KEY"] = "please remember to set a password here later"
# PLEASE set the password after downloading, I am not responsible for committed passwords being insecure, they are publicly available.


def get_db():
    if getattr(g, "_database", None) is None:
        g._database = sqlite3.connect("database.db")

    return g._database


@app.teardown_appcontext
def close_db(_exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


with open("schema.sql") as file, app.app_context():
    get_db().executescript(file.read())


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # response_encoded: str = request.json["dataUri"].split(",")[1]
        # response = base64.b64decode(response_encoded)
        # with open("response.svg", "wb") as file:  # TODO: Make this auto-generate file names using users' names
        #    file.write(response)
        cursor = get_db().cursor()
        # name = request.form["name"]
        date = datetime.date.today().strftime("%Y-%M-%D")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        # equipment = request.form["equipment"]
        # cursor.execute(
        #    "INSERT INTO equipment_log() VALUES($1, $2, $3, $4, $5) ",
        #    (name, date, time, equipment, NotImplemented),
        # )
        return redirect("/success", code=302)
    return render_template("index.jinja")


@app.route("/main.js", methods=["GET"])
def js_serve():
    with open("templates/main.js") as file:
        return file.read()


@app.route("/success", methods=["GET"])
def success():
    return render_template("success.jinja")
