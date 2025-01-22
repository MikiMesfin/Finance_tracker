from datetime import datetime, timedelta
from django.db.models import Avg, Sum, Count
from .models import Expense

class SpendingAnalyzer:
    def __init__(self, user):
        self.user = user

    def get_spending_patterns(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)  # Last 90 days
        
        expenses = Expense.objects.filter(
            user=self.user,
            date__range=[start_date, end_date]
        )

        patterns = {
            'total_spent': expenses.aggregate(Sum('amount'))['amount__sum'] or 0,
            'average_daily': expenses.aggregate(Avg('amount'))['amount__avg'] or 0,
            'top_categories': list(expenses.values('category__name')
                                 .annotate(total=Sum('amount'))
                                 .order_by('-total')[:5]),
            'spending_frequency': expenses.count(),
            'insights': self._generate_insights(expenses)
        }
        
        return patterns

    def _generate_insights(self, expenses):
        insights = []
        
        # Analyze spending trends
        if expenses.count() > 0:
            avg_amount = expenses.aggregate(Avg('amount'))['amount__avg']
            high_expenses = expenses.filter(amount__gt=avg_amount * 1.5).count()
            
            if high_expenses > 0:
                insights.append(
                    f"You have {high_expenses} expenses that are significantly "
                    "higher than your average spending"
                )

        # Analyze category distribution
        category_spending = expenses.values('category__name').annotate(
            total=Sum('amount'),
            count=Count('id')
        )
        
        for cat in category_spending:
            if cat['count'] > expenses.count() * 0.3:  # More than 30% of transactions
                insights.append(
                    f"Category '{cat['category__name']}' accounts for a large portion "
                    "of your transactions"
                )

        return insights
