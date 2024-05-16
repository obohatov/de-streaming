import pytest
from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)

@pytest.fixture
def test_data():
    return {
        "id": "123456789",
        "store": "Brussels",
        "date": "2020-01-01",
        "products": [
            {"id": "123456789", "name": "Banana", "price": 1.5},
            {"id": "123456789", "name": "Bread", "price": 1.5},
            {"id": "123456789", "name": "Water", "price": 1.5}
        ]
    }

def test_post_data(test_data):
    response = client.post("/data", json=test_data)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    