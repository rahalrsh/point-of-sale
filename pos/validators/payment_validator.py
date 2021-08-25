from pos.models.item import Item
from pos.exceptions.custom_exceptions import EmptyResourceError, QuantityError, PaymentError


def payment_validator(order_items, payment_amount):
    """This method checks and validation below conditions
        1) Item availability
        2) Order quantity availability
        3) Payment correctness (payment high or low than expected amount)
    """

    expected_payment_amount = 0

    for order_item in order_items:
        item_id = order_item['item_id']
        order_quantity = order_item['order_quantity']

        item = Item.query.get(item_id)

        # Item does not exist
        if not item:
            raise EmptyResourceError(f"Items {item_id} not found")

        # Quantity does not exist
        if order_quantity > item.quantity:
            raise QuantityError(f"Quantity: {order_quantity} not available for item: {item_id}")

        expected_payment_amount += (order_quantity * item.price)

    if expected_payment_amount > payment_amount:
        raise PaymentError("Payment amount is too low")

    if expected_payment_amount < payment_amount:
        raise PaymentError("Payment amount is too high")
