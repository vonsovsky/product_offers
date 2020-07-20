def populate_products(db):
    with db.get_cursor() as cursor:
        query = "DELETE FROM products"
        cursor.execute(query)

    db.create_product("Zámek", "Vybydlený zámek ve starém městě bez vodovodu")
    db.create_product("Důl", "Uzavřený uhelný důl OKD promořený koronavirem")
    db.create_product("Lavička u nádraží", "Podnájem na lavičce, blízkost k centru, sociální kontakt")


def test_create_product(db):
    populate_products(db)


def test_retrieve_products(db):
    populate_products(db)

    products = db.retrieve_products()

    assert len(products) == 3
    assert products[0]['name'] == 'Zámek'
    assert products[0]['description'] == 'Vybydlený zámek ve starém městě bez vodovodu'


def test_insert_offers(db):
    populate_products(db)

    products = db.retrieve_products()
    offer_map = {
        products[0]['id']: [
            {'id': 4, 'price': 1000, 'items_in_stock': 23},
            {'id': 6, 'price': 2000, 'items_in_stock': 46}
        ],
        products[1]['id']: [
            {'id': 8, 'price': 3000, 'items_in_stock': 69}
        ]
    }

    db.insert_offers(offer_map)

    offer_map[products[1]['id']] = [
        {'id': 8, 'price': 4000, 'items_in_stock': 69},
        {'id': 10, 'price': 5000, 'items_in_stock': 92}
    ]

    db.insert_offers(offer_map)

    with db.get_cursor() as cursor:
        query = "SELECT ms_id, price FROM offers"
        cursor.execute(query)
        offers = [{'id': row[0], 'price': row[1]} for row in cursor.fetchall()]

    assert offers[0]['id'] == 4
    assert offers[0]['price'] == 1000
    assert offers[1]['id'] == 6
    assert offers[2]['id'] == 8
    assert offers[2]['price'] == 4000
    assert offers[3]['id'] == 10
