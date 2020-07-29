"""
Provides SQL database layer to products and offers
"""

from typing import List, Dict
from app import db
from app.models import Product, Offer


class DBModel:

    db = db

    def create_product(self, name: str, description: str) -> int:
        p = Product(name=name, description=description)
        self.db.session.add(p)
        self.db.session.commit()
        return p.id

    def retrieve_products(self) -> List[Dict[str, str]]:
        products = []
        for p in Product.query.all():
            products.append(p.as_dict())
        return products

    def insert_offers(self, offer_map: Dict[int, List[Dict[str, int]]]) -> None:
        for product_id, offers in offer_map.items():
            for offer in offers:
                offer_row = Offer.query.filter(Offer.ms_id == offer['id']).first()
                if offer_row is None:
                    offer_row = Offer(product_id=product_id, ms_id=offer['id'])

                offer_row.price = offer['price']
                offer_row.items_in_stock = offer['items_in_stock']
                self.db.session.add(offer_row)
                self.db.session.commit()

    def update_product(self, id, name, description):
        p = Product.query.get(id)
        p.name = name
        p.description = description

        self.db.session.add(p)
        self.db.session.commit()

    def delete_product(self, id):
        p = Product.query.get(id)
        self.db.session.delete(p)
        self.db.session.commit()
