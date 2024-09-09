from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.users.auth import get_menu


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/rules")
async def home(request: Request, menu: list = Depends(get_menu)):
    return templates.TemplateResponse("rules.html", {"request": request, "menu": menu})