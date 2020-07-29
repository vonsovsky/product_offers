from app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(255))
    offers = db.relationship('Offer', backref='offer', lazy='dynamic')

    def __repr__(self):
        return '<Product {}>'.format(self.name)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ms_id = db.Column(db.Integer)
    price = db.Column(db.Float)
    items_in_stock = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self):
        return '<Offer of {}: {} x {}>'.format(self.product_id, self.price, self.items_in_stock)
