from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import Settings, get_settings
from .database.db import create_db_and_tables
from .routers import games, guesses, players


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan startup")
    create_db_and_tables()
    yield
    print("lifespan shutdown")


app = FastAPI(lifespan=lifespan)

app.include_router(players.router)
app.include_router(games.router)
app.include_router(guesses.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]) -> Settings:
    return settings


@app.get("/")
def read_root():
    return {"Hello": "World"}


# example of rendering a template
@app.get("/index.html", response_class=HTMLResponse)
def read_html(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})
