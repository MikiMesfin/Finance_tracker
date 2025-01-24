from rest_framework import serializers
from .models import User, Currency

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'preferred_currency', 'created_at')
        read_only_fields = ('created_at',)

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'code', 'name', 'symbol')
