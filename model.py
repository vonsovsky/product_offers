"""
Provides SQL database layer to products and offers
"""

from typing import List, Dict
from custom_connection import CustomConnection


class DBModel:

    def __init__(self) -> None:
        self._conn = None

    def init_app(self, file_name: str) -> None:
        self._conn = CustomConnection(file_name)

    def get_cursor(self):
        return self._conn.cursor()

    def create_product(self, name: str, description: str) -> int:
        with self.get_cursor() as cursor:
            query = "INSERT INTO products (name, description) VALUES (\"{}\", \"{}\")".format(name, description)
            cursor.execute(query)
            return cursor.lastrowid

    def retrieve_products(self) -> List[Dict[str, str]]:
        with self.get_cursor() as cursor:
            query = "SELECT id, name, description FROM products"
            cursor.execute(query)
            products = [{'id': row[0], 'name': row[1], 'description': row[2]} for row in cursor.fetchall()]
            return products

    # TODO we could make in-memory check whether something changed and update only those
    # TODO batching if we have a lot of products
    def insert_offers(self, offer_map: Dict[int, List[Dict[str, int]]]) -> None:
        with self.get_cursor() as cursor:
            for product_id, offers in offer_map.items():
                for offer in offers:
                    query = "SELECT id FROM offers WHERE ms_id = {}".format(offer['id'])
                    cursor.execute(query)
                    if cursor.fetchone() is None:
                        query = "INSERT INTO offers (product, ms_id, price, items_in_stock) VALUES ({}, {}, {}, {})"\
                            .format(product_id, offer['id'], offer['price'], offer['items_in_stock'])
                    else:
                        query = "UPDATE offers SET price={}, items_in_stock={} WHERE ms_id={}"\
                            .format(offer['price'], offer['items_in_stock'], offer['id'])
                    cursor.execute(query)
