from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.users.auth import get_menu


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/notifications")
async def notifications(request: Request, messages: str):
    return templates.TemplateResponse("notifications.html", {"request": request, "messages": messages})