from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.users.auth import get_menu, get_current_user
from app.users.dao import InventoryDAO
from app.users.models import User

from app.games.service import game_statistics, last_3_games


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/profile")
async def profile(request: Request, menu: list = Depends(get_menu), user_data: User = Depends(get_current_user)):
    game_stats = await game_statistics(user_data.id)
    last_games = await last_3_games(user_data.id)
    inventory_items = await InventoryDAO.find_item_from_user_all(user_data.id)
    return templates.TemplateResponse("profile.html", {
        "request": request, 
        "menu": menu, 
        "user_data": user_data,
        "inventory_items": inventory_items,
        "all_games_statistics": game_stats,
        "last_games": last_games
    })