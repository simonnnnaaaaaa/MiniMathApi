from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# test for main
def test_fib_endpoint():
    response = client.get("/fib/7")
    assert response.status_code == 200
    assert response.json()["result"] == 13


def test_pow_endpoint():
    response = client.post("/pow", json={"x": 2, "y": 5})
    assert response.status_code == 200
    assert response.json()["result"] == 32


def test_fact_endpoint():
    response = client.get("/fact/4")
    assert response.status_code == 200
    assert response.json()["result"] == 24
