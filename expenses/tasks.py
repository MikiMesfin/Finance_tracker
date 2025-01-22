from celery import shared_task
from django.db.models import Sum
from .models import Expense
from datetime import datetime, timedelta

@shared_task
def generate_monthly_report(user_id):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    expenses = Expense.objects.filter(
        user_id=user_id,
        date__range=[start_date, end_date]
    )
    
    total_spent = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    category_breakdown = expenses.values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    return {
        'total_spent': total_spent,
        'category_breakdown': list(category_breakdown),
        'period': {
            'start': start_date,
            'end': end_date
        }
    }
