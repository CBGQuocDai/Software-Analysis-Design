import requests


BOOK_SERVICE_URL = "http://localhost:8002/api/books/"


class BookServiceClient:

    @staticmethod
    def get_book(book_id):
        try:
            res = requests.get(f"{BOOK_SERVICE_URL}{book_id}/")

            if res.status_code == 200:
                return res.json()

            return None
        except:
            return None
        
CUSTOMER_SERVICE_URL = "http://localhost:8001/api/customers/"


class CustomerServiceClient:

    @staticmethod
    def get_customer(customer_id):
        try:
            res = requests.get(f"{CUSTOMER_SERVICE_URL}{customer_id}/")

            if res.status_code == 200:
                return res.json()

            return None
        except:
            return None
