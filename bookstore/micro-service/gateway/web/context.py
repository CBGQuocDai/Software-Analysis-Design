from .utils import get_current_user


def current_customer(request):
    return {
        "current_customer": get_current_user(request)
    }
