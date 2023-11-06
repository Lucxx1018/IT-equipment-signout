import base64
from flask import Flask, render_template, g, request, redirect, url_for
from pathlib import Path
import sqlite3
import datetime
import os


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
        assert request.json is not None
        response_encoded: str = request.json["signature"].split(",")[1]
        response = base64.b64decode(response_encoded)
        name = request.json["name"]
        file_name = name.lower().replace(" ", "_") + ".svg"
        if Path("signatures").exists() is not True:
            Path("signatures").mkdir()
        with open(f"signatures/{file_name}", "wb") as file:
            file.write(response)

        cursor = get_db().cursor()
        date = datetime.date.today().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        equipment = request.json["equipment"]
        cursor.execute(
            "INSERT INTO equipment_log VALUES($1, $2, $3, $4, $5)",
            (name, date, current_time, equipment, file_name),
        )
        get_db().commit()
        return redirect("success", code=302)  # TODO: Fix broken redirect
    else:
        return render_template("index.jinja")


@app.route("/main.js", methods=["GET"])
def js_serve():
    with open("templates/main.js") as file:
        return file.read()


@app.route("/success", methods=["GET", "POST"])
def success():
    return render_template("success.jinja")
