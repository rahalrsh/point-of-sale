from pos import db


class Item(db.Model):
    """Database model for menu Item"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(50), unique=False, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Item(id={self.id}, price={self.price}, quantity={self.quantity})"

    def __init__(self, description, price, quantity):
        self.description = description
        self.price = price
        self.quantity = quantity

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity,
        }
