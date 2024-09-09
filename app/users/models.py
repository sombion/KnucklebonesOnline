from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.database import Base


class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    activate_url: Mapped[str] = mapped_column(default="/static/images/avatar/lamb-icon.png", nullable=True)
    username: Mapped[str]
    login: Mapped[str]
    hash_password: Mapped[str]
    trophies: Mapped[int] = mapped_column(default=0)
    money: Mapped[int] = mapped_column(default=100)
    
    is_user: Mapped[bool] = mapped_column(default=True, server_default='true', nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default='false', nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(default=False, server_default='false', nullable=False)
    

class Inventory(Base):
    __tablename__ = "inventory"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"))
    id_item: Mapped[int] = mapped_column(ForeignKey("shop_info.id"))
    