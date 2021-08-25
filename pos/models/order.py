from pos import db


class Order(db.Model):
    """Database model for Order"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(50), unique=False, nullable=False)
    items = db.relationship('OrderItem')

    def __repr__(self):
        return f"Order(id={self.id}, amount={self.amount}, note={self.note})"

    def __init__(self, amount, note):
        self.amount = amount
        self.note = note

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'amount': self.amount,
            'note': self.note,
            'items': [item.serialize for item in self.items],
        }
