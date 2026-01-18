import requests

BASE = "http://localhost:8003/api/carts/"


class CartClient:

    @staticmethod
    def add_to_cart(data):
        return requests.post(BASE + "add/", json=data).json()

    @staticmethod
    def get_cart(customer_id):
        return requests.get(f"{BASE}{customer_id}/").json()
