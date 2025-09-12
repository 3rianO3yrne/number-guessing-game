from fastapi import HTTPException, APIRouter
from sqlmodel import select


from ..db import SessionDep
from ..models import Guess, GuessPublic, GuessCreate


router = APIRouter(prefix="/guess", tags=["guess"])


@router.get("/", response_model=list[Guess])
async def read_guesses(session: SessionDep):
    guess = session.exec(select(Guess)).all()
    return guess


@router.post("/", response_model=GuessPublic)
async def create_guess(guess: GuessCreate, session: SessionDep):
    guess_db = Guess.model_validate(guess)
    session.add(guess_db)
    session.commit()
    session.refresh(guess_db)
    return guess_db


@router.get("/{guess_id}", response_model=list[GuessPublic])
async def read_guess(guess_id: int, session: SessionDep):
    guess = session.get(Guess, guess_id)
    if not guess:
        raise HTTPException(status_code=404, detail="Guess not found")
    return guess
