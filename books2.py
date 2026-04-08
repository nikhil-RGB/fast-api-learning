from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
app=FastAPI()
# An object of class Book will be used in this updated model of the API.
class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int

    def __init__(self, id:int, title:str, author:str, description:str, rating:int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id:Optional[int]= Field(description="ID is not needed on create",default=None) 
    title:str=Field(min_length=3)
    author:str=Field(min_length=1)
    description:str=Field(min_length=1,max_length=100)

    rating:int=Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {                
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                'published_date': 2029
            }
        }
    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1)
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/books/")
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
