import pytest
from fastapi import status
from sqlalchemy import select

from src.models.books import Book
from src.models.sellers import Seller

API_V1_URL_PREFIX = "/api/v1/books"


async def create_seller(db_session) -> Seller:
    seller = Seller(first_name="Ivan", last_name="Ivanov", email="ivan@example.com", password="qwerty")
    db_session.add(seller)
    await db_session.flush()
    return seller


@pytest.mark.asyncio()
async def test_create_book(db_session, async_client):
    seller = await create_seller(db_session)
    data = {"title": "Clean Architecture", "author": "Robert Martin", "count_pages": 300, "year": 2025, "seller_id": seller.id}
    response = await async_client.post(f"{API_V1_URL_PREFIX}/", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    result_data = response.json()
    assert result_data.pop("id", None) is not None
    assert result_data == {"title": "Clean Architecture", "author": "Robert Martin", "pages": 300, "year": 2025, "seller_id": seller.id}


@pytest.mark.asyncio()
async def test_get_books(db_session, async_client):
    seller = await create_seller(db_session)
    book = Book(author="Pushkin", title="Eugeny Onegin", year=2021, pages=104, seller_id=seller.id)
    db_session.add(book)
    await db_session.flush()
    response = await async_client.get(f"{API_V1_URL_PREFIX}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["books"][0]["seller_id"] == seller.id


@pytest.mark.asyncio()
async def test_delete_book(db_session, async_client):
    seller = await create_seller(db_session)
    book = Book(author="Lermontov", title="Mtziri", pages=510, year=2024, seller_id=seller.id)
    db_session.add(book)
    await db_session.flush()
    response = await async_client.delete(f"{API_V1_URL_PREFIX}/{book.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    all_books = await db_session.execute(select(Book))
    assert len(all_books.scalars().all()) == 0
