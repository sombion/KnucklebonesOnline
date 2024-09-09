from pydantic import BaseModel, Field

class SUserRegister(BaseModel):
	username: str = Field(..., description="Игровой ник")
	login: str = Field(..., description="Логин")
	password: str = Field(..., min_length=5, max_length=64, description="Пароль")
 
class SUserAuth(BaseModel):
    login: str = Field(..., description="Логин")
    password: str = Field(..., min_length=5, max_length=64, description="Пароль")
    
class SAvatar(BaseModel):
    url: str = Field(...)