import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(scope="function")
def game_fixture(player_fixture):

    response = client.post(
        "/games", headers={}, json={"player_id": player_fixture["player_id"]}
    )
    json_response = response.json()
    return json_response


@pytest.fixture(scope="function")
def player_fixture():
    body = {"name": "new_player"}
    response = client.post("/players/", json=body)
    player = response.json()
    return player


@pytest.fixture(scope="function")
def guess_fixture(game_fixture):
    game_id = game_fixture["game_id"]
    body = {"game_id": game_id, "value": 123}
    response = client.post("/guess/", json=body)
    player = response.json()
    return player
