from pos import db


class OrderItem(db.Model):
    """Association table model. Orders and Items have a many-to-many relationship"""

    order_id = db.Column(db.ForeignKey('order.id'), primary_key=True)
    item_id = db.Column(db.ForeignKey('item.id'), primary_key=True)
    ordered_quantity = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'item_id': self.item_id,
            'ordered_quantity': self.ordered_quantity
        }

