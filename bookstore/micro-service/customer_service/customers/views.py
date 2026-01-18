import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Customer


# POST /api/customers/register/
@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body)

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return JsonResponse({"error": "Missing fields"}, status=400)

    if Customer.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already exists"}, status=400)

    customer = Customer.objects.create(
        name=name,
        email=email,
        password=password
    )

    return JsonResponse({
        "id": customer.id,
        "name": customer.name,
        "email": customer.email
    })


# POST /api/customers/login/
@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body)

    email = data.get("email")
    password = data.get("password")

    try:
        customer = Customer.objects.get(email=email, password=password)
    except Customer.DoesNotExist:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({
        "id": customer.id,
        "name": customer.name,
        "email": customer.email
    })


# GET /api/customers/<id>/
def customer_detail(request, customer_id):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return JsonResponse({"error": "Customer not found"}, status=404)

    return JsonResponse({
        "id": customer.id,
        "name": customer.name,
        "email": customer.email
    })
