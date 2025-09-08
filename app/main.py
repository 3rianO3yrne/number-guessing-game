from typing import Annotated
from functools import lru_cache

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from sqlmodel import Session

from .routers import items, players
from .config import get_settings, Settings
from .db import create_db_and_tables, SessionDep


app = FastAPI()
app.include_router(items.router)
app.include_router(players.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]) -> Settings:
    return settings


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/index.html", response_class=HTMLResponse)
def read_html(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})
