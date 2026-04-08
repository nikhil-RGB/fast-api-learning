from fastapi import FastAPI, Body
app=FastAPI()
BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/authors/{author_name}")
async def read_book_from_author(author_name:str):

    all_books=[]
    for book in BOOKS:
        if book['author'].casefold() == author_name.casefold():
            all_books.append(book)
    return all_books

@app.get("/books/author_query/")
async def read_book_from_author_query(author_name:str):
    all_books=[]
    for book in BOOKS:
        if book['author'].casefold() == author_name.casefold():
            all_books.append(book)
    return all_books

@app.get("/books/")
async def read_book_by_category(category: str):
    all_books=[]
    for book in BOOKS:
        if book['category'].casefold() == category.casefold():
            all_books.append(book)
    return all_books



@app.get("/books/titles/{dynamic_param}")
async def read_book(dynamic_param: str):
    for books in BOOKS:
        if books['title'].casefold() == dynamic_param.casefold():
            return books['title'].casefold()
    return {"message": "Book not found"}

@app.get("/books/{author_name}/")
async def read_book_by_category_author(author_name: str,category:str):
    books_to_return=[]
    for book in BOOKS:
        if book['author'].casefold()==author_name.casefold() and book['category'].casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return
    
@app.get("/books/{dynamic_param}")
async def readBookDynamically(dynamic_param: str):
    return {"book": dynamic_param}

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

@app.put("/books/update_book_category")
async def update_book_category(book_title: str, new_category: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS[i]['category'] = new_category
    return {"message": "Book category updated"}

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break