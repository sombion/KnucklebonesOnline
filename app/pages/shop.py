from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.templating import Jinja2Templates

from app.shop.dao import ShopDAO
from app.users.auth import get_current_user, get_menu
from app.users.dao import InventoryDAO

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/shop")
async def home(request: Request, menu: list = Depends(get_menu)):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Вы не вошли в аккаунт")
    user_data = await get_current_user(token)
    
    if user_data:
        all_items = await ShopDAO.find_shop()
        user_items = await InventoryDAO.find_item_from_user(user_data.id)
        if not user_items:
            shop_items = all_items
        else:
            shop_items = [item_all for item_all in all_items if item_all['id'] not in {item_user['id_item'] for item_user in user_items}]
    else:
        shop_items = await ShopDAO.find_shop()
        
    shop_status = True
    if not shop_items:
        shop_status = False
    
    return templates.TemplateResponse("shop.html", {"request": request, "menu": menu, "shop_status": shop_status, "shop_items": shop_items, "user_data": user_data})