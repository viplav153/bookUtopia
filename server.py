"""Books Sharing"""

from jinja2 import StrictUndefined
from flask import(Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Book, connect_to_db, db
from sqlalchemy import func
from twilio.rest import Client
import requests
import os 


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
################################################################################Logout

@app.route("/logout", methods=['GET'])
def logout():
    """Log out"""

    del session['user_id']
    flash("Logged out.")
    return redirect("/")


###################################################################################Login User homepage

@app.route("/home")
def book_home():

    if session:
        user = User.query.get(session['user_id'])
        name = user.user_name

        books = Book.query.all()

        return render_template("home.html", books=books,name=name)

####################################################################################Add function

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

    print(payload)

    r = requests.get(url, params=payload)

    book_info = r.json()

    print(book_info)

    # Loop through the json file to get title, author and image.
    title = []
    author = []
    cover_url = []

    try:
        for key in book_info.keys():

            title_list = book_info["items"][0]["volumeInfo"]["title"]
            title.append(title_list)

            author_list = book_info["items"][0]["volumeInfo"]["authors"]
            author.append(author_list)

            cover_url_list  = book_info["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
            cover_url.append(cover_url_list)

    except KeyError:

            cover_url = "https://web.northamptoncounty.org/Corrections/images/No_image_available.png"

    #first title is param
    book = Book(title=title[0], author=author[0], book_cover=cover_url[0], ISBN=user_isbn, user_id=session['user_id'])

    user = User.query.get(session['user_id'])

    db.session.add(book)
    db.session.commit()
    
    return redirect('/book_list')


#####################################################################################Search funtion:
@app.route("/search", methods=['GET'])
def search_form():
    choices = ['Keyword', 'Title', 'Author', 'Zipcode']
 
    return render_template("/search.html", choices=choices)



@app.route("/search", methods=['POST'])
def search_func():


    search_type = request.form.get('choice')
    search_terms = request.form.get('search')


    if  search_type == 'Keyword':

        if len(search_terms.split()) >= 1:
            book_result = Book.query.filter(Book.title.ilike('%{}%'.format(search_terms))|
                                        Book.author.ilike('%{}%'.format(search_terms))).all()

        if len(search_terms.split()) >= 2:

            words = search_terms.split()
            
            results =[]

            for word in words:

                result = Book.query.filter(Book.title.ilike('%{}%'.format(search_terms))|
                                        Book.author.ilike('%{}%'.format(search_terms))).all()

                results.append(result)
                
            book_result = set(results[0])
            for result in results:
                book_result = book_result & set(result)


    elif search_type == 'Title':

        if len(search_terms.split()) <= 1:

            book_result = Book.query.filter(Book.title.ilike('%{}%'.format(search_terms))).all()

        if len(search_terms.split()) >= 2:

            words = search_terms.split()

            results = []

            for word in words:

                result = Book.query.filter(Book.title.ilike('%{}%'.format(word))).all()

                results.append(result)

            book_result = set(results[0])
            for result in results:
                book_result = book_result & set(result)

    

    elif search_type == 'Author':

        if len(search_terms.split()) >= 1:
            book_result = Book.query.filter(Book.author.ilike('%{}%'.format(search_terms))).all()

        if len(search_terms.split()) >= 2:
            words = search_terms.split()
            
            results = []

            for word in words:

                result = Book.query.filter(Book.author.ilike('%{}%'.format(word))).all()

                results.append(result)

            book_result = set(results[0])
            for result in results:
                book_result = book_result & set(result)


    elif search_type == 'Zipcode':
        if len(search_terms) < 5 or len(search_terms) > 5:

            flash("Please  enter valid 5 digits Zipcode ")

            return redirect("/search")
        else:
            zipcode_result = User.query.filter(User.zipcode == search_terms).all()
            user = zipcode_result[0]
            book_result = Book.query.filter(Book.user_id == user.user_id).all()


    if book_result:
        
        flash("We have the book!")

        return render_template('search_result.html', book_result=book_result)
    else:

        flash("Sorry, book is no find, please search again.")

        return redirect("/search")


####################################################################################
#twilio SMS message 

@app.route("/request", methods=['POST'])
def request_book():

    user_request = request.form.get('book_id')

    print(user_request)

    if user_request:
        account_sid = os.environ["twilio_sid"]
        auth_token = os.environ["twilio_token"]

        user = User.query.get(session['user_id'])
        name = user.user_name
        email = user.email

        book = Book.query.get(user_request)
        title = book.title



        client = Client(account_sid, auth_token)

        message = client.messages.create(
                                      from_='+16503824264',
                                      body='Hello, my name is {}, I am interested your {} book, If it still available, please contact me at {} ?'.format(name, title, email),
                                      to='+15103040780'
                                  )

       

        flash('Your request had sent!')


        return redirect("/home")



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