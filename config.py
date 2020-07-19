import os


class Config:
    TESTING = False
    SQLITE_FILE = "db.sqlite3"

    base_url_key = 'PRODUCT_BASE_URL'
    if base_url_key not in os.environ:
        raise ValueError("PRODUCT_BASE_URL is not specified")
    BASE_URL = os.environ[base_url_key]

    TOKEN_URL = BASE_URL + 'auth'
    REGISTER_PRODUCT_URL = BASE_URL + 'products/register'
    GET_OFFERS_URL = BASE_URL + 'products/{}/offers'
