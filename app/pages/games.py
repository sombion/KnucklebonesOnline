from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect, HTTPException, status
from fastapi.templating import Jinja2Templates
from app.games.dao import GameDAO
from app.users.auth import get_current_user, get_menu, give_awards
from app.games.service import create_dict, make_move

from app.users.models import User
from app.users.dao import UsersDAO


router = APIRouter(
    prefix="/games",
    tags=["Игры"],
)

templates = Jinja2Templates(directory="app/templates")


class ConnectionGame:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def ws_make_move(self, number: int, id_game: int, user: User, websocket: WebSocket):
        game_data = await GameDAO.find_by_id(id_game)
        if game_data.id_pl_move != user.id:
            return {"detail": "Игрок не может сделать ход"}
        await make_move(number, id_game, user.id)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            token = connection.cookies['users_access_token']
            user = await get_current_user(token=token)  
            game_data = await GameDAO.find_by_id(data["id_game"])
            
            if user.id == game_data.id_pl1:
                dict_data = await create_dict(
                    id_pl=user.id, 
					pl_name=user.username,
					id_pl_move=game_data.id_pl_move, 
					pl_1_3_temp=[
						game_data.pl1_1_1, game_data.pl1_1_2, game_data.pl1_1_3,
						game_data.pl1_2_1, game_data.pl1_2_2, game_data.pl1_2_3,
						game_data.pl1_3_1, game_data.pl1_3_2, game_data.pl1_3_3,
					], 
					pl_1_2_3=[game_data.pl1_1, game_data.pl1_2, game_data.pl1_3],
					pl_count=game_data.pl1_count,
					op_name="...",
					op_1_3_temp=[
						game_data.pl2_1_1, game_data.pl2_1_2, game_data.pl2_1_3,
						game_data.pl2_2_1, game_data.pl2_2_2, game_data.pl2_2_3,
						game_data.pl2_3_1, game_data.pl2_3_2, game_data.pl2_3_3,
					], 
					op_1_2_3=[game_data.pl2_1, game_data.pl2_2, game_data.pl2_3], 
					op_count=game_data.pl2_count,
					current_count=game_data.current_count
				)
            else: 
                dict_data = await create_dict(
					id_pl=user.id, 
					pl_name=user.username,
					id_pl_move=game_data.id_pl_move, 
					pl_1_3_temp=[
						game_data.pl2_1_1, game_data.pl2_1_2, game_data.pl2_1_3,
						game_data.pl2_2_1, game_data.pl2_2_2, game_data.pl2_2_3,
						game_data.pl2_3_1, game_data.pl2_3_2, game_data.pl2_3_3,
					],
					pl_1_2_3=[game_data.pl2_1, game_data.pl2_2, game_data.pl2_3],
					pl_count=game_data.pl2_count,
					op_name="...",
					op_1_3_temp=[
						game_data.pl1_1_1, game_data.pl1_1_2, game_data.pl1_1_3,
						game_data.pl1_2_1, game_data.pl1_2_2, game_data.pl1_2_3,
						game_data.pl1_3_1, game_data.pl1_3_2, game_data.pl1_3_3,
					],
					op_1_2_3=[game_data.pl1_1, game_data.pl1_2, game_data.pl1_3],
					op_count=game_data.pl1_count,
					current_count=game_data.current_count
				)
                
            dict_data['status_games'] = game_data.status_games
            if game_data.status_games == "ending":
                if game_data.id_pl_win == user.id:
                    dict_data['pl_win'] = "Вы победили"
                elif game_data.id_pl_win == 0:
                    dict_data['pl_win'] = "Ничья"
                else:
                    dict_data['pl_win'] = "Вы проиграли"
            await connection.send_json(dict_data)
            

manager = ConnectionGame()


@router.get("/{id_games}")
async def games_page(request: Request, id_games: int, user_data: User = Depends(get_current_user), menu: list = Depends(get_menu)):
    game_data = await GameDAO.find_by_id(id_games)
    if not game_data:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Игра не найдена")
    if not (user_data.id in [game_data.id_pl1, game_data.id_pl2]):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Вы не участвует в данной игре")
    if user_data.id == game_data.id_pl1:
        op_user = await UsersDAO.find_by_id(game_data.id_pl2)
        op_name = op_user.username
        dict_data = await create_dict(
			id_pl=user_data.id, 
			pl_name=user_data.username,
			id_pl_move=game_data.id_pl_move, 
			pl_1_3_temp=[
				game_data.pl1_1_1, game_data.pl1_1_2, game_data.pl1_1_3,
				game_data.pl1_2_1, game_data.pl1_2_2, game_data.pl1_2_3,
				game_data.pl1_3_1, game_data.pl1_3_2, game_data.pl1_3_3,
			], 
			pl_1_2_3=[game_data.pl1_1, game_data.pl1_2, game_data.pl1_3],
			pl_count=game_data.pl1_count,
   			op_name=op_name,
			op_1_3_temp=[
				game_data.pl2_1_1, game_data.pl2_1_2, game_data.pl2_1_3,
				game_data.pl2_2_1, game_data.pl2_2_2, game_data.pl2_2_3,
				game_data.pl2_3_1, game_data.pl2_3_2, game_data.pl2_3_3,
			], 
			op_1_2_3=[game_data.pl2_1, game_data.pl2_2, game_data.pl2_3], 
			op_count=game_data.pl2_count,
			current_count=game_data.current_count
		)
    else: 
        op_user = await UsersDAO.find_by_id(game_data.id_pl1)
        op_name = op_user.username
        dict_data = await create_dict(
			id_pl=user_data.id, 
			pl_name=user_data.username,
			id_pl_move=game_data.id_pl_move, 
			pl_1_3_temp=[
				game_data.pl2_1_1, game_data.pl2_1_2, game_data.pl2_1_3,
				game_data.pl2_2_1, game_data.pl2_2_2, game_data.pl2_2_3,
				game_data.pl2_3_1, game_data.pl2_3_2, game_data.pl2_3_3,
			],
			pl_1_2_3=[game_data.pl2_1, game_data.pl2_2, game_data.pl2_3],
			pl_count=game_data.pl2_count,
            op_name=op_name,
            op_1_3_temp=[
				game_data.pl1_1_1, game_data.pl1_1_2, game_data.pl1_1_3,
				game_data.pl1_2_1, game_data.pl1_2_2, game_data.pl1_2_3,
				game_data.pl1_3_1, game_data.pl1_3_2, game_data.pl1_3_3,
			],
            op_1_2_3=[game_data.pl1_1, game_data.pl1_2, game_data.pl1_3],
			op_count=game_data.pl1_count,
   			current_count=game_data.current_count
		)
    dict_data['request'] = request
    dict_data['pl_url'] = user_data.activate_url
    dict_data['op_url'] = op_user.activate_url
    dict_data['id_game'] = id_games
    dict_data['menu'] = menu
    dict_data['status_games'] = game_data.status_games
    if game_data.id_pl_win == user_data.id:
        dict_data['pl_win'] = "Вы победили"
    elif game_data.id_pl_win == 0:
        dict_data['pl_win'] = "Ничья"
    else:
        dict_data['pl_win'] = f"Вы проиграли"
    return templates.TemplateResponse("games.html", dict_data)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            user = await UsersDAO.find_one_or_none(username=data['user_name'])
            await manager.ws_make_move(data["number"], data["id_game"], user, websocket)
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # print(data['user_name'])
        # Победа другого игрока