"""Books Sharing"""

from jinja2 import StrictUndefined

from flask import(Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Book, connect_to_db, db

app = Flask(__name__)

app.secret_key = "HBAC"
#app.secret_key = os.environ['SECRET_KEY']


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

    name = request.form.get("user_name")
    email = request.form.get("email")
    password = request.form.get("password")
    zipcode = request.form.get("zipcode")

    new_user = User(user_name=name, email=email, password=password, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()
    
    flash(f"Welcome to the BookLot, {name}")
    return redirect("/")

    # add to the user name welcome.

@app.route("/login", methods=['GET'])
def login_form():

    return render_template("login.html")



@app.route("/login", methods=['POST'])
def logged_in():

    name = request.form.get("user_name")
    # print(name)
    password = request.form.get("password")
    # print(password)

    query = User.query.filter(User.user_name == name, User.password == password).first()
    # print(query)


    if query:
        #seeting user_id = 1 in the session.
        session['user_id'] = query.user_id 
        flash("You are successfully logged in.")

        return redirect('/home')


    else:
        return redirect('/login')


@app.route("/home")
def book_home():
    

    return render_template("home.html")



@app.route("/add_book", methods=['GET'])
def add_form():

    return render_template("add_book.html")


@app.route("/add_book", methods=['POST'])
def adding_book():

    title = request.form.get("title")
    author = request.form.get("author")
    
    #first title is param
    book = Book(title=title, author=author, user_id=session['user_id'])

    user = User.query.get(session['user_id'])

    # user.books
    # user.email

    # book = Book.query.filter


    db.session.add(book)
    db.session.commit()

    
    return render_template("add_book.html")

@app.route("/search")




if __name__ =="__main__":

    app.debug = True


    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)


    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')