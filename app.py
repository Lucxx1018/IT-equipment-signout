import base64
from flask import Flask, render_template, g, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired
import sqlite3
import string
import datetime


class NameForm(FlaskForm):
    name = StringField("Put your name here:", validators=[DataRequired()])
    equipment = SelectField(
        "Select equipment",
        choices=[("test", "test"), ("but with different text oooo", "also test")],
        validators=[DataRequired()],
    )
    signature = FileField("Attach the file with the signature here:", validators=[DataRequired()])
    submit = SubmitField("Click here when all fields are filled in.")


app = Flask(__name__)
app.config["SECRET_KEY"] = "please remember to set a password here later"


def get_db():
    if getattr(g, "_database", None) is None:
        g._database = sqlite3.connect("database.db")

    return g._database


@app.teardown_appcontext
def close_db(*args):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


with open("schema.sql") as file, app.app_context():
    get_db().executescript(file.read())

@app.route("/process", methods=["POST"])
def process():
    # TODO: Handle
    assert request.json is not None

    response_encoded: str = request.json["dataUri"].split(",")[1]
    response = base64.b64decode(response_encoded)
    with open("response.svg", "wb") as file:
        file.write(response)

    return ""

@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        cursor = get_db().cursor()
        date = datetime.date.today().strftime("%Y-%M-%D")
        time = datetime.datetime.now().strftime("%H:%M:%S")
        cursor.execute(
            "INSERT INTO equipment_log() VALUES($1, $2, $3, $4, $5) ",
            (form.name.data, date, time, form.equipment.data, NotImplemented),
        )
    return render_template("index.jinja", form=form)

@app.route("/main.js", methods=["GET"])
def js_serve():
    with open("templates/main.js") as file:
        return file.read()
