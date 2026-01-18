import requests

BASE = "http://localhost:8001/api/customers/"


class CustomerClient:

    @staticmethod
    def register(data):
        return requests.post(BASE + "register/", json=data).json()

    @staticmethod
    def login(data):
        return requests.post(BASE + "login/", json=data).json()

    @staticmethod
    def get_customer(customer_id):
        return requests.get(f"{BASE}{customer_id}/").json()
