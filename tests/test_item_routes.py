import pytest
from pos import app as _app, db
import json


@pytest.fixture
def test_client(app):
    """Get a test client for testing"""
    return app.test_client()


@pytest.fixture
def app():
    with _app.app_context():
        db.create_all()
        yield _app
        db.drop_all()


@pytest.fixture
def add_test_item(test_client):
    """Method to add a test item to the test client app"""

    post_data = json.dumps({
        "description": "Pizza",
        "price": 15.5,
        "quantity": 20
    })

    response = test_client.post("/api/v1/items", data=post_data, content_type="application/json")
    return response


def test_add_item__success(test_client):
    """add_item success case"""

    post_data = json.dumps({
        "description": "Burger",
        "price": 12.5,
        "quantity": 20
    })

    response = test_client.post("/api/v1/items", data=post_data, content_type="application/json")

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert b'"description":"Burger"' in response.data


def test_add_item__fail_with_validation_error(test_client):
    """add_item fail case. Price cannot be negative"""

    post_data = json.dumps({
        "description": "Burger",
        "price": -10,
        "quantity": 10
    })

    response = test_client.post("/api/v1/items", data=post_data, content_type="application/json")

    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert b'400 Bad Request: 1 validation error' in response.data


def test_get_all_items__success(test_client, add_test_item):
    """get_all_items success case"""

    response = test_client.get("/api/v1/items", content_type="application/json")
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert b'"description":"Pizza"' in response.data


def test_get_all_items__fail_items_not_found(test_client):
    """get_all_items fail case. No items added to the menu"""

    response = test_client.get("/api/v1/items", content_type="application/json")
    assert response.status_code == 404
    assert response.content_type == 'application/json'
    assert b'404 Not Found: Items not found. Please add items to menu' in response.data


def test_get_item_by_id__success(test_client, add_test_item):
    """get_item_by_id success case"""

    response = test_client.get("/api/v1/items/1", content_type="application/json")
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert b'"description":"Pizza"' in response.data


def test_get_item_by_id__fail_item_not_found(test_client):
    """get_item_by_id fail case. Item with given id does not exist"""

    response = test_client.get("/api/v1/items/5", content_type="application/json")
    assert response.status_code == 404
    assert response.content_type == 'application/json'
    assert b'Item 5 not found' in response.data


def test_update_item_by_id__success(test_client, add_test_item):
    """update_item_by_id_ success case"""

    put_data = json.dumps({
        "description": "Salad",
        "price": 10,
        "quantity": 25
    })

    response = test_client.put("/api/v1/items/1", data=put_data, content_type="application/json")
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert b'"price":10.0' in response.data
    assert b'"description":"Salad"' in response.data


def test_remove_item_by_id__success(test_client, add_test_item):
    """remove_item_by_id success case"""

    response = test_client.delete("/api/v1/items/1", content_type="application/json")
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert b'"id":1' in response.data
