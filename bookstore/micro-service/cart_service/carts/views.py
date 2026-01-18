from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartSerializer, AddToCartSerializer
from .clients import BookServiceClient, CustomerServiceClient

class AddToCartAPI(APIView):
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        customer_id = serializer.validated_data["customer_id"]
        book_id = serializer.validated_data["book_id"]
        quantity = serializer.validated_data["quantity"]
        # Check customer tồn tại
        customer = CustomerServiceClient.get_customer(customer_id)
        if not customer:
            return Response(
                {"error": "Customer does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Check book tồn tại
        book = BookServiceClient.get_book(book_id)
        if not book:
            return Response(
                {"error": "Book does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        cart, _ = Cart.objects.get_or_create(customer_id=customer_id)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            book_id=book_id,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()
        # Sau khi thêm xong trả về luôn cart mới
        return GetCartAPI().get(request, customer_id)
class GetCartAPI(APIView):
    def get(self, request, customer_id):
        # Check customer tồn tại
        customer = CustomerServiceClient.get_customer(customer_id)
        if not customer:
            return Response(
                {"error": "Customer does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        cart = Cart.objects.filter(customer_id=customer_id).first()
        if not cart:
            return Response(
                {
                    "id": None,
                    "customer_id": customer_id,
                    "items": []
                },
                status=status.HTTP_200_OK
            )
        items_data = []
        for item in CartItem.objects.filter(cart=cart):
            book = BookServiceClient.get_book(item.book_id)
            if not book:
                continue
            items_data.append({
                "book": {
                    "id": book.get("id"),
                    "title": book.get("title"),
                    "price": book.get("price"),
                    "author": book.get("author"),
                },
                "quantity": item.quantity
            })
        response_data = {
            "id": cart.id,
            "customer_id": cart.customer_id,
            "created_at": cart.created_at,
            "items": items_data
        }
        serializer = CartSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
