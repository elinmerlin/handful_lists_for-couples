import os
import datetime

from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///gs2.db")
# engine = create_engine(os.getenv("DATABASE_URL"))
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    movie = Column(String(30))


class Places(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    place = Column(String(30))


class Grocery(Base):
    __tablename__ = "grocery"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), default=datetime.date.today)
    product = Column(String(20))
    bought = Column(String(10), default='🚫')


class Notes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    note = Column(String(50))


if __name__ == '__main__':
    Base.metadata.create_all(engine)
