from celery import shared_task
from django.core.mail import send_mail
from .models import Budget
from expenses.models import Expense
from django.db.models import Sum
from django.conf import settings

@shared_task
def check_budget_alerts():
    budgets = Budget.objects.all()
    for budget in budgets:
        expenses = Expense.objects.filter(
            user=budget.user,
            date__range=[budget.start_date, budget.end_date],
            currency=budget.currency
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        if expenses >= budget.amount * 0.8:  # Alert at 80% of budget
            send_mail(
                'Budget Alert',
                f'You have used {(expenses/budget.amount)*100:.2f}% of your {budget.name} budget',
                settings.DEFAULT_FROM_EMAIL,
                [budget.user.email],
                fail_silently=False,
            )
