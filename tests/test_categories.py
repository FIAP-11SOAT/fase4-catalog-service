from fastapi.testclient import TestClient
from app.main import app
import uuid


def test_list_categories_empty_returns_404_and_empty_array():
    client = TestClient(app)
    resp = client.get("/categories")
    assert resp.status_code == 404
    assert resp.json() == []


def test_create_category_requires_admin_header():
    payload = {"name": "Lanches", "description": "Lanches rápidos"}
    client = TestClient(app)
    resp = client.post("/categories", json=payload)
    assert resp.status_code == 403


def test_create_get_update_delete_category_happy_path():
    client = TestClient(app)
    # Create
    unique_name = f"Bebidas-{uuid.uuid4().hex[:8]}"
    payload = {"name": unique_name, "description": "Categoria de bebidas"}
    resp = client.post("/categories", json=payload, headers={"X-Role": "admin"})
    assert resp.status_code == 201
    created = resp.json()
    assert created["name"] == unique_name

    cat_id = created["id"]

    # Get by id
    resp = client.get(f"/categories/{cat_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == cat_id

    # Update
    upd = {"name": unique_name, "description": "Atualizada"}
    resp = client.put(f"/categories/{cat_id}", json=upd, headers={"X-Role": "admin"})
    assert resp.status_code == 200
    assert resp.json()["description"] == "Atualizada"

    # Delete
    resp = client.delete(f"/categories/{cat_id}", headers={"X-Role": "admin"})
    assert resp.status_code == 204

    # Ensure gone
    resp = client.get(f"/categories/{cat_id}")
    assert resp.status_code == 404
    assert resp.json() == []
