from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_players():
    response = client.get("/players", headers={})
    assert response.status_code == 200


def test_create_player():
    item_data = {"name": "test_player"}
    response = client.post("/players/", json=item_data)
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["name"] == item_data["name"]
    assert isinstance(json_response["player_id"], int)


def test_get_player():
    item_data = {"name": "test_player"}
    response = client.post("/players/", json=item_data)
    json_response = response.json()
    player_id = json_response["player_id"]

    response = client.get(f"/players/{player_id}", headers={})
    assert response.status_code == 200


def test_delete_player(player_fixture):
    player_id = player_fixture["player_id"]

    response = client.delete(f"/players/{player_id}")

    assert response.status_code == 200

    response = client.get(f"/players/{player_id}", headers={})
    assert response.status_code == 404


def test_patch_player(player_fixture):
    player_id = player_fixture["player_id"]
    player_name = player_fixture["name"]
    body = {"name": "updated_new_name"}

    response = client.get(f"/players/{player_id}", headers={})
    assert response.status_code == 200

    response = client.patch(
        f"/players/{player_id}", headers={}, json={"name": "updated_new_name"}
    )

    json_response = response.json()
    assert response.status_code == 200
    assert json_response["name"] != player_name
    assert json_response["name"] == body["name"]
    assert json_response["player_id"] == player_id
