from fastapi.testclient import TestClient
from apis.main import app, add_user
from unittest.mock import MagicMock


client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI with Poetry!"}


def test_get_item():
    response = client.get("/item/9")
    assert response.status_code == 200
    print("Hello")
    print(response.json())
    assert response.json() == "string is returned 9"


def test_add_user():
    mock_session = MagicMock()
    payload = {"id":2, "name": "chali", "email": "johnny@kane.com"}
    mock_user = MagicMock()
    mock_user.dict.return_value == {"id":2, "name": "chali", "email": "johnny@kane.com"}

    response = client.post("/user",json=payload)
    assert response.status_code == 200
    print(response)
    # user = await add_user(session, user)
    # session.commit().assert_called_once()


