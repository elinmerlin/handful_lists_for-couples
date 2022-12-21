import os
from datetime import date

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Movies(Base):
    """ Creates a table to store the films to watch later """
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    movie = Column(String(30))


class Places(Base):
    """ Creates a table to store events/places to visit together """
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    place = Column(String(30))


class Grocery(Base):
    """ Creates a table to store shopping list """
    __tablename__ = "grocery"

    id = Column(Integer, primary_key=True)
    date = Column(String(10), default=date.today().strftime("%Y-%m-%d"))
    product = Column(String(20))
    bought = Column(String(10), default='🚫')


class Notes(Base):
    """ Creates a table to store nice little notes for each other """
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    note = Column(String(50))


if __name__ == '__main__':
    Base.metadata.create_all(engine)
