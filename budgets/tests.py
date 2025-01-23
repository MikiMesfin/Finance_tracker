from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Budget
from accounts.models import User, Currency
from decimal import Decimal

class BudgetTests(APITestCase):
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
        
    def test_create_budget(self):
        data = {
            'name': 'Monthly Budget',
            'amount': '1000.00',
            'currency': self.currency.id,
            'start_date': '2024-03-01',
            'end_date': '2024-03-31'
        }
        
        response = self.client.post(reverse('budget-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 1)
        self.assertEqual(Budget.objects.get().amount, Decimal('1000.00'))
