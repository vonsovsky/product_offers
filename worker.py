from app import create_app, db
from offer_service import OfferService
from typing import List, Dict

app = create_app()
app.app_context().push()


def update_offers():
    service = OfferService()
    products = db.retrieve_products()
    offer_map: Dict[int, List[Dict[str, int]]] = {}

    # gather all offers into map so everything can be updated in one transaction
    for product in products:
        offer_map[product['id']] = service.get_offers(product['id'])

    db.insert_offers(offer_map)
