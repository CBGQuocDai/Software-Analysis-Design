def get_current_customer(request):
    customer_id = request.session.get('customer_id')

    if not customer_id:
        return None

    from accounts.models import Customer

    try:
        return Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return None
