import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TESTING = False

    base_url_key = 'PRODUCT_BASE_URL'
    if base_url_key not in os.environ:
        raise ValueError("PRODUCT_BASE_URL is not specified")
    BASE_URL = os.environ[base_url_key]

    TOKEN_URL = BASE_URL + 'auth'
    REGISTER_PRODUCT_URL = BASE_URL + 'products/register'
    GET_OFFERS_URL = BASE_URL + 'products/{}/offers'
