from fastapi.testclient import TestClient
from apis.main import app

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