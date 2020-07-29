import pytest
import server
import os
import tempfile


@pytest.fixture(scope='module')
def db():
    db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
    with server.app.app_context():
        server.db.init_app(server.app.config['DATABASE'])
        _create_structure(server.db)

        yield server.db

    os.close(db_fd)
    os.unlink(server.app.config['DATABASE'])


def _create_structure(db_model):
    """
    Used for testing
    """

    sql_create_products = """
        CREATE TABLE IF NOT EXISTS "products" (
        "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        "name"  TEXT NOT NULL,
        "description"  TEXT
        );
    """

    sql_create_offers = """
        CREATE TABLE IF NOT EXISTS "offers" (
        "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        "product"  INTEGER NOT NULL,
        "ms_id"  INTEGER NOT NULL DEFAULT 0,
        "price"  INTEGER NOT NULL DEFAULT 0,
        "items_in_stock"  INTEGER NOT NULL DEFAULT 0,
        CONSTRAINT "product_id" FOREIGN KEY ("product") REFERENCES "products" ("id") ON DELETE CASCADE ON UPDATE CASCADE
        );
    """

    with db_model.get_cursor() as cursor:
        cursor.execute(sql_create_products)
        cursor.execute(sql_create_offers)
        cursor.execute("DELETE FROM offers")
        cursor.execute("DELETE FROM products")
