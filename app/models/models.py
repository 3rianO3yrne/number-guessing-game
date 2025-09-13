from uuid import uuid4

from sqlmodel import Field, Relationship, SQLModel


# Player models
class PlayerBase(SQLModel):
    name: str = Field(index=True, title="The player's name")


class Player(PlayerBase, table=True):
    games: list["Game"] = Relationship(back_populates="player")
    player_id: int | None = Field(default=None, primary_key=True)


class PlayerPublic(PlayerBase):
    name: str
    player_id: int


class PlayerCreate(PlayerBase):
    name: str


class PlayerUpdate(PlayerBase):
    name: str | None = None


# Game models
class GameBase(SQLModel):
    game_id: str | None = Field(default_factory=lambda: uuid4().hex, primary_key=True)


class Game(GameBase, table=True):
    player_id: int = Field(default=None, foreign_key="player.player_id")
    player: Player | None = Relationship(back_populates="games")
    guesses: list["Guess"] | None = Relationship(back_populates="game")


class GamePublic(GameBase):
    game_id: str


class GameCreate(GameBase):
    player_id: int


class GameUpdate(GameBase):
    guess: int | None = None
    guesses: list[int]


# Guess models
class GuessBase(SQLModel):
    value: int = Field(title="The guessed number", le=999)
    guess_id: int | None = Field(default=None, primary_key=True)


class Guess(GuessBase, table=True):
    game_id: str | None = Field(default=None, foreign_key="game.game_id")
    game: Game | None = Relationship(back_populates="guesses")


class GuessPublic(GuessBase):
    value: int | None
    guess_id: int


class GuessCreate(GuessBase):
    game_id: str
    value: int


# combined models
class PlayerPublicWithGame(PlayerPublic):
    game: list[GamePublic] = []


class GamePublicWithPlayerGuesses(GamePublic):
    player: PlayerPublic | None = None
    guesses: list[GuessPublic] = []
