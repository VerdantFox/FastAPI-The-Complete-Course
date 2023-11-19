from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DB_URL = "sqlite:///./todos_db.db"
# DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
# engine = create_engine(DB_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBDependency = Annotated[Session, Depends(get_db)]
