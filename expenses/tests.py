from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Expense
from accounts.models import User, Currency
from decimal import Decimal

class ExpenseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.currency = Currency.objects.create(
            code='USD',
            name='US Dollar',
            symbol='$'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_create_expense(self):
        category = Category.objects.create(
            name='Food',
            user=self.user
        )
        
        data = {
            'amount': '50.00',
            'currency': self.currency.id,
            'category': category.id,
            'description': 'Lunch',
            'date': '2024-03-20'
        }
        
        response = self.client.post(reverse('expense-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.get().amount, Decimal('50.00'))
