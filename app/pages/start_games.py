import random
from time import sleep
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.games.dao import GameDAO
from app.games.service import check_start_games
from app.games.dao import GameDAO
from app.users.auth import get_current_user, get_menu
from app.users.models import User


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

class ConnectionGame:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.broadcast()
        if len(self.active_connections) == 2:
            await self.create_games()

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self):
        for connection in self.active_connections:
            if len(self.active_connections) == 2:
                data_dict = {"count": len(self.active_connections), "text": "Противник найден..."}
            elif len(self.active_connections) > 2:
                data_dict = {"count": len(self.active_connections), "text": "Ошибка..."}
            else:
                data_dict = {"count": len(self.active_connections), "text": "Поиск противника..."}
            data_dict['redirect'] = False
            await connection.send_json(data_dict)
                
            
    async def create_games(self):
        users_id = []
        for connection in self.active_connections:
            token = connection.cookies['users_access_token']
            user = await get_current_user(token=token)  
            users_id.append(user.id)
        print(users_id)
        try:
            users_id = sorted(users_id)
            id = await GameDAO.create_game(id_pl1=users_id[0], id_pl2=users_id[1], id_pl_move=random.randint(users_id[0], users_id[1]), current_count=random.randint(1, 6))
            for connection in self.active_connections:
                data_dict = {
                    "redirect": True,
                    "id": id
                }
                await connection.send_json(data_dict)
        except Exception:
            print("Error")

manager = ConnectionGame()

@router.get("/start-games")
async def home(request: Request, user_data: User = Depends(get_current_user)):
    game_data = await GameDAO.find_game(user_data.id)
    if game_data:
        return RedirectResponse(f"/games/{game_data[0]['id']}")
    return templates.TemplateResponse("start_games.html", {"request": request})

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
    except WebSocketDisconnect:
        manager.disconnect(websocket)