from app.dao.base import BaseDAO
from app.users.models import User, Inventory
from app.shop.models import ShopInfo
from app.database import async_session_maker
from sqlalchemy import insert, select, update

 
class UsersDAO(BaseDAO):
    model = User
    
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_id_on_username(cls, username: str):
        async with async_session_maker() as session:
            query = select(cls.model.id).filter_by(username=username)
            result = await session.execute(query)
            return result.scalar()
        
    @classmethod
    async def add_user(cls, username: str, login: str, hash_password: str):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
				username=username,
				login=login,
    			hash_password=hash_password
			)
            await session.execute(stmt)
            await session.commit()
            
    @classmethod
    async def edit_user(cls, id_user, activate_url):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id==id_user).values(
                activate_url=activate_url
            )
            await session.execute(stmt)
            await session.commit()
    
    @classmethod
    async def edit_money(cls, id_user: int, count: int):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id==id_user).values(
                money=cls.model.money-count
            ).returning(cls.model.money)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
    
    @classmethod
    async def give_award_win(cls, id_user: int, trophies: int, money: int):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id==id_user).values(
                trophies=cls.model.trophies+trophies,
                money=cls.model.money+money,
            )
            await session.execute(stmt)
            await session.commit()
            
    @classmethod
    async def give_award_lose(cls, id_user: int, trophies: int, money: int):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id==id_user).values(
                trophies=cls.model.trophies-trophies,
                money=cls.model.money+money,
            )
            await session.execute(stmt)
            await session.commit()
        
class InventoryDAO(BaseDAO):
    model = Inventory
    
    @classmethod
    async def find_item_from_user_and_id(cls, id_user: int, id_item: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id_user=id_user, id_item=id_item)
            result = await session.execute(query)
            return result.mappings().all()
    
    @classmethod
    async def find_item_from_user(cls, id_user):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id_user=id_user)
            result = await session.execute(query)
            return result.mappings().all()
    
    @classmethod
    async def find_item_from_user_all(cls, id_user):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns, ShopInfo.__table__.columns).join(ShopInfo, cls.model.id_item==ShopInfo.id).filter(cls.model.id_user==id_user)
            result = await session.execute(query)
            return result.mappings().all()
    
    @classmethod
    async def add_item(cls, id_user: int, id_item: int):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
                id_user=id_user,
                id_item=id_item
            )
            await session.execute(stmt)
            await session.commit()