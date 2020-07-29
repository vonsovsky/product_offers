import json
import pytest
import server


@pytest.fixture
def client(db):
    with server.app.test_client() as client:
        yield client


def test_add_product(client):
    data = {'name': 'Zámek', 'description': 'Vybydlený zámek ve starém městě bez vodovodu'}
    client.post('/products/', data=data)
    data = {'name': 'Důl', 'description': 'Uzavřený uhelný důl OKD promořený koronavirem'}
    client.post('/products/', data=data)
    data = {'name': 'Lavička u nádraží', 'description': 'Podnájem na lavičce, blízkost k centru, sociální kontakt'}
    client.post('/products/', data=data)


def test_get_products(client):
    response = client.get('/products/')
    data = json.loads(response.data)
    assert len(data) == 3
    assert data[0]['name'] == 'Zámek'


def test_update_product(client):
    data = {'name': 'Krámek', 'description': 'Vybydlený zámek ve starém městě bez vodovodu'}
    client.put('/products/1/', data=data)

    response = client.get('/products/')
    data = json.loads(response.data)
    assert len(data) == 3
    assert data[0]['name'] == 'Krámek'


def test_delete_product(client):
    client.delete('/products/1/')

    response = client.get('/products/')
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['name'] == 'Důl'
