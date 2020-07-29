import pytest
from offer_service import OfferService
import requests
from unittest.mock import Mock


@pytest.fixture
def offer_service():
    return OfferService()


class MockProductResponse:

    def __init__(self, status_code=200):
        self.status_code = status_code

    def json(self):
        if self.status_code < 400:
            return {'success': True, 'access_token': 'dummy'}
        else:
            return {'code': self.status_code, 'msg': 'request failed', 'access_token': 'dummy'}


class MockOfferResponse:

    def __init__(self, status_code=200):
        self.status_code = status_code

    def json(self):
        if self.status_code < 400:
            return [{"id": 1, "price": 1000, "items_in_stock": 4}, {"id": 2, "price": 2000, "items_in_stock": 1}]
        else:
            return {'code': self.status_code, 'msg': 'request failed', 'access_token': 'dummy'}


def test_bearer_token(offer_service):
    assert offer_service.bearer_token.get_token() is not None
    assert len(offer_service.bearer_token.get_token()) > 0


def test_register_product_201(mocker, offer_service):
    response = Mock()
    response.return_value = MockProductResponse(status_code=201)
    mocker.patch('requests.post', response)

    data = offer_service.register_product(10, "Dosqvarna", "Nejlepší pila na ruce i nohy")
    assert 'success' in data


def test_register_product_400(mocker, offer_service):
    response = Mock()
    response.return_value = MockProductResponse(status_code=400)
    mocker.patch('requests.post', response)

    with pytest.raises(requests.HTTPError) as err:
        offer_service.register_product(10, "Dosqvarna", "Nejlepší pila na ruce i nohy")

    assert "400: request failed" in str(err.value)


def test_register_product_401(mocker, offer_service):
    response = Mock()
    response.return_value = MockProductResponse(status_code=401)
    mocker.patch('requests.post', response)

    with pytest.raises(requests.HTTPError) as err:
        offer_service.register_product(10, "Dosqvarna", "Nejlepší pila na ruce i nohy")

    assert response.call_count == 4  # one for token, one for request itself, 2 tries
    assert "401: request failed" in str(err.value)


def test_get_offers_200(mocker, offer_service):
    response = Mock()
    response.return_value = MockOfferResponse(status_code=200)
    mocker.patch('requests.get', response)
    mocker.patch('requests.post')

    data = offer_service.get_offers(10)
    assert len(data) == 2


def test_get_offers_400(mocker, offer_service):
    response = Mock()
    response.return_value = MockOfferResponse(status_code=400)
    mocker.patch('requests.get', response)
    mocker.patch('requests.post')

    with pytest.raises(requests.HTTPError) as err:
        offer_service.get_offers(10)

    assert "400: request failed" in str(err.value)


def test_get_offers_401(mocker, offer_service):
    response = Mock()
    response.return_value = MockOfferResponse(status_code=401)
    mocker.patch('requests.get', response)
    mocker.patch('requests.post')

    with pytest.raises(requests.HTTPError) as err:
        offer_service.get_offers(10)

    assert response.call_count == 2
    assert "401: request failed" in str(err.value)


def test_get_offers_404(mocker, offer_service):
    response = Mock()
    response.return_value = MockOfferResponse(status_code=404)
    mocker.patch('requests.get', response)
    mocker.patch('requests.post')

    data = offer_service.get_offers(10)
    assert len(data) == 0
