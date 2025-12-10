from fastapi.testclient import TestClient
from app.main import app


def test_require_admin_denied():
    client = TestClient(app)
    r = client.post("/categories", json={"name": "x", "description": "y"})
    assert r.status_code == 403


def test_require_admin_allowed():
    client = TestClient(app)
    r = client.post("/categories", json={"name": "x2", "description": "y2"}, headers={"X-Role": "admin"})
    assert r.status_code in (201, 409)
