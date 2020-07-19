from flask import request, abort, jsonify
from app import create_app, db
from offer_service import OfferService
import logging

app = create_app()
product_service = OfferService()
logging.basicConfig(level=logging.DEBUG)


@app.route('/products/', methods=['GET'])
def get_products() -> None:
    fetched_products = db.retrieve_products()
    app.logger.info("Retrieved %d products", len(fetched_products))
    products = [{'name': row[0], 'description': row[1]} for row in fetched_products]
    app.logger.info(products)

    return jsonify(products)


@app.route('/products/', methods=['POST'])
def add_product() -> None:
    try:
        name = request.form['name']
        description = request.form['description']
    except KeyError as key:
        abort(400, description="Missing key: " + key)

    created_id = db.create_product(name, description)
    data = product_service.register_product(created_id, name, description)
    app.logger.info("Product %d created", created_id)

    return {'id': data['id']}


@app.route('/products/<int:id>/', methods=['PUT'])
def update_product(id: int) -> None:
    try:
        name = request.form['name']
        description = request.form['description']
    except KeyError as key:
        abort(400, description="Missing key: " + key)

    app.logger.info("Product %d updated", id)
    db.update_product(id, name, description)

    return jsonify(success=True)


@app.route('/products/<int:id>/', methods=['DELETE'])
def delete_product(id: int) -> None:
    db.delete_product(id)
    app.logger.info("Product %d deleted", id)

    return jsonify(success=True)
