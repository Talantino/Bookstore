import sqlalchemy as orm
from database import Base


class Book(Base):
    __tablename__ = "books"
    id = orm.Column(orm.Integer, primary_key=True)
    title = orm.Column(orm.String)
    author = orm.Column(orm.String)
    description = orm.Column(orm.String)
    price = orm.Column(orm.Integer)

    def update(self, title: str = None, author: str = None, description: str=None, price: int=None):
        if not all([title, author, price, description]):
            return self
        self.title = title
        self.author = author
        self.description = description
        self.price = price
        return self


class User(Base):
    __tablename__ = "users"
    id = orm.Column(orm.Integer, primary_key=True)
    username = orm.Column(orm.String, unique=True)
    password = orm.Column(orm.String)
