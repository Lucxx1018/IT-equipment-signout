import base64
from flask import Flask, render_template, g, request
import sqlite3
import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = "please remember to set a password here later"
# PLEASE set the password after downloading, I am not responsible for committed passwords being insecure, they are publicly available.


def get_db():
    if getattr(g, "_database", None) is None:
        g._database = sqlite3.connect("database.db")

    return g._database


@app.teardown_appcontext
def close_db(_exception):
    # TODO: Figure out what black magic makes this error if it isn't given *args
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


with open("schema.sql") as file, app.app_context():
    get_db().executescript(file.read())


@app.route("/", methods=["GET", "POST"])
def index():
    #    if request.json is not None:
    # response_encoded: str = request.json["dataUri"].split(",")[1]
    # response = base64.b64decode(response_encoded)
    # if True:  # TODO: Check if signature already exists before making it again
    #     with open("response.svg", "wb") as file:  # TODO: Make this auto-generate file names using users' names
    #         file.write(response)
    # cursor = get_db().cursor()
    # date = datetime.date.today().strftime("%Y-%M-%D")
    # time = datetime.datetime.now().strftime("%H:%M:%S")
    # cursor.execute(
    #     "INSERT INTO equipment_log() VALUES($1, $2, $3, $4, $5) ",
    #     (NotImplemented, date, time, NotImplemented, response),
    # )
    return render_template("index.jinja")


@app.route("/main.js", methods=["GET"])
def js_serve():
    with open("templates/main.js") as file:
        return file.read()


@app.route("/success", methods=["POST"])
def success():
    return render_template("success.jinja")
