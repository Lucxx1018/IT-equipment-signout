from flask import Flask, render_template, g, request
from typing import Optional
from pathlib import Path
import datetime
import sqlite3
import base64


app = Flask(__name__)
app.config["SECRET_KEY"] = "please remember to set a password here later"
# PLEASE set the password after downloading, I am not responsible for committed passwords being insecure, they are publicly available.


def get_db():
    if getattr(g, "_database", None) is None:
        g._database = sqlite3.connect("database.db")

    return g._database


@app.teardown_appcontext
def close_db(_: Optional[BaseException]):
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
        name = name.lower().replace(" ", "_")  # This makes John Doe -> john_doe
        try:
            Path("signatures").mkdir()
        except FileExistsError:
            pass

        cursor = get_db().cursor()
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        equipment = request.json["equipment"]
        cursor.execute(
            "INSERT INTO equipment_log VALUES($1, $2, $3, $4, $5)",
            (name, equipment, 0, time, time),
        )
        get_db().commit()
        with open(
            f"signatures/{name}-{time.replace(':', '-')}.svg", "wb"
        ) as file:  # This comes out as john_doe-1999-12-31 11-59-59
            file.write(response)
        return '{"redirect_to": "success"}'
    else:
        return render_template("index.jinja")


@app.route("/signin", methods=["GET", "POST"])
def signin(names):
    cursor = get_db().cursor()
    if request.method == "POST":
        assert request.json is not None
        name = request.json["name"].lower().replace(" ", "_")
        equipment = request.json["equipment"]
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            """
            UPDATE equipment_log
            SET Returned = $1, TimeIn = $2
            WHERE Name = $3 AND Equipment = $4""",
            (1, time, name, equipment),
        )
        get_db().commit()
        return '{"redirect_to": "success"}'
    else:
        # TODO: Let users choose their name from a dropdown of currently unresolved signouts
        cursor.execute("""SELECT Name FROM equipment_log WHERE Returned = 0""")
        names = cursor.fetchall()[0][0]
        print(names)
        return render_template("signin.jinja", names=names)


@app.route("/main.js", methods=["GET"])
def js_serve():
    with open("templates/main.js") as file:
        return file.read()


@app.route("/signin.js", methods=["GET"])
def serve_js():
    with open("templates/signin.js") as file:
        return file.read()


@app.route("/style.css", methods=["GET"])
def css_serve():
    with open("static/style.css") as file:
        return file.read()


@app.route("/success", methods=["GET", "POST"])
def success():
    return render_template("success.jinja")


# TODO: Create and serve a favicon.ico, they're neat
