from pydantic.dataclasses import dataclass
from pydantic import conlist, constr, confloat


@dataclass
class OrderInputValidator:
    """Pydantic data validation class for order input"""

    order_items: conlist(dict, min_items=1)
    payment_amount: confloat(gt=0)
    order_note: constr(min_length=1)
