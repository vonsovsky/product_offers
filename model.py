from custom_connection import CustomConnection


class DBModel:

    def __init__(self):
        self._conn = None

    def init_app(self, file_name):
        self._conn = CustomConnection(file_name)

    def create_product(self, name, description):
        with self._conn.cursor() as cursor:
            query = "INSERT INTO products (name, description) VALUES (\"{}\", \"{}\")".format(name, description)
            cursor.execute(query)
            return cursor.lastrowid

    def retrieve_products(self):
        with self._conn.cursor() as cursor:
            query = "SELECT name, description FROM products"
            cursor.execute(query)
            return cursor.fetchall()

    def update_product(self, id, name, description):
        with self._conn.cursor() as cursor:
            query = "UPDATE products SET name = \"{}\", description = \"{}\" WHERE id = {}"\
                .format(name, description, id)
            cursor.execute(query)

    def delete_product(self, id):
        with self._conn.cursor() as cursor:
            query = "DELETE FROM products WHERE id = {}".format(id)
            cursor.execute(query)
