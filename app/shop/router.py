from fastapi import APIRouter, Request, HTTPException, status
from app.shop.dao import ShopDAO
from app.shop.service import check_buy, continuation_buy
from app.users.auth import get_current_user
from app.users.dao import InventoryDAO, UsersDAO
from app.shop.schemas import SShopBuy


router = APIRouter(
	prefix="/api/shop",
	tags=["API магазина"]
)

@router.post('/buy')
async def buy_item(request: Request, data_buy: SShopBuy):
    token = request.cookies.get('users_access_token')
    user_data = await get_current_user(token)
    id_user = await UsersDAO.find_id_on_username(user_data.username)
    item = await ShopDAO.find_by_id(data_buy.id_item)
    await check_buy(id_user, user_data, item)
    money = await continuation_buy(id_user, item)
    print(money)
    return {"status": 200, "money": money}