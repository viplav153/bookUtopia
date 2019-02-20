import os
from twilio.rest import Client



account_sid = os.environ["twilio_sid"]
auth_token = os.environ["twilio_token"]


def get_user_info():

    user = User.query.get(session['user_id'])
    name = user.user_name
    email = user.email

    book = Book.query.get(book_id)
    title = book.book_id

client = Client(account_sid, auth_token)

message = client.messages.create(
                              from_='+16503824264',
                              body='Hello, my name is {}, I am interested your {}, If it available, please contact me at{}? ',
                              to='+14159106112'
                          )

print(message.sid)



def 