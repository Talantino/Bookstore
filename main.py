from database import get_db
from fastapi import FastAPI, Depends
from schemas import BookCreate, BookRetrieve, UserSchema
from models import Book, User
from typing import List
from sqlalchemy.orm import Session
from database import Base, engine
from user_authen import create_access_token, get_current_user
from sqlalchemy import update
from user_authen import decode_access_token

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/books/", response_model=List[BookRetrieve])
async def get_books(db=Depends(get_db)):
    books = db.query(Book).all()
    return list(books)


@app.post("/books/")
async def create_books(item: BookCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    item = dict(item)
    item['author'] = user.username
    book = Book(**dict(item))
    db.add(book)
    db.commit()
    # print(user.username)
    return item


@app.put("/books/{id}", response_model=BookRetrieve)
async def update_books(id : int, item:BookCreate, db: Session = Depends(get_db)):
    updated = update(Book).where(Book.id == id).values(**dict(item))
    db.execute(updated)
    db.commit()
    return {"message": "updated successfully"}


@app.delete("/books/{id}")
async def delete_books(id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id).delete()
    db.commit()
    return {"message": f"book {id} deleted successfully"}


@app.post("/users/", response_model=UserSchema)
async def sign_up(user: UserSchema, db:Session=Depends(get_db)):
    created_user = User(**dict(user))
    db.add(created_user)
    db.commit()
    return user


@app.post("/users/sign_in")
async def sign_in(user: UserSchema, db: Session=Depends(get_db)):
    user_exists = db.query(User).filter(User.username == user.username).first()
    if not user_exists:
        return {"message": "user does not exists"}

    if user.password != user_exists.password:
        return {"message": "password is incorrect"}
    return {"message": {"access token": create_access_token(dict(user))}}


@app.get("/users/")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.post('/users/decode_jwt')
async def decode_jwt(token:str):
    return decode_access_token(token)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)
