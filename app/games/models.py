from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Computed, ForeignKey
from app.database import Base

class Game(Base):
    __tablename__ = "game"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_pl1: Mapped[int] = mapped_column(ForeignKey("user.id"))
    id_pl2: Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    pl1_1_1: Mapped[int] = mapped_column(default=0)
    pl1_1_2: Mapped[int] = mapped_column(default=0)
    pl1_1_3: Mapped[int] = mapped_column(default=0)
    pl1_2_1: Mapped[int] = mapped_column(default=0)
    pl1_2_2: Mapped[int] = mapped_column(default=0)
    pl1_2_3: Mapped[int] = mapped_column(default=0)
    pl1_3_1: Mapped[int] = mapped_column(default=0)
    pl1_3_2: Mapped[int] = mapped_column(default=0)
    pl1_3_3: Mapped[int] = mapped_column(default=0)
    
    pl1_1: Mapped[int] = mapped_column(default=0)
    pl1_2: Mapped[int] = mapped_column(default=0)
    pl1_3: Mapped[int] = mapped_column(default=0)
    pl1_count: Mapped[int] = mapped_column(default=0)
    
    pl2_1_1: Mapped[int] = mapped_column(default=0)
    pl2_1_2: Mapped[int] = mapped_column(default=0)
    pl2_1_3: Mapped[int] = mapped_column(default=0)
    pl2_2_1: Mapped[int] = mapped_column(default=0)
    pl2_2_2: Mapped[int] = mapped_column(default=0)
    pl2_2_3: Mapped[int] = mapped_column(default=0)
    pl2_3_1: Mapped[int] = mapped_column(default=0)
    pl2_3_2: Mapped[int] = mapped_column(default=0)
    pl2_3_3: Mapped[int] = mapped_column(default=0)
    
    pl2_1: Mapped[int] = mapped_column(default=0)
    pl2_2: Mapped[int] = mapped_column(default=0)
    pl2_3: Mapped[int] = mapped_column(default=0)
    pl2_count: Mapped[int] = mapped_column(default=0)
    
    status_games: Mapped[str] = mapped_column(default="playing") # playing | error | ending
    id_pl_win: Mapped[int] = mapped_column(nullable=True)
    
    id_pl_move: Mapped[int]
    current_count: Mapped[int]
    