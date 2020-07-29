import pytest
import server


@pytest.fixture(scope='module')
def db():
    server.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with server.app.app_context():
        server.db_model.db.create_all()
        yield server.db_model
