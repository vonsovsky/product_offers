# Product offers
Simple Flask app for product and their offers management. A product is being updated with their offers via microservice.

## Installation

`pip install -r requirements.txt`

Set up environment variables with `SET` on Windows or `export` on Linux

SET PRODUCT_BASE_URL=&lt;your microservice url here&gt;

SET FLASK_APP=server.py

SET FLASK_DEBUG=1

## Usage

### Background job

run `rq worker po-task` in bash to prepare RQ worker for background task.

run `python run_worker.py` to schedule microservice calls every minute.
Environment variables from installation section must be set.

### Web service

Execute `flask run` to prepare CRUD architecture on http://127.0.0.1:5000/products/.

Adding new product by CREATE mode will trigger new product being added to offers microservice.

### Testing

run `pytest`
