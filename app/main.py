from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.games.router import router as router_api_game
from app.pages.auth import router as router_login
from app.pages.games import router as router_games
from app.pages.home import router as router_home
from app.pages.notifications import router as router_notification
from app.pages.rules import router as router_rules
from app.pages.shop import router as router_shop
from app.pages.start_games import router as router_start_games
from app.pages.profile import router as router_profile
from app.users.router import router as router_user
from app.shop.router import router as router_api_shop

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router_home)
app.include_router(router_start_games)
app.include_router(router_rules)
app.include_router(router_shop)
app.include_router(router_games)
app.include_router(router_login)
app.include_router(router_notification)
app.include_router(router_profile)

app.include_router(router_user)
app.include_router(router_api_game)
app.include_router(router_api_shop)