from pydantic import BaseModel
from pydantic import validator


class BaseBook(BaseModel):
    title: str
    author: str
    price: int


class BookCreate(BaseBook):
    description: str


class BookRetrieve(BaseBook):
    id: int
    description: str


class UserSchema(BaseModel):
    username: str
    password: str

    @validator('password')
    def validate_password(cls, password):
        min_length = 8
        errors = ''
        if len(password) < min_length:
            errors += 'Password must be at least 8 characters long. '
        if not any(character.islower() for character in password):
            errors += 'Password should contain at least one lowercase character.'
        if errors:
            raise ValueError(errors)

        return password
