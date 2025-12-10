from fastapi.testclient import TestClient
from app.main import app
from app.models import Category
import uuid


def _ensure_category(client):
    name = f"Cat-{uuid.uuid4().hex[:6]}"
    resp = client.post("/categories", json={"name": name, "description": "tmp"}, headers={"X-Role": "admin"})
    assert resp.status_code in (201, 409)
    if resp.status_code == 201:
        return resp.json()["id"], name
    # If conflict, get by listing
    resp = client.get("/categories")
    if resp.status_code == 404:
        # create again
        resp = client.post("/categories", json={"name": name, "description": "tmp"}, headers={"X-Role": "admin"})
        assert resp.status_code == 201
        return resp.json()["id"], name
    cat = resp.json()[0]
    return cat["id"], cat["name"]


def test_products_crud_flow():
    client = TestClient(app)
    cat_id, _ = _ensure_category(client)

    unique = uuid.uuid4().hex[:8]
    payload = {
        "name": f"Produto-{unique}",
        "description": "desc",
        "price": 12.34,
        "image_url": "http://example.com/img.png",
        "preparation_time": 10,
        "category_id": cat_id,
    }

    # Create requires admin
    r = client.post("/products", json=payload)
    assert r.status_code == 403

    r = client.post("/products", json=payload, headers={"X-Role": "admin"})
    assert r.status_code == 201
    created = r.json()
    pid = created["id"]

    # Get by id
    r = client.get(f"/products/{pid}")
    assert r.status_code == 200

    # List
    r = client.get("/products")
    assert r.status_code in (200, 404)

    # Update
    upd = dict(payload)
    upd["description"] = "nova"
    r = client.put(f"/products/{pid}", json=upd, headers={"X-Role": "admin"})
    assert r.status_code == 200
    assert r.json()["description"] == "nova"

    # Delete
    r = client.delete(f"/products/{pid}", headers={"X-Role": "admin"})
    assert r.status_code == 204

    # Ensure gone
    r = client.get(f"/products/{pid}")
    assert r.status_code == 404
