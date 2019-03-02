for row in open("seed_data/u.book"):
        
        # row = row.rstrip()
        # print(row)
        # print (len(row))
        # row = row.split("|")
        # print(row)
        # print (len(row))
        # row = tuple(row)

    # row = row.rstrip()
    content = row.split("|")
    book_id = content[0]
    title = content[1]
    author = content[2]
    book_cover = content[3]
    isbn = content[4]
    book_availability = content[5]
    book_note = content[6]




        
    book_id, title, author, ISBN, book_cover, book_availability, book_note = row
    
    print(row)