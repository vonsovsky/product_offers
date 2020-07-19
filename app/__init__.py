from flask import Flask
from model import DBModel
from config import Config

db = DBModel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(config_class.SQLITE_FILE)

    return app
