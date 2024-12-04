from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


engine = create_engine(url="postgresql://postgres:password@db:5432/dbname", echo=False)
#engine = create_engine(url="postgresql://postgres:password@localhost:5432/dbname", echo=False)

session_factory = sessionmaker(engine)

class Base(DeclarativeBase):
    pass
