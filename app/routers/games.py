from fastapi import APIRouter, HTTPException, APIRouter

from sqlmodel import select

from ..db import SessionDep
from ..models import (
    PlayerPublic,
    Game,
    GameCreate,
    GameUpdate,
    GamePublicWithPlayerGuesses,
)
from .players import read_player

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/", response_model=list[Game])
async def get_games(session: SessionDep):
    games = session.exec(select(Game)).all()
    return games


@router.post("/", response_model=GamePublicWithPlayerGuesses)
async def create_game(game: GameCreate, session: SessionDep):
    player = await read_player(game.player_id, session)

    game_db = Game.model_validate(game)
    session.add(game_db)
    session.commit()
    session.refresh(game_db)
    return game_db


@router.get("/{game_id}", response_model=GamePublicWithPlayerGuesses)
async def get_game(game_id: str, session: SessionDep):
    game = session.get(Game, game_id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.patch("/{game_id}", response_model=GamePublicWithPlayerGuesses)
async def update_game(game_id: str, game: GameUpdate, session: SessionDep):
    game_db = session.get(Game, game_id)

    if not game_db:
        raise HTTPException(status_code=404, detail="Game not found")

    game_data = game.model_dump(exclude_unset=True)

    game_db.sqlmodel_update(game_data)

    session.add(game_db)
    session.commit()
    session.refresh(game_db)
    return game_db


@router.delete("/{game_id}", response_model=dict)
async def delete_game(game_id: str, session: SessionDep):
    game_db = session.get(Game, game_id)

    if not game_db:
        raise HTTPException(status_code=404, detail="Player not found")

    session.delete(game_db)
    session.commit()
    return {"ok": True}
