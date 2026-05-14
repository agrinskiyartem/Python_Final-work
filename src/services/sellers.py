from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.sellers import Seller
from src.schemas.sellers import IncomingSeller, UpdateSeller


class SellerService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_seller(self, seller: IncomingSeller) -> Seller:
        new_seller = Seller(**seller.model_dump())
        self.session.add(new_seller)
        await self.session.flush()
        return new_seller

    async def get_all_sellers(self) -> list[Seller]:
        result = await self.session.execute(select(Seller))
        return result.scalars().all()

    async def get_single_seller(self, seller_id: int) -> Seller | None:
        result = await self.session.execute(
            select(Seller).options(selectinload(Seller.books)).where(Seller.id == seller_id)
        )
        return result.scalar_one_or_none()

    async def update_seller(self, seller_id: int, seller_data: UpdateSeller) -> Seller | None:
        seller = await self.session.get(Seller, seller_id)
        if not seller:
            return None

        seller.first_name = seller_data.first_name
        seller.last_name = seller_data.last_name
        seller.email = seller_data.email
        await self.session.flush()
        return seller

    async def delete_seller(self, seller_id: int) -> bool:
        seller = await self.session.get(Seller, seller_id)
        if not seller:
            return False
        await self.session.delete(seller)
        return True
