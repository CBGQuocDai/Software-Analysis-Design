from framework.apps.models import Customer


def current_customer(request):
    customer_id = request.session.get('customer_id')

    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
            return {'current_customer': customer}
        except Customer.DoesNotExist:
            pass

    return {'current_customer': None}
