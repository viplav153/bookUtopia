"""Books Sharing"""

from jinja2 import StrictUndefined

from flask import(Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Book, connect_to_db, db
import os 


app = Flask(__name__)


app.secret_key = os.environ['secret_key']


app.jinja_env.undefined = StrictUndefined

###################################################################
@app.route("/")
def index():
    """Homepage"""
    return render_template("homepage.html")


######################################################################
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
    
    flash(f"You successfully registed {name} .")
    return render_template("homepage.html", name=name)

############################################################################

@app.route("/login", methods=['GET'])
def login_form():
    """User login form"""

    return render_template("login.html")



@app.route("/login", methods=['POST'])
def logged_in():
    """getting the user login name and password, check if matches with the database"""

    name = request.form.get("user_name")
    password = request.form.get("password")
  
    query = User.query.filter(User.user_name == name, User.password == password).first()
    


    if query:
        #seeting user_id = 1 in the session.
        session['user_id'] = query.user_id 
        flash("You are successfully logged in.")

        return redirect('/home')

    # elif:



    else:
        return redirect('/login')
################################################################################

@app.route("/logout", methods=['GET'])
def logout():
    """Log out"""

    del session['user_id']
    flash("Logged out.")
    return redirect("/")


###################################################################################

@app.route("/home")
def book_home():

    if session:
        user = User.query.get(session['user_id'])
        name = user.user_name

    
        books = Book.query.all()

        return render_template("home.html", books=books,name=name)

####################################################################################

@app.route("/add_book", methods=['GET'])
def add_form():

    return render_template("add_book.html")


@app.route("/add_book", methods=['POST'])
def adding_book():

    title = request.form.get("title")
    print(title)
    author = request.form.get("author")
    
    #first title is param
    book = Book(title=title, author=author, user_id=session['user_id'])

    user = User.query.get(session['user_id'])

    # user.books
    # user.email

    # book = Book.query.filter


    db.session.add(book)
    db.session.commit()

    
    return redirect('/book_list')

####################################################################################
@app.route("/search")
def search_form():


    # book = Book.query.all()
    # print(book)
    # book_id = book[book_id]
    # print(book_id)

    return render_template("/search.html")


@app.route("/search", methods=['POST'])
def search_func():

    keyword = request.form.get('keyword')

    book_result = Book.query.filter(db.or_(Book.title.contains(keyword),
                                   Book.author.contains(keyword))).all()
    #query with keyword in user table
    # query = Book.query.filter(Book.title == title, Book.author == author).first()
    zipcode = request.form.get('zipcode')

    zipcode_result = User.query.filter(User.zipcode.contains(zipcode)).all()


    if book_result or zipcode_result:
         # r = book_result[0]
         # title = r.title
         # author = r.author
        
        flash("We have the book!")

        return render_template('search_result.html', book_result=book_result, zipcode_result=zipcode_result)
    else:

        flash("Sorry, book is no find, please search again.")

        return redirect("/search")

#####################################################################################

@app.route("/delete", methods=["POST"])
def delete_book():
     
      book_id = request.form.get("book_id")

      bookid = Book.query.filter(Book.book_id == book_id).first()


      db.session.delete(bookid)
      db.session.commit()

      return redirect('/book_list')



#####################################################################################

@app.route("/book_list")
def book_list():


    books = Book.query.filter(Book.user_id == session['user_id']).all()
    return render_template("book_list.html", books=books)


#######################################################################################

if __name__ == "__main__":

    app.debug = True


    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)


    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')