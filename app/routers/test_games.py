from fastapi.testclient import TestClient

from .games import router

client = TestClient(router)


def test_read_item():
    response = client.get("/", headers={})
    print(response)
    print(";;fawfaasffsdfsfs!")
    assert "hi" == "hi"
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }
