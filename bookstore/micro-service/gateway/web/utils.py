from .clients.customer import CustomerClient


def get_current_user(request):
    customer_id = request.session.get("customer_id")

    if not customer_id:
        return None

    try:
        return CustomerClient.get_customer(customer_id)
    except:
        return None
