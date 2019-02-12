"""Books Sharing"""

from jinja2 import StrictUndefined

from flask import(Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Book, connect_to_db, db

app = Flask(__name__)

app.secret_key = "HBAC"


app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Homepage"""

    return render_template("homepage.html")



@app.route("/register", methods=["GET"])
def register_form():
    """registering a user"""

    return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def register_process():
    """getting store user_name. email and password to database"""

    name = 







if __name__ =="__main__":

    app.debug = True


    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)


    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')