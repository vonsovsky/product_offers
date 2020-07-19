# product_offers
Simple Flask app for product and their offers management. A product is being updated with their offers via microservice.

## Installation

`pip install -r requirements.txt`

Set up environment variables with `SET` on Windows or `export` on Linux

SET PRODUCT_BASE_URL=<your microservice url here>
SET FLASK_APP=server.py
SET FLASK_DEBUG=1

## Usage

CRUD architecture on http://127.0.0.1:5000/products/ when `flask run` is executed.
Job is running in the background to update offers every hour.
