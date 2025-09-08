import os
from typing import Annotated
import sqlite3

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from logging import getLogger


sqlite_file_name = os.environ["DATABASE_URL"]
# sqlite_file_name = ":memory:"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}


engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    print("creating database and tables...")
    try:
        SQLModel.metadata.create_all(engine)
        print("Database and tables created successfully.")

    except sqlite3.OperationalError as e:
        print("OperationalError:", e)
    except Exception as e:
        print("Error creating database and tables:", e)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
