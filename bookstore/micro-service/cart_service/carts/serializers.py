from rest_framework import serializers

class BookInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    author = serializers.CharField()
    price = serializers.IntegerField()

class CartItemSerializer(serializers.Serializer):
    book = BookInfoSerializer()
    quantity = serializers.IntegerField()

class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    customer_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    items = CartItemSerializer(many=True)

class AddToCartSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
