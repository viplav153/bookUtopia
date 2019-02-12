"""Models and database functions for LotOfBooks project"""

from flask_sqlalchemy import SQLAlchemy


# This is the connection to the PostgreSQL database, we are getting this through
# the flask_sqlalchemy helper library. On this, we can find the 'session' object, 
# where we do most of our interactions (like commiting, ect)

db = SQLAlchemy()


#############################################################
#Model definitions


class User(db.Model):
    """User of the LofOfBook website"""

    __tablename__ = "users"


    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)

    #books = db.relationship('Book')

    def __repr__(self):
        """Provied helpful representation when printed"""

        return ('User user_id={} email={}'.format(self.user_id, self.email))

class Book(db.Model):
    """Book table for the LotOfBook webiste"""

    __tablename__ = "books"

    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    #Connection with the User table, should I use "user insstead of users？"
    # user = db.relationship("User")

    user = db.relationship("User", backref='books')


    def __repr__(self):

        return ('Book title={}, author={}'.format(self.title, self.author))


##########################################################3

def  init_app():
    #So that we can use Flask-SQLAlchemy, we'll make a Flask app

    from flask import Flask
    app = Flask(__name__)


    connect_to_db(app)

    print("Connected to DB")


def connect_to_db(app):
    """Connect to our database to our Flask app"""


    #Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///bookdb'

    #Why false？ no need to debugging?
    #app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


#What is the purpose of this ?
if __name__ == "__main__":


    init_app()



























