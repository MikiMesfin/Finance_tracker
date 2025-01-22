from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer
from django.http import HttpResponse
from .utils import generate_csv, generate_pdf
from .analysis import SpendingAnalyzer

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        
        queryset = self.get_queryset().filter(
            date__year=year,
            date__month=month
        )
        
        total = sum(expense.amount for expense in queryset)
        by_category = {}
        
        for expense in queryset:
            category = expense.category.name if expense.category else 'Uncategorized'
            by_category[category] = by_category.get(category, 0) + expense.amount
        
        return Response({
            'total': total,
            'by_category': by_category
        })

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        expenses = self.get_queryset()
        csv_content = generate_csv(expenses)
        
        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
        return response

    @action(detail=False, methods=['get'])
    def export_pdf(self, request):
        expenses = self.get_queryset()
        pdf_content = generate_pdf(expenses, request.user)
        
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="expenses.pdf"'
        return response

    @action(detail=False, methods=['get'])
    def analysis(self, request):
        analyzer = SpendingAnalyzer(request.user)
        patterns = analyzer.get_spending_patterns()
        return Response(patterns)
