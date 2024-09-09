from time import sleep
from fastapi import APIRouter, Depends, Request, Form, Response, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO


router = APIRouter(
	prefix="/auth"
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def auth(request: Request):
    token = request.cookies.get('users_access_token')
    if token:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("authorization.html", {"request": request})

@router.post("/login")
async def login(response: Response, login: str = Form(...), password: str = Form(...)):
    check = await authenticate_user(login=login, password=password)
    if check is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Неверное имя пользователя или пароль")
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'message': 'Вы успешно вошли!'}

@router.post("/register")
async def register(login: str = Form(...), username: str = Form(...), password: str = Form(...)):
    user = await UsersDAO.find_one_or_none(login=login)
    if user:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="Пользователь уже существует")
    if await UsersDAO.find_id_on_username(username=username):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="Имя пользователя уже существует")
    hash_password = get_password_hash(password)
    await UsersDAO.add_user(username=username, login=login, hash_password=hash_password)
    return {'message': 'Вы успешно зарегистрированы!'}

@router.get("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Вы успешно вышли!'}