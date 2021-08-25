class EmptyResourceError(Exception):
    """Raised when resources are not found"""
    pass


class QuantityError(Exception):
    """Raised when order quantity is not correct"""
    pass


class PaymentError(Exception):
    """Raised when payment amount is not correct"""
    pass
