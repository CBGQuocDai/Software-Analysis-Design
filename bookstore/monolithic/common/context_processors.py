from .utils import get_current_customer

def current_customer(request):
    return {
        'current_customer': get_current_customer(request)
    }
