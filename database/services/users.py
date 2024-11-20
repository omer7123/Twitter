from psycopg2 import Error
from sqlalchemy import create_engine, select, func, distinct
from sqlalchemy.orm import sessionmaker, joinedload, selectinload, join, DeclarativeBase
from typing import List
from sqlalchemy.exc import NoResultFound
import bcrypt


from database.database import engine, session_factory

from fastapi import FastAPI, HTTPException
import uuid
from datetime import datetime

from database.models.users import User


class UserServiceDB:


    def register_user(self, id, username, email, password):
        with session_factory() as session:
            try:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user = User(id=id,
                             username=username,
                             email=email,
                             password=hashed_password.decode('utf-8'),
                             city="",
                             hobby="",
                             first_name="",
                             last_name="",
                             )
                session.add(user)
                session.commit()
                return 0
            except (Exception, Error) as error:
                # print(error)
                return -1

    def check_user(self, email, password):
        with session_factory() as session:
            try:
                user = session.query(User).filter_by(email=email).one()
                hashed_password = user.password.encode('utf-8')

                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    return 0
                else:
                    return -1

            except (Exception, Error) as error:
                print(error)
                return -1

    def get_user(self, email):
        with session_factory() as session:
            try:
                user = session.query(User).filter_by(email=email).one()

                return user

            except (Exception, Error) as error:
                print(error)
                return -1



user_service_db: UserServiceDB = UserServiceDB()