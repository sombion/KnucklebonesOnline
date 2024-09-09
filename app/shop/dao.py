from app.dao.base import BaseDAO
from app.shop.models import ShopInfo
from sqlalchemy import and_, insert, or_, select, update
from app.database import async_session_maker


class ShopDAO(BaseDAO):
    model = ShopInfo
    
    @classmethod
    async def find_shop(cls):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by().order_by(cls.model.price)
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def find_id_from_url(cls, url: str):
        async with async_session_maker() as session:
            query = select(cls.model.id).filter_by(url=url)
            result = await session.execute(query)
            return result.scalar()