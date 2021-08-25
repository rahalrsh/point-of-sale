from flask import request, jsonify, abort, Blueprint
from pydantic import ValidationError

from pos import db
from pos.exceptions.custom_exceptions import EmptyResourceError
from pos.models.item import Item
from pos.validators.item_input_validator import ItemInputValidator

# Blueprint for api/v1/items routes
items_bp = Blueprint("items", __name__)


@items_bp.route('/', methods=['POST'])
def add_item():
    """
    Description: Add a new item to the system
    URL: api/v1/items
    Method: POST
    Content Type: application/json
    Body:
        {
            "description": "Salad",
            "price": 12.5,
            "quantity": 20
        }
    Responses:
        200: Success. Item added
        400: Input validation error
        500: Internal server error
    """

    try:
        description = request.json['description']
        price = request.json['price']
        quantity = request.json['quantity']

        # Validate input
        ItemInputValidator(description, price, quantity)

        # Create new item and commit to db
        new_item = Item(description, price, quantity)

        db.session.add(new_item)
        db.session.commit()

        return jsonify(new_item.serialize), 200

    except ValidationError as ex:
        abort(400, str(ex))
    except Exception as ex:
        abort(500, str(ex))


@items_bp.route('/', methods=['GET'])
def get_all_items():
    """
    Description: Get all items in the system
    URL: api/v1/items
    Method: GET
    Content Type: application/json
    Body: N/A
    Responses:
        200: Success. All items returned
        404: No items found in the system
        500: Internal server error
    """

    try:
        all_items = Item.query.all()

        if not all_items:
            raise EmptyResourceError("Items not found. Please add items to menu")

        return jsonify([item.serialize for item in all_items]), 200

    except EmptyResourceError as ex:
        abort(404, str(ex))
    except Exception as ex:
        abort(500, str(ex))


@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item_by_id(item_id):
    """
    Description: Get an item by item_id
    URL: api/v1/items/123
    Method: GET
    Content Type: application/json
    Body: N/A
    Responses:
        200: Success. Item found
        404: Item with item_id not found
        500: Internal server error
    """

    try:
        item = Item.query.get(item_id)

        if not item:
            raise EmptyResourceError(f"Item {item_id} not found")

        return jsonify(item.serialize), 200

    except EmptyResourceError as ex:
        abort(404, str(ex))
    except Exception as ex:
        abort(500, str(ex))


@items_bp.route('/<int:item_id>', methods=['PUT'])
def update_item_by_id(item_id):
    """
    Description: Get an item by item_id
    URL: api/v1/items/123
    Method: PUT
    Content Type: application/json
    Body:
        {
        "description": "Pizza",
        "price": 22.5,
        "quantity": 10
    }
    Responses:
        200: Success. Item updated
        404: Item with item_id not found
        500: Internal server error
    """

    try:
        description = request.json['description']
        price = request.json['price']
        quantity = request.json['quantity']

        # Validate input
        ItemInputValidator(description, price, quantity)

        item = Item.query.get(item_id)

        if not item:
            raise EmptyResourceError(f"Failed to update. Item {item_id} not found")

        item.description = description
        item.price = price
        item.quantity = quantity

        db.session.commit()

        return jsonify(item.serialize), 200

    except EmptyResourceError as ex:
        abort(404, str(ex))
    except Exception as ex:
        abort(500, str(ex))


@items_bp.route('/<int:item_id>', methods=['DELETE'])
def remove_item_by_id(item_id):
    """
    Description: Delete an item by item_id
    URL: api/v1/items/123
    Method: DELETE
    Content Type: application/json
    Body: N/A
    Responses:
        200: Success. Item deleted
        404: Item with item_id not found
        500: Internal server error
    """

    try:
        item = Item.query.get(item_id)

        if not item:
            raise EmptyResourceError(f"Failed to delete. Item {item_id} not found")

        db.session.delete(item)
        db.session.commit()

        return jsonify(item.serialize), 200

    except EmptyResourceError as ex:
        abort(404, str(ex))
    except Exception as ex:
        abort(500, str(ex))
