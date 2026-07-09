# tests/test_app.py
import pytest
from app import app
import data_store

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def reset_inventory():
    # Reset the in-memory data before every test so tests don't interfere with each other
    data_store.inventory.clear()
    data_store.inventory.append({
        "id": 1, "product_name": "Laptop", "brand": "Dell",
        "price": 999.99, "barcode": "123456789012", "quantity": 10
    })
    data_store.inventory.append({
        "id": 2, "product_name": "Smartphone", "brand": "Apple",
        "price": 699.99, "barcode": "098765432109", "quantity": 20
    })

def test_get_all_items(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.get_json()) == 2

def test_get_single_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Laptop"

def test_get_single_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404

def test_create_item(client):
    new_item = {"product_name": "Mouse", "brand": "Logitech", "price": 25.0, "quantity": 50, "barcode": "111"}
    response = client.post("/inventory", json=new_item)
    assert response.status_code == 201
    assert response.get_json()["product_name"] == "Mouse"

def test_create_item_missing_name(client):
    response = client.post("/inventory", json={"brand": "NoName"})
    assert response.status_code == 400

def test_update_item(client):
    response = client.patch("/inventory/1", json={"price": 899.99})
    assert response.status_code == 200
    assert response.get_json()["price"] == 899.99

def test_update_item_not_found(client):
    response = client.patch("/inventory/999", json={"price": 1})
    assert response.status_code == 404

def test_delete_item(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200

def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404