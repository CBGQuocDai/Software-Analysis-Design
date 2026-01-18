from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Customer
from .serializers import CustomerSerializer, CustomerPublicSerializer


# POST /api/customers/register/
class RegisterAPI(APIView):

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            customer = serializer.save()

            public_serializer = CustomerPublicSerializer(customer)

            return Response(
                public_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# POST /api/customers/login/
class LoginAPI(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Missing credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            customer = Customer.objects.get(email=email, password=password)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = CustomerPublicSerializer(customer)

        return Response(serializer.data, status=status.HTTP_200_OK)


# GET /api/customers/<id>/
class CustomerDetailAPI(APIView):

    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerPublicSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
