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
        db.create_all()


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


@pytest.fixture
def add_test_order(test_client):
    """Method to add a test order to the test client app"""

    post_data = json.dumps({
        "order_items": [
            {
                "item_id": 1,
                "order_quantity": 2
            }
        ],
        "payment_amount": 31,
        "order_note": "No pineapples"
    })

    response = test_client.post("/api/v1/orders", data=post_data, content_type="application/json")
    return response


def test_add_order__success(test_client, add_test_item):
    """add_order success case"""

    post_data = json.dumps({
        "order_items": [
            {
                "item_id": 1,
                "order_quantity": 2
            }
        ],
        "payment_amount": 31,
        "order_note": "No pineapples"
    })

    response = test_client.post("/api/v1/orders", data=post_data, content_type="application/json")

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert b'"order_id":1' in response.data


def test_add_order__fail_with_validation_error(test_client, add_test_item):
    """add_order fail case. order_items cannot be an empty array"""

    post_data = json.dumps({
        "order_items": [],
        "payment_amount": 15.5,
        "order_note": "No pineapples"
    })

    response = test_client.post("/api/v1/orders", data=post_data, content_type="application/json")

    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert b'400 Bad Request: 1 validation error for OrderInputValidator' in response.data


def test_add_order__fail_item_not_available(test_client, add_test_item):
    """add_order fail case. item_id=100 does not exist in menu"""

    post_data = json.dumps({
        "order_items": [
            {
                "item_id": 100,
                "order_quantity": 1
            }
        ],
        "payment_amount": 15.5,
        "order_note": "No pineapples"
    })

    response = test_client.post("/api/v1/orders", data=post_data, content_type="application/json")

    assert response.status_code == 404
    assert response.content_type == 'application/json'
    assert b'404 Not Found: Items 100 not found' in response.data


def test_add_order__fail_payment_too_low(test_client, add_test_item):
    """add_order fail case. Payment amount is too low"""

    post_data = json.dumps({
        "order_items": [
            {
                "item_id": 1,
                "order_quantity": 1
            }
        ],
        "payment_amount": 10,
        "order_note": "No pineapples"
    })

    response = test_client.post("/api/v1/orders", data=post_data, content_type="application/json")

    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert b'400 Bad Request: Payment amount is too low' in response.data


def test_add_order__fail_payment_too_high(test_client, add_test_item):
    """add_order fail case. Payment amount is too high"""

    post_data = json.dumps({
        "order_items": [
            {
                "item_id": 1,
                "order_quantity": 1
            }
        ],
        "payment_amount": 1000,
        "order_note": "No pineapples"
    })

    response = test_client.post("/api/v1/orders", data=post_data, content_type="application/json")

    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert b'400 Bad Request: Payment amount is too high' in response.data


def test_get_order_by_id__success(test_client, add_test_item, add_test_order):
    """get_order_by_id success case"""

    response = test_client.get("/api/v1/orders/1", content_type="application/json")
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert b'"id":1' in response.data
    assert b'"ordered_quantity":2' in response.data


def test_get_order_by_id__fail_order_not_found(test_client):
    """get_order_by_id fail case. Order with id 11 does not exist"""

    response = test_client.get("/api/v1/orders/11", content_type="application/json")
    assert response.status_code == 404
    assert response.content_type == 'application/json'
    assert b'Order 11 not found. Please place orders' in response.data
