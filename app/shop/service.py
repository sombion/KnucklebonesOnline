from fastapi import HTTPException, status
from app.shop.models import ShopInfo
from app.users.dao import InventoryDAO, UsersDAO
from app.users.models import User


async def check_buy(id_user: int, user_data: User, item_data: ShopInfo) -> bool:
    if item_data == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Предмет не найден")
    if not await InventoryDAO.find_by_id(id_user):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Предмет уже куплен")
    if user_data.money < item_data.price:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Недостаточно золота")
    return True
    
async def continuation_buy(id_user: int, item_data: ShopInfo) -> int:
    money = await UsersDAO.edit_money(id_user=id_user, count=item_data.price)
    await InventoryDAO.add_item(id_user=id_user, id_item=item_data.id)
    return money
    