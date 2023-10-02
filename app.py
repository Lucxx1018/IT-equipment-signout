from flask import Flask, render_template, redirect, url_for, request, session, g
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, DateTimeField, SelectField
from wtforms.validators import DataRequired
import sqlite3
import random
import string
import datetime


class NameForm(FlaskForm):
    name = StringField("Put your name here:", validators=[DataRequired()])
    date = DateTimeField("Current date:")
    time = DateTimeField("Current time:")
    equipment = SelectField(
        "Select equipment",
        choices=[("test", "test"), ("but with different text oooo", "also test")],
        validators=DataRequired(),
    )
    signature = FileField("Attach the file with the signature here:", validators=[DataRequired()])
    submit = SubmitField("Click here when all fields are filled in.")


app = Flask(__name__)
app.config["SECRET_KEY"] = "please remember to set a password here later"
