from pydantic.dataclasses import dataclass
from pydantic import conint, constr, confloat


@dataclass
class ItemInputValidator:
    """Pydantic data validation class for item input"""

    description: constr(min_length=1)
    price: confloat(gt=0)
    quantity: conint(gt=0)
