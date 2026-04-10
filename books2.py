from typing import Optional
from datetime import date
from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app=FastAPI()
# An object of class Book will be used in this updated model of the API.
class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int
    published_date: int

    def __init__(self, id:int, title:str, author:str, description:str, rating:int, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date= published_date

class BookRequest(BaseModel):
    id:Optional[int]= Field(description="ID is not needed on create",default=None) 
    title:str=Field(min_length=3)
    author:str=Field(min_length=1)
    description:str=Field(min_length=1,max_length=100)

    rating:int=Field(gt=0, lt=6)
    published_date:int=Field(gt=1800, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {                
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2021
            }
        }
    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5,2013),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5,2012),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5,2014),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2,2015),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3,2016),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1,1998)
]

@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS



@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_book_by_id(book_id:int=Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found!")

@app.get("/books/date/{p_date}",status_code=status.HTTP_200_OK)
async def read_books_by_date(p_date:int=Path(gt=1800, lt=2031)):
    books_to_return=[]
    for book in BOOKS:
        if book.published_date==p_date:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_book_by_rating(rating: int= Query(gt=0,lt=6)):
    result_books=[]
    for book in BOOKS:
        if rating == book.rating:
            result_books.append(book)
    return result_books


@app.post("/books/",status_code=status.HTTP_201_CREATED)
async def create_book(new_book_req: BookRequest):
    new_book=Book(**new_book_req.dict())
    BOOKS.append(find_book_id(new_book))
    return f"{new_book_req.title} has been added"

def find_book_id(book:Book):
    if len(BOOKS)>0:
        book.id= BOOKS[-1].id + 1
    else:
        book.id=1
    return book
#Update book id
@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT) 
async def update_book(updated_book: BookRequest):
    
    for i in range(len(BOOKS)):
        if BOOKS[i].id == updated_book.id:
            BOOKS[i]= updated_book
    raise HTTPException(status_code=404,detail="No book updated")

#Delete book by ID
@app.delete("/books/delete/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int=Path(gt=0)):
    flag=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            flag=True
            break
    if not flag:
        raise HTTPException(status_code=404,detail="No book deleted")
    

