from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_guesses():
    response = client.get("/guess", headers={})
    assert response.status_code == 200


def test_get_guess(game_fixture):

    game_id = game_fixture["game_id"]
    response = client.post(
        f"/guess/", headers={}, json={"game_id": game_id, "value": 123}
    )

    json_response = response.json()
    guess_id = json_response["guess_id"]
    response = client.get(f"/guess/{guess_id}", headers={})
    assert response.status_code == 200


def test_get_guess_not_found():
    guess_id = "999999999999999"
    response = client.get(f"/guess/{guess_id}", headers={})
    assert response.status_code == 404


def test_create_guess(game_fixture):
    game_id = game_fixture["game_id"]
    response = client.post(
        f"/guess/", headers={}, json={"game_id": game_id, "value": 123}
    )
    assert response.status_code == 200
