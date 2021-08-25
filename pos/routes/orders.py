from flask import request, jsonify, abort, Blueprint
from pydantic import ValidationError

from pos import db
from pos.exceptions.custom_exceptions import EmptyResourceError, QuantityError, PaymentError
from pos.models.item import Item
from pos.models.order import Order
from pos.models.order_item import OrderItem
from pos.validators.order_input_validator import OrderInputValidator
from pos.validators.payment_validator import payment_validator

# Blueprint for api/v1/orders routes
orders_bp = Blueprint("orders", __name__)


@orders_bp.route('/', methods=['POST'])
def add_order():
    """
    Description: Add a new order to the system
    URL: api/v1/orders
    Method: POST
    Content Type: application/json
    Body:
        {
            "order_items": [
                {
                    "item_id":1,
                    "order_quantity":1
                },
                {
                    "item_id":2,
                    "order_quantity":5
                }
            ],
            "payment_amount": 20.5,
            "order_note": "Add extra cheese"
        }
    Responses:
        200: Success. Order placed successfully
        400: Invalid payment error, ordered quantity not available or input validation error
        404: Ordered item(s) not found in the system
        500: Internal server error
    """

    try:
        order_items = request.json['order_items']
        payment_amount = request.json['payment_amount']
        order_note = request.json['order_note']

        # Validate input
        OrderInputValidator(order_items, payment_amount, order_note)

        # Validate item availability and payment correctness
        payment_validator(order_items, payment_amount)

        # Create order
        new_order = Order(payment_amount, order_note)
        db.session.add(new_order)

        for order_item in order_items:
            item_id = order_item['item_id']
            order_quantity = order_item['order_quantity']

            item = Item.query.get(item_id)
            item.quantity -= order_quantity

            order_item = OrderItem(item_id=item_id, ordered_quantity=order_quantity)

            # Update association table
            new_order.items.append(order_item)

        db.session.commit()

        return jsonify({"order_id": new_order.id}), 200

    except (ValidationError, QuantityError, PaymentError) as ex:
        abort(400, str(ex))
    except EmptyResourceError as ex:
        abort(404, str(ex))
    except Exception as ex:
        abort(500, str(ex))


@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    """
    Description: Get an order by order_id
    URL: api/v1/orders/1234
    Method: GET
    Content Type: application/json
    Body: N/A
    Responses:
        200: Success. Order found
        404: Order with order_id not found
        500: Internal server error
    """

    try:
        order = Order.query.get(order_id)

        if not order:
            raise EmptyResourceError(f"Order {order_id} not found. Please place orders")

        return jsonify(order.serialize), 200

    except EmptyResourceError as ex:
        abort(404, str(ex))
    except Exception as ex:
        abort(500, str(ex))
