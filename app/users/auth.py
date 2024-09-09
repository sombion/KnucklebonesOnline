from datetime import datetime, timedelta, timezone
import random

from fastapi import Depends, HTTPException, Request, Response, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_auth_data
from app.shop.dao import ShopDAO
from app.users.dao import InventoryDAO, UsersDAO
from app.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt

async def authenticate_user(login: str, password: str):
    user = await UsersDAO.find_one_or_none(login=login)
    if not user or verify_password(plain_password=password, hashed_password=user.hash_password) is False:
        return None
    return user

def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token
  
async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')

    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user

async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.is_admin or current_user.is_super_admin:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')

async def get_current_super_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.is_super_admin:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')

async def check_user(token):
    if not token:
        return False
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        return False

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        return False
    
    user_id = payload.get('sub')
    if not user_id:
        return False
    
    return await UsersDAO.find_by_id(int(user_id))

async def check_avatar(id_user: int, url: str):
    if url == "/static/images/avatar/lamb-icon.png":
        return 200
    id_item = await ShopDAO.find_id_from_url(url=url)
    if not id_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Неверный URL")
    if not await InventoryDAO.find_item_from_user_and_id(id_user, id_item):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="У Вас нет данной аватарки")

async def get_menu(request: Request) -> list:
    token = request.cookies.get('users_access_token')
    user = await check_user(token)
    if not user:
        menu = [
            {"name": "Главная", "class": "menu", "url": "/"},
            {"name": "Правила", "class": "menu", "url": "/rules"},
            {"name": "Войти", "class": "login", "url": "/auth"},
        ]
    else:
        menu = [
            {"name": "Главная", "class": "menu", "url": "/"},
            {"name": "Играть", "class": "menu", "url": "/start-games"},
            {"name": "Правила", "class": "menu", "url": "/rules"},
            {"name": "Магазин", "class": "menu", "url": "/shop"},
            {"name": "Профиль", "class": "login", "url": "/profile"},
            {"name": "Выйти", "class": "login", "url": "/auth/logout"},
        ]
    return menu

async def give_awards(id_user: int, status_games: int):
    user_data = await UsersDAO.find_by_id(id_user)
    trophies_now = user_data.trophies
    trophies = random.choices([10, 20, 30], [15, 35, 50])[0]
    if status_games == 1:
        money = random.choices([25, 50, 75, 100, 200], [45, 25, 15, 10, 5])[0]
        await UsersDAO.give_award_win(id_user, trophies, money)
    elif status_games == 0:
        await UsersDAO.give_award_lose(id_user, 0, 0)
    else:
        money = random.choices([5, 10, 15, 20], [50, 25, 15, 10])[0]
        if trophies_now - trophies >= 0:
            await UsersDAO.give_award_lose(id_user, trophies, money)