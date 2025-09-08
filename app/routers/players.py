from typing import Union, Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Query, APIRouter
from sqlmodel import Field, Session, SQLModel, create_engine, select

from app.db import SessionDep


router = APIRouter(prefix="/players", tags=["[players"])


class PlayerBase(SQLModel):
    name: str = Field(index=True, title="The player's name")


class Player(PlayerBase, table=True):
    player_id: int | None = Field(default=None, primary_key=True)


class PlayerCreate(PlayerBase):
    name: str


class PlayerUpdate(PlayerBase):
    name: str | None = None


@router.get("/", response_model=list[Player])
async def read_players(session: SessionDep) -> list[Player]:
    players = session.exec(select(Player)).all()
    return players


@router.post("/", response_model=Player)
async def create_player(player: PlayerCreate, session: SessionDep) -> Player:
    player_db = Player.model_validate(player)
    session.add(player_db)
    session.commit()
    session.refresh(player_db)
    return player_db


@router.get("/{player_id}", response_model=Player)
async def read_player(player_id: int, session: SessionDep) -> Player:

    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.patch("/{player_id}")
async def update_player(
    player_id: int, player: PlayerUpdate, session: SessionDep
) -> Player:
    player_db = session.get(Player, player_id)

    if not player_db:
        raise HTTPException(status_code=404, detail="Player not found")

    player_data = player.model_dump(exclude_unset=True)

    player_db.sqlmodel_update(player_data)

    session.add(player_db)
    session.commit()
    session.refresh(player_db)
    return player_db


@router.delete("/{player_id}")
async def delete_player(player_id: str, session: SessionDep) -> dict:
    player_db = session.get(Player, player_id)

    if not player_db:
        raise HTTPException(status_code=404, detail="Player not found")

    session.delete(player_db)
    session.commit()
    return {"ok": True}
