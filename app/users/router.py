from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from app.users.auth import authenticate_user, check_avatar, create_access_token, get_current_admin_user, get_current_user, get_password_hash
from app.users.dao import UsersDAO
from app.users.models import User
from app.users.schemas import SUserAuth, SUserRegister, SAvatar


router = APIRouter(
    prefix='/api/auth', 
    tags=['Авторизация']
)


@router.get('/all-user')
async def all_user(user_data: User = Depends(get_current_admin_user)):
    result = await UsersDAO.find_all()
    return result

@router.get("/me")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data

@router.put("/set-avatar")
async def edit_user(request: Request, avatar: SAvatar):
    token = request.cookies.get('users_access_token')
    user_data = await get_current_user(token)
    
    if avatar.url != "/static/images/avatar/lamb-icon.png":
        await check_avatar(user_data.id, avatar.url)
    
    await UsersDAO.edit_user(id_user=user_data.id, activate_url=avatar.url)
    
    return {"status": 200}

@router.post("/register")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(login=user_data.login)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    if await UsersDAO.find_one_or_none(login=user_data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Имя пользователя уже занято'
        )
    user_dict = user_data.__dict__
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add_user(username=user_data.username, login=user_data.login, hash_password=user_dict['password'])
    return {'message': 'Вы успешно зарегистрированы!'}

@router.post("/login")
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(login=user_data.login, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}