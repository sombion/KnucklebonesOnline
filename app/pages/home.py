from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.users.auth import get_menu


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def home(request: Request):
    menu = await get_menu(request)
    return templates.TemplateResponse("index.html", {"request": request, "menu": menu})