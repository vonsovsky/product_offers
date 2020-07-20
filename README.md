# product_offers
Simple Flask app for product and their offers management. A product is being updated with their offers via microservice.

## Installation

`pip install -r requirements.txt`

Set up environment variables with `SET` on Windows or `export` on Linux

SET PRODUCT_BASE_URL=<your microservice url here>
SET FLASK_APP=server.py
SET FLASK_DEBUG=1

## Usage

run `rq worker po-task` in bash to prepare RQ worker for background task
In order to test worker, you can run it manually in python shell:
```
from redis import Redis
import rq
queue = rq.Queue('po-task', connection=Redis.from_url('redis://'))
job = queue.enqueue('worker.update_offers')
```

Execute `flask run` to prepare CRUD architecture on http://127.0.0.1:5000/products/.

Adding new product by CREATE mode will trigger new product being added to offers microservice.
