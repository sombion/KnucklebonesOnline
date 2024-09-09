from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ShopInfo(Base):
    __tablename__ = "shop_info"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    price: Mapped[int]
    url: Mapped[str]