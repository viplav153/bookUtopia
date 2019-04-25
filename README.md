# BookUtopia
BookUtopia is a web application that provides users with a convenient and efficient platform to facilitate the exchange of second-hand books.

Users can simply enter their book ISBN numbers into the application, where the Google Book API is utilized to obtain relevant information including book cover, title, author, description, and more.  This information is then populated into an SQLAlchemy postgres database. Twilio API integration allows users to connect via SMS.  Registered users can search for books by title, author, keywords, or zip code, and the Google Map API helps users to visualize the search results. CRUD features allow users to manage their personal booklist.

Video Demo: https://youtu.be/eg-83beBiRY

##  Features

<p align="center">
  Home Page
  <br>
  <img width="460" height="300" src="https://media.giphy.com/media/SUFTlmyxli2G1tDoXI/giphy.gif">
</p>
 <br>
 <br>
<p align="center">
  Login & Register Page
  <br>
  <img width="460" height="300" src="https://media.giphy.com/media/IcuP5130xlemtvIMaN/giphy.gif">
</p>
<br>
 <br>
<p align="center">
  User logged in page with Available books list
  <br>
  <img width="460" height="300" src="https://media.giphy.com/media/U8epY7ODcq6Z8R9UlO/giphy.gif">
</p>
<br>
 <br>
<p align="center">
  Request a book & Book owner received the text notofication
  <br>
  <img width="460" height="300" src="https://media.giphy.com/media/W6QIH8piwJbcwMRPoU/giphy.gif">
</p>

<br>
 <br>
<p align="center">
  Add a book that user want to share with others by ISBN 
  <br>
  <img width="460" height="300" src="https://media.giphy.com/media/fUwvxkWPBeH3kCQqME/giphy.gif">
</p>

<br>
 <br>
<p align="center">
  Book lists management - Create& Read & Update & Delete
  <br>
  <img width="460" height="300" src="https://media.giphy.com/media/UQ6KjDEb0pX3RSeW07/giphy.gif">
</p>

<br>
 <br>
<p align="center">
  Book search by keyword, title, author or zipcode
  <br>
  <img width="460" height="300" src="https://media.giphy.com/media/LMcY86GSJRi0UBWsnV/giphy.gif">
</p>

## Tech Stack
* **Back-End**: - Python, Flask, Jinja, SQLAlchemy, PostgreSQL
* **Front-End**:- HTML/CSS, Bootstrap, JQuery, JavaScript, AJAX
* **APIS**: - Google Map, Google Books, Twillio


## Setup and installation
Clone repository:
```
$ git clone https://github.com/yparks/bookUtopia.git
```

Create a virtual environment in the directory:
```
$ virtualenv env
```
Activate virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt 
```
Create database:
```
$ createdb bookdb
```
Build database:
```
$ python3 -i model.py
db.create_all() 
```
Run app:
```
$ python3 server.py 
```
Navigate to localhost:5000 in browser

## Future Features
* Give recommendation for user based on their interests of the books by using Machine Learning 
* Implement React to user interfaces
