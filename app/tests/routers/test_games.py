from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_games():
    response = client.get("/games", headers={})
    assert response.status_code == 200


def test_create_game():
    item_data = {"name": "test_player"}
    response = client.post("/players/", json=item_data)
    player = response.json()

    response = client.post(
        "/games", headers={}, json={"player_id": player["player_id"]}
    )
    json_response = response.json()

    assert response.status_code == 200
    assert isinstance(json_response["game_id"], str)
    assert json_response["player"]["name"] == player["name"]
    assert json_response["player"]["player_id"] == player["player_id"]
    assert json_response["guesses"] == []


def test_get_game(game_fixture):
    game_id = game_fixture["game_id"]
    response = client.get(f"/games/{game_id}", headers={})
    json_response = response.json()
    assert response.status_code == 200
    assert json_response == game_fixture
