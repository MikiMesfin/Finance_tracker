from rest_framework import serializers
from .models import Category, Expense

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'icon')

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Expense
        fields = ('id', 'amount', 'currency', 'category', 'category_name', 
                 'description', 'date', 'created_at')
        read_only_fields = ('created_at',)
