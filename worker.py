from db_model import DBModel
from offer_service import OfferService
from typing import List, Dict

db_model = DBModel()


def update_offers():
    service = OfferService()
    products = db_model.retrieve_products()
    offer_map: Dict[int, List[Dict[str, int]]] = {}

    # gather all offers into map so everything can be updated in one transaction
    for product in products:
        offer_map[product.id] = service.get_offers(product.id)

    db_model.insert_offers(offer_map)


update_offers()