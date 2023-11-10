from fastapi import Body, FastAPI

app = FastAPI()

BOOKS: list[dict[str, str]] = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]


@app.get("/books")
async def get_books(category: str = "", author: str = "") -> list[dict[str, str]]:
    """Get all books"""
    books = BOOKS.copy()
    if category:
        books = [
            book
            for book in books
            if book.get("category", "").casefold() == category.casefold()
        ]
    if author:
        books = [
            book
            for book in books
            if book.get("author", "").casefold() == author.casefold()
        ]
    return books


@app.get("/books/{book_title}")
async def get_book(book_title: str) -> dict[str, str] | None:
    """Get a book by title"""
    for book in BOOKS:
        if book.get("title", "").casefold() == book_title.casefold():
            return book
    return None


@app.post("/books/create-book")
async def create_book(new_book=Body()) -> dict[str, str]:
    BOOKS.append(new_book)
    return new_book


@app.patch("/books/{book_title}")
async def update_book(book_title: str, book_update=Body()) -> dict[str, str] | None:
    for book in BOOKS:
        if book.get("title", "").casefold() == book_title.casefold():
            book.update(book_update)
            return book
    return None


@app.delete("/books/{book_title}")
async def delete_book(book_title: str) -> dict[str, str] | None:
    for i, book in enumerate(BOOKS.copy()):
        if book.get("title", "").casefold() == book_title.casefold():
            return BOOKS.pop(i)
    return None
