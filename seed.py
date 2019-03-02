
# from sqlalchemy import func
# from model import User
# from model import connect_to_db, db
# from server import app
# from model import Book


# def load_users():

#     print("Users")


#     User.query.delete()


#     for row in open("seed_data/u.user"):
#         row = row.rstrip()
#         user_id, user_name, phone_number, email, password, zipcode = row.split("|")

#         user = User(user_id=user_id, user_name=user_name, phone_number=phone_number, email=email, password=password, zipcode=zipcode)


#         db.session.add(user)
#     db.session.commit()


# def load_books():

#     print("Books")
#     for row in open("seed_data/u.book"):
#         # row = row.rstrip()
#         content = row.split("|")
#         book_id = content[0]
#         title = content[1]
#         author = content[2]
#         book_cover = content[3]
#         isbn = content[4]
#         book_availability = content[5]
#         book_note = content[6]



#         book = Book(book_id=book_id, title=title, author=author, ISBN=isbn, book_cover=book_cover, book_availability=book_availability, book_note=book_note)
        
#         db.session.add(book)
#     db.session.commit()


# if __name__ == "__main__":
#     connect_to_db(app)

#     # In case tables haven't been created, create them
#     db.create_all()

#     # Import different types of data
#     load_users()
#     load_books()



from sqlalchemy import func
from model import User
from model import Book
import datetime

from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, user_name, phone_number, email, password, zipcode = row.split("|")

        user = User(user_id=user_id,
                    user_name=user_name,
                    phone_number=phone_number,
                    email=email,
                    password=password,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()

def load_books():
    """Load users from u.user into database."""

    print("Books")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.book"):
        row = row.rstrip()
        book_id, title, author, isbn, book_cover, book_availability, book_note, user_id = row.split("|")

        book = Book(book_id=book_id, 
                    title=title,
                    author=author, 
                    ISBN=isbn,
                    book_cover=book_cover,
                    book_availability=True, 
                    book_note=book_note,
                    user_id=user_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(book)

    # Once we're done, we should commit our work
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_books()
    
    