from datetime import date

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

books =[
    {
        "id": 1,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "publish_date": "1988-01-01"
    },
    {
        "id": 2,
        "title": "The God of Small Things",
        "author": "Arundhati Roy",
        "publish_date": "1997-04-04"
    },
    {
        "id": 3,
        "title": "The White Tiger",
        "author": "Aravind Adiga",
        "publish_date": "2008-01-01"
    },
    {
        "id": 4,
        "title": "The Palace of Illusions",
        "author": "Chitra Banerjee Divakaruni",
        "publish_date": "2008-02-12"
    }
]

app = FastAPI()

@app.get("/book")
def get_book():
    return books

@app.get("/book/{book_id}")
def single_book(book_id: int):
    result = list(filter(lambda item: item["id"] == book_id, books))
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    return result[0]  # return the single book instead of a list


class Book(BaseModel):
    id: int
    title:str
    author: str
    publish_date:date
    
    
@app.post("/book")
def create_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book

class BookUpdate(BaseModel):
    title:str
    author: str
    publish_date:date

@app.put("/book/{book_id}")
def update_book(book_id: int, updated_book: BookUpdate):
    for index, item in enumerate(books):
        if item["id"] == book_id:
            books[index].update(updated_book)
            return books[index]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )
    
    
@app.delete("/book/{book_id}")
def delete_book(book_id: int):
    for index, item in enumerate(books):
        if item["id"] == book_id:
            deleted_book = books.pop(index)
            return {"message": "Book deleted", "book": deleted_book}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )