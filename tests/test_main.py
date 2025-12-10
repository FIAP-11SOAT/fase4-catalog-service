from fastapi.testclient import TestClient
from app.main import app


def test_health_and_startup_log_message():
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
