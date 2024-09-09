import random

from app.games.dao import GameDAO
from app.users.auth import give_awards
from app.users.dao import UsersDAO


async def check_start_games(id_pl1: int, id_pl2: int) -> bool:
	if await GameDAO.find_game(id_pl1):
		return False
	if await GameDAO.find_game(id_pl2):
		return False
	return True

async def game_statistics(id_user: int) -> dict:
    games_data = await GameDAO.find_end_game(id_user)
    total_games = 0
    wins = 0
    losses = 0
    draw = 0
    max_score = 0
    total_score = 0
    for game in games_data:
        total_games += 1
        
        # Определение побед и поражений
        if game['id_pl_win'] == id_user:
            wins += 1
        elif game['id_pl_win'] == 0:
            draw += 0
        else:
            losses += 1
            
        if game['id_pl1'] == id_user:
            player_score = game['pl1_count']
        else:
            player_score = game['pl2_count']

        total_score += player_score
        if player_score > max_score:
            max_score = player_score

    return {
        "total_games": total_games,
        "wins": wins,
        "losses": losses,
        "draw": draw,
        "max_score": max_score,
        "total_score": total_score
    }

async def last_3_games(id_user: int) -> list:
    games = (await GameDAO.find_end_game(id_user))[:3]
    info_games = []
    for game in games:
        info_game = {
            "pl1_count": game["pl1_count"],
            "pl2_count": game["pl2_count"],
        }
        info_game['pl1_name'] = (await UsersDAO.find_by_id(game['id_pl1'])).username
        info_game['pl2_name'] = (await UsersDAO.find_by_id(game['id_pl2'])).username
        
        if game['id_pl_win'] == game['id_pl1']:
            info_game['pl_win'] = info_game['pl1_name']
        elif game['id_pl_win'] == 0:
            info_game['pl_win'] = "Ничья"
        else:
            info_game['pl_win'] = info_game['pl2_name']
        info_games.append(info_game)
        
    return info_games

async def create_color(data_temp: dict) -> dict:
    data = []
    for i in range(0, 9, 3):
        count = {num: data_temp[i:i+3].count(num) for num in set(data_temp[i:i+3])}
        for j in data_temp[i:i+3]:
            if j == 0:
                data.append("black")
            else:
                if count[j] == 1:
                    data.append("white")
                if count[j] == 2:
                    data.append("yellow") 
                if count[j] == 3:
                    data.append("blue") 
    return data

async def create_dict(
	id_pl: int, 
 	id_pl_move: int,
 	pl_name: str, 
  	pl_1_3_temp: list, 
   	pl_1_2_3: list,
    pl_count: int,
    op_name: str,
   	op_1_3_temp: list, 
    op_1_2_3: list, 
    op_count: int,
    current_count: int
) -> dict:
	pl_1_3 = [x if x != 0 else "" for x in pl_1_3_temp]
	pl_1_3_color = await create_color(pl_1_3_temp) # black white yellow blue
	
	op_1_3 = [x if x != 0 else "" for x in op_1_3_temp]
	op_1_3_color = await create_color(op_1_3_temp)
	
	if id_pl_move == id_pl:
		pl_current_count = current_count
		op_current_count = ""
	else:
		pl_current_count = ""
		op_current_count = current_count
	return {
		"id_pl": id_pl,
		"pl_name": pl_name,
		"pl_1_3": pl_1_3,
		"pl_1_3_color": pl_1_3_color,
		"pl_1_2_3": pl_1_2_3,
		"pl_count": pl_count,
		"pl_current_count": pl_current_count,
		
		"op_name": op_name,
		"op_1_3": op_1_3,
		"op_1_3_color": op_1_3_color,
		"op_1_2_3": op_1_2_3,
		"op_count": op_count,
		"op_current_count": op_current_count,
	}
 
async def make_move(number: int, id_game: int, id_pl: int):
    game_data = await GameDAO.find_by_id(id_game) # Дублирование!
    if game_data.status_games != "playing":
        return {"detail": "Игра окончена"}
    if id_pl == game_data.id_pl1:
        id_pl_name = 1
        id_op_name = 2
        next_id_pl = game_data.id_pl2
        op_sum_count = game_data.pl2_count
        pl_1_3 = [
			game_data.pl1_1_1, game_data.pl1_1_2, game_data.pl1_1_3,
			game_data.pl1_2_1, game_data.pl1_2_2, game_data.pl1_2_3,
			game_data.pl1_3_1, game_data.pl1_3_2, game_data.pl1_3_3,
		]
        op_1_3 = [
			game_data.pl2_1_1, game_data.pl2_1_2, game_data.pl2_1_3,
			game_data.pl2_2_1, game_data.pl2_2_2, game_data.pl2_2_3,
			game_data.pl2_3_1, game_data.pl2_3_2, game_data.pl2_3_3,
		]
    if id_pl == game_data.id_pl2:
        id_pl_name = 2
        id_op_name = 1
        next_id_pl = game_data.id_pl1
        op_sum_count = game_data.pl1_count
        pl_1_3 = [
			game_data.pl2_1_1, game_data.pl2_1_2, game_data.pl2_1_3,
			game_data.pl2_2_1, game_data.pl2_2_2, game_data.pl2_2_3,
			game_data.pl2_3_1, game_data.pl2_3_2, game_data.pl2_3_3,
		]
        op_1_3 = [
			game_data.pl1_1_1, game_data.pl1_1_2, game_data.pl1_1_3,
			game_data.pl1_2_1, game_data.pl1_2_2, game_data.pl1_2_3,
			game_data.pl1_3_1, game_data.pl1_3_2, game_data.pl1_3_3,
		] 
        
    if number == 1:
        pl = pl_1_3[0:3]
        op = op_1_3[0:3]
    if number == 2:
        pl = pl_1_3[3:6]
        op = op_1_3[3:6]
    if number == 3:
        pl = pl_1_3[6:9]
        op = op_1_3[6:9]
    
    if pl.count(0) <= 0:
        return {"detail": "Невозможно вставить число"}
    
    for i in range(0, len(pl)):
        if pl[i] == 0:
            pl[i] = game_data.current_count
            break
    
    pl_1_3[(number-1)*3+i] = game_data.current_count
    
    position = f"pl{id_pl_name}_{number}_{i+1}"
    count = game_data.current_count
    sum_position = f"pl{id_pl_name}_{number}"
    sum_count = sum(pl)
    pl_sum_name = f"pl{id_pl_name}_count"
    
    pl_sum = {}
    
    for i in range(0, 9, 3):
        i_next = i + 3
        if i/3+1 == number:
            dict_pl = {num: pl.count(num) for num in set(pl)}
            pl_sum[f"pl_{int(i/3+1)}"] = sum(num * cn * cn for num, cn in dict_pl.items())
        else:
            dict_pl = {num: pl_1_3[i:i_next].count(num) for num in set(pl_1_3[i:i_next])}
            pl_sum[f"pl_{int(i/3+1)}"] = sum(num * cn * cn for num, cn in dict_pl.items())
    
    pl_sum_count = pl_sum['pl_1'] + pl_sum['pl_2'] + pl_sum['pl_3']
    
    id_pl_move = next_id_pl
    update_data = {
		position: count,
		sum_position: sum_count,
		"current_count": random.randint(1, 6),
		"id_pl_move": id_pl_move,
		pl_sum_name: pl_sum_count,
		f"pl{id_pl_name}_1": pl_sum['pl_1'],
		f"pl{id_pl_name}_2": pl_sum['pl_2'],
		f"pl{id_pl_name}_3": pl_sum['pl_3'],
	}
    
    if op.count(game_data.current_count) > 0:
        for i in range(0, len(op)):
            if op[i] == game_data.current_count:
                op[i] = 0
                
        non_zero_op = [num for num in op if num != 0]
        zero_count = op.count(0)
        sorted_op = non_zero_op + [0] * zero_count
                
        update_data[f"pl{id_op_name}_{number}_1"] = sorted_op[0]
        update_data[f"pl{id_op_name}_{number}_2"] = sorted_op[1]
        update_data[f"pl{id_op_name}_{number}_3"] = sorted_op[2]
        
        op_sum = {}
        
        for i in range(0, 9, 3):
            i_next = i + 3
            if i/3+1 == number:
                dict_op = {num: op.count(num) for num in set(op)}
                op_sum[f"op_{int(i/3+1)}"] = sum(num * cn * cn for num, cn in dict_op.items())
            else:
                dict_op = {num: op_1_3[i:i_next].count(num) for num in set(op_1_3[i:i_next])}
                op_sum[f"op_{int(i/3+1)}"] = sum(num * cn * cn for num, cn in dict_op.items())
        
        update_data[f"pl{id_op_name}_1"] = op_sum['op_1']
        update_data[f"pl{id_op_name}_2"] = op_sum['op_2']
        update_data[f"pl{id_op_name}_3"] = op_sum['op_3']
        
        op_sum_count = op_sum['op_1'] + op_sum['op_2'] + op_sum['op_3']
        
        update_data[f"pl{id_op_name}_count"] = op_sum_count
        
    if pl_1_3.count(0) <= 0 or op_1_3.count(0) <= 0:
        update_data["status_games"] = "ending"
        win = -1
        if pl_sum_count > op_sum_count:
            win = id_pl
            status_games = 1
        elif op_sum_count > pl_sum_count:
            win = next_id_pl
            status_games = -1
        elif op_sum_count == pl_sum_count:
            win = 0
            status_games = 0
        
        update_data["id_pl_win"] = win
        
        await give_awards(id_pl, status_games)
        await give_awards(next_id_pl, -1 * status_games)
    
    await GameDAO.update_game(id_game, **update_data)