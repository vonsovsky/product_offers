from flask import request, abort, jsonify, make_response, Response
from app import app
from db_model import DBModel
from offer_service import OfferService
import logging

db_model = DBModel()
product_service = OfferService()
logging.basicConfig(level=logging.INFO)


@app.route('/products/', methods=['GET'])
def get_products() -> Response:
    products = db_model.retrieve_products()
    app.logger.info("Retrieved %d products", len(products))

    return make_response(jsonify(products))


@app.route('/products/', methods=['POST'])
def add_product() -> Response:
    try:
        name = request.form['name']
        description = request.form['description']
    except KeyError as key:
        abort(400, description="Missing key: " + key)

    created_id = db_model.create_product(name, description)
    data = product_service.register_product(created_id, name, description)
    app.logger.info("Product %d created", created_id)

    return make_response(jsonify({'id': data['id']}))


@app.route('/products/<int:id>/', methods=['PUT'])
def update_product(id: int) -> Response:
    try:
        name = request.form['name']
        description = request.form['description']
    except KeyError as key:
        abort(400, description="Missing key: " + key)

    app.logger.info("Product %d updated", id)
    db_model.update_product(id, name, description)

    return make_response("", 200)


@app.route('/products/<int:id>/', methods=['DELETE'])
def delete_product(id: int) -> Response:
    db_model.delete_product(id)
    app.logger.info("Product %d deleted", id)

    return make_response("", 204)
