import requests
import os


key = os.environ["book_api_key"]
# headers = {"Authorization": 'Bearer ' + key}
# url = "https://www.googleapis.com/books/v1/volumes"
url = "https://www.googleapis.com/books/v1/volumes"

payload = {"q": "isbn: 978-1465474773", "key": key}

r = requests.get(url, params=payload)
# https://www.googleapis.com/auth/books

book_info = r.json()
print(book_info)
