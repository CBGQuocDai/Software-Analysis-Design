from rest_framework import serializers
from .models import Customer


# Dùng cho create/update
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'password']


# Dùng để trả dữ liệu cho client (không lộ password)
class CustomerPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email']
