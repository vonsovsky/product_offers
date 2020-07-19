from typing import List, Dict
import requests
from config import Config


class BearerToken:

    def __init__(self) -> None:
        self.access_token = None

    def renew_bearer_token(self) -> None:
        data = requests.post(Config.TOKEN_URL).json()
        self.access_token = data['access_token']

    def get_token(self) -> str:
        if self.access_token is None:
            self.renew_bearer_token()
        return self.access_token

    def reset_token(self) -> None:
        self.access_token = None


class OfferService:
    def __init__(self):
        self.bearer_token = BearerToken()

    def register_product(self, id: int, name: str, description: str, retries: int = 1) -> Dict[str, int]:
        headers = {"Bearer": self.bearer_token.get_token()}
        data = {
            'id': id,
            'name': name,
            'description': description
        }
        response = requests.post(Config.REGISTER_PRODUCT_URL, headers=headers, data=data)
        data = response.json()

        if response.status_code == 201:
            return data
        if response.status_code == 400:
            raise requests.HTTPError("{}: {}".format(data['code'], data['msg']))
        if response.status_code == 401:
            if retries > 0:
                self.bearer_token.reset_token()
                return self.register_product(id, name, description, retries - 1)
            else:
                raise requests.HTTPError("{}: {}".format(data['code'], data['msg']))

    def get_offers(self, id: int, retries: int = 1) -> List[Dict[str, int]]:
        headers = {"Bearer": self.bearer_token.get_token()}
        url = Config.GET_OFFERS_URL.format(id)
        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code == 200:
            return data
        if response.status_code == 400:
            raise requests.HTTPError("{}: {}".format(data['code'], data['msg']))
        if response.status_code == 401:
            if retries > 0:
                self.bearer_token.reset_token()
                self.get_offers(id, retries - 1)
            else:
                raise requests.HTTPError("{}: {}".format(data['code'], data['msg']))
        if response.status_code == 404:
            print("Error not found: {}".format(data['msg']))
            return []
