import random

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status

from app.games.dao import GameDAO
from app.games.schemas import SGame
from app.users.auth import get_current_admin_user, get_current_user
from app.users.models import User
from app.games.service import check_start_games

router = APIRouter(
	prefix="/api/game",
	tags=["API игры"]
)


@router.get("/all-playing-games")
async def all_playing_games(user_data: User = Depends(get_current_admin_user)):
    result = await GameDAO.find_all_game_playing()
    return result

@router.get("/all-games")
async def all_games(user_data: User = Depends(get_current_admin_user)):
    result = await GameDAO.find_all()
    return result

@router.post("/create-games")
async def create_games(game_data: SGame, user_data: User = Depends(get_current_admin_user)):
    if not await check_start_games(game_data.id_pl1, game_data.id_pl2):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже играет")
    await GameDAO.create_game(game_data.id_pl1, game_data.id_pl2, random.randint(game_data.id_pl1, game_data.id_pl2), random.randint(1, 6))
    return {"detail": "Игра успешно создана"}