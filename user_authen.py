from datetime import timedelta, datetime
import jwt
from database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models import User

SECRET_KEY = "some ux"


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=2)
    to_encode.update({"expires": expire.strftime("%Y-%m-%d %H: %M:%S")})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

    return encoded_jwt


def decode_access_token(token: str):
    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="invalid token")
    return user


def get_current_user(token: str, db: Session = Depends(get_db)):
    user_data = decode_access_token(token)
    user = db.query(User).filter(User.username == user_data['username']).first()
    if not user:
        return False
    return user
