"""Books Sharing"""

from jinja2 import StrictUndefined
from flask import(Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Book, connect_to_db, db
import requests
import os 

# from  book_api  import search



app = Flask(__name__)


app.secret_key = os.environ['secret_key']

key = os.environ["book_api_key"]


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


    user_isbn = request.form.get("isbn")


    #Connect to the API to get the isbn book infomation.
    url = "https://www.googleapis.com/books/v1/volumes"

    key = os.environ["book_api_key"]

    payload = {"q": "isbn:{}".format(user_isbn), "key": key}

    r = requests.get(url, params=payload)

    book_info = r.json()

    # Loop through the json file to get title, author and image.
    title = []
    author = []
    cover_url = []


    for key in book_info.keys():

     title_list = book_info["items"][0]["volumeInfo"]["title"]
     title.append(title_list)

     author_list = book_info["items"][0]["volumeInfo"]["authors"]
     author.append(author_list)

     cover_url_list  = book_info["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
     cover_url.append(cover_url_list)

    

    
    #first title is param
    book = Book(title=title[0], author=author[0], book_cover=cover_url[0], ISBN=user_isbn, user_id=session['user_id'])

    user = User.query.get(session['user_id'])

 


    db.session.add(book)
    db.session.commit()
    
    return redirect('/book_list')

#Search funtion:
####################################################################################
@app.route("/search", methods=['GET'])
def search_form():
    choices = ['Keyword', 'Title', 'Author', 'Zipcode']
 
    return render_template("/search.html", choices=choices)



@app.route("/search", methods=['POST'])
def search_func():


    user_choice = request.form.get('choice')
    user_input = request.form.get('search')

    if user_choice == 'Keyword':
        book_result = Book.query.filter(db.or_(Book.title.contains(user_input),
                                        Book.author.contains(user_input))).all()
    # elif user_choice == 'Title':

    elif user_choice == 'Title':
        book_result = Book.query.filter(Book.title.contains(user_input)).all()


    elif user_choice == 'Author':
        book_result = Book.query.filter(Book.author.contains(user_input)).all()


    # elif user_choice == 'Zipcode':




    # book_result = Book.query.filter(db.or_(Book.title.contains(keyword),
                                   # Book.author.contains(keyword))).all()
    #query with keyword in user table
    # # query = Book.query.filter(Book.title == title, Book.author == author).first()
    # zipcode = request.form.get('zipcode')
   

    if book_result:
        
        
        flash("We have the book!")

        return render_template('search_result.html', book_result=book_result)
    else:

        flash("Sorry, book is no find, please search again.")

        return redirect("/search")
# ###################################################################################
#     zipcode = request.form.get('zipcode')

#     zipcode_result = User.query.filter(User.zipcode == zipcode).all()

#     user = zipcode_result[0]

#     book = Book.query.filter(Book.user_id == user.user_id).all()

#     book_detail = book[0]

#     title = book_detail.title

#     author = book_detail.author

#     ISBN   = book_detail.ISBN

#     cover_url = book_detail.book_cover

#     if zipcode_result:
        
        
#         flash("We have the book!")

#         return render_template('search_result.html', book=book, book_cover=cover_url, title=title, author=author, ISBN=ISBN )
#     else:

#         flash("Sorry, book is no find, please search again.")

#         return redirect("/search")


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