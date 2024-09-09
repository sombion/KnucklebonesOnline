from app.dao.base import BaseDAO
from app.games.models import Game
from sqlalchemy import and_, insert, or_, select, update
from app.database import async_session_maker


class GameDAO(BaseDAO):
    model = Game
    
    @classmethod
    async def create_game(cls, id_pl1, id_pl2, id_pl_move, current_count):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
				id_pl1 = id_pl1,  
    			id_pl2 = id_pl2,  
     			id_pl_win = None,
       			id_pl_move = id_pl_move,  
          		current_count = current_count
            ).returning(cls.model.id)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
            
    @classmethod
    async def update_game(cls, id_game, **update_data):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id==id_game, cls.model.status_games=="playing").values(update_data)
            await session.execute(stmt)
            await session.commit()
    
    @classmethod
    async def find_game(cls, id_user: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(
				or_(
					cls.model.id_pl1 == id_user,
					cls.model.id_pl2 == id_user
				),
				cls.model.status_games == "playing"
            )
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def find_end_game(cls, id_user: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(
                or_(
                    cls.model.id_pl1 == id_user,
                    cls.model.id_pl2 == id_user
                ),
                cls.model.status_games == "ending"
            ).order_by(cls.model.id.desc())
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def find_all_game_playing(cls):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(status_games = "playing")
            result = await session.execute(query)
            return result.mappings().all()