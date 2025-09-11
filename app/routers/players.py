from fastapi import HTTPException, APIRouter
from sqlmodel import select

from ..db import SessionDep
from ..models import Player, PlayerCreate, PlayerUpdate, PlayerPublic


router = APIRouter(prefix="/players", tags=["players"])


@router.get("/", response_model=list[PlayerPublic])
async def read_players(session: SessionDep):
    players = session.exec(select(Player)).all()
    return players


@router.post("/", response_model=PlayerPublic)
async def create_player(player: PlayerCreate, session: SessionDep):
    player_db = Player.model_validate(player)
    session.add(player_db)
    session.commit()
    session.refresh(player_db)
    return player_db


@router.get("/{player_id}", response_model=PlayerPublic)
async def read_player(player_id: int, session: SessionDep):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.patch("/{player_id}", response_model=PlayerPublic)
async def update_player(player_id: int, player: PlayerUpdate, session: SessionDep):
    player_db = session.get(Player, player_id)

    if not player_db:
        raise HTTPException(status_code=404, detail="Player not found")

    player_data = player.model_dump(exclude_unset=True)

    player_db.sqlmodel_update(player_data)

    session.add(player_db)
    session.commit()
    session.refresh(player_db)
    return player_db


@router.delete("/{player_id}", response_model=dict)
async def delete_player(player_id: int, session: SessionDep):
    player_db = session.get(Player, player_id)

    if not player_db:
        raise HTTPException(status_code=404, detail="Player not found")

    session.delete(player_db)
    session.commit()
    return {"ok": True}
