from datetime import date
from typing import Annotated, Any

from fastapi import FastAPI, Path, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()


class NotFoundException(Exception):
    def __init__(self, model: type[BaseModel], id: int | None = None) -> None:
        if not issubclass(model, BaseModel):
            raise TypeError("model must be a pydantic BaseModel")
        self.model: type[BaseModel] = model
        self.id: int | None = id


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(
    _request: Request, exc: NotFoundException
) -> JSONResponse:
    id_str = f" with id={exc.id!r}" if exc.id else ""
    return JSONResponse(
        status_code=404, content={"detail": f"{exc.model.__name__}{id_str} not found"}
    )


POST_BOOK_CONFIG = ConfigDict(
    json_schema_extra={
        "examples": [
            {
                "title": "A new book",
                "author": "Some Author",
                "description": "A new description",
                "publish_date": "2021-01-01",
                "rating": 5,
            }
        ]
    }
)
GET_BOOK_CONFIG = POST_BOOK_CONFIG.copy()
GET_BOOK_CONFIG["json_schema_extra"]["examples"][0]["id"] = 1  # type: ignore[index]


def not_found_response(model: type[BaseModel]) -> dict[int | str, dict[str, Any]]:
    if not issubclass(model, BaseModel):
        raise TypeError("model must be a pydantic BaseModel")
    return {
        404: {
            "description": "Not found",
            "content": {
                "application/json": {
                    "example": {"detail": f"{model.__name__} not found"}
                }
            },
        }
    }


class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    publish_date: date
    rating: int

    model_config = GET_BOOK_CONFIG


class PostBookIn(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, le=5)
    publish_date: date

    model_config = POST_BOOK_CONFIG


class PutBookIn(BaseModel):
    title: str | None = Field(min_length=3, default=None)
    author: str | None = Field(min_length=1, default=None)
    description: str | None = Field(min_length=1, max_length=100, default=None)
    rating: int | None = Field(gt=0, le=5, default=None)
    publish_date: date | None = None

    model_config = POST_BOOK_CONFIG


BOOKS: list[Book] = [
    Book(
        id=1,
        title="Computer Science Pro",
        author="codingwithroby",
        description="A very nice book",
        rating=5,
        publish_date=date(2021, 1, 1),
    ),
    Book(
        id=2,
        title="Be fast with FastAPI",
        author="codingwithroby",
        description="A great book!",
        rating=5,
        publish_date=date(2021, 10, 14),
    ),
    Book(
        id=3,
        title="Master Endpoints",
        author="codingwithroby",
        description="An awesome book",
        rating=5,
        publish_date=date(2021, 10, 24),
    ),
    Book(
        id=4,
        title="HP1",
        author="Author 1",
        description="Book description",
        rating=4,
        publish_date=date(2022, 5, 24),
    ),
    Book(
        id=5,
        title="HP2",
        author="Author 2",
        description="Book description",
        rating=1,
        publish_date=date(1995, 2, 3),
    ),
    Book(
        id=6,
        title="HP3",
        author="Author 3",
        description="Book description",
        rating=1,
        publish_date=date(2005, 2, 3),
    ),
]


@app.get("/books")
async def get_books(
    min_rating: Annotated[
        int,
        Query(description="Integer between 0 and 5.", example=5, ge=0, le=5),
    ] = None,
    earliest_publish_date: Annotated[
        date,
        Query(description="date in format 'YEAR-MONTH-DAY'.", example="2021-01-01"),
    ] = None,
    latest_publish_date: Annotated[
        date,
        Query(description="date in format 'YEAR-MONTH-DAY'.", example="2021-01-01"),
    ] = None,
) -> list[Book]:
    books = BOOKS.copy()

    if min_rating:
        books = [book for book in books if book.rating >= min_rating]
    if earliest_publish_date:
        books = [book for book in books if book.publish_date > earliest_publish_date]
    if latest_publish_date:
        books = [book for book in books if book.publish_date < latest_publish_date]
    return books


@app.get(
    "/books/{book_id}",
    responses=not_found_response(Book),
)
async def get_book(book_id: Annotated[int, Path(ge=1)]) -> Book:
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise NotFoundException(model=Book, id=book_id)


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(new_book: PostBookIn) -> Book:
    book = Book(**new_book.model_dump(), id=gen_new_book_id())
    BOOKS.append(book)
    return book


def gen_new_book_id() -> int:
    return BOOKS[-1].id + 1 if BOOKS else 1


@app.patch(
    "/books/{book_id}",
    responses=not_found_response(Book),
)
async def update_book(book_id: Annotated[int, Path(ge=1)], new_book: PutBookIn) -> Book:
    for i, book in enumerate(BOOKS.copy()):
        if book.id != book_id:
            continue
        updated_book = book.model_copy(update=new_book.model_dump(exclude_unset=True))
        BOOKS[i] = updated_book
        return updated_book
    raise NotFoundException(model=Book, id=book_id)


@app.delete(
    "/books/{book_id}",
    responses=not_found_response(Book),
)
async def delete_book(book_id: Annotated[int, Path(ge=1)]) -> Book:
    for i, book in enumerate(BOOKS.copy()):
        if book.id != book_id:
            continue
        del BOOKS[i]
        return book
    raise NotFoundException(model=Book, id=book_id)
