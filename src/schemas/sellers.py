from pydantic import BaseModel

from .books import ReturnedBook


class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: str


class IncomingSeller(BaseSeller):
    password: str


class UpdateSeller(BaseModel):
    first_name: str
    last_name: str
    email: str


class ReturnedSeller(BaseSeller):
    id: int


class ReturnedSellerWithBooks(ReturnedSeller):
    books: list[ReturnedBook]


class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]
