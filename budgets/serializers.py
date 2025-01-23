from rest_framework import serializers
from .models import Budget, FinancialGoal

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ('id', 'name', 'amount', 'currency', 'start_date', 'end_date')

class FinancialGoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = FinancialGoal
        fields = ('id', 'name', 'target_amount', 'currency', 'deadline', 
                 'current_amount', 'progress_percentage')

    def get_progress_percentage(self, obj):
        if obj.target_amount == 0:
            return 0
        return (obj.current_amount / obj.target_amount) * 100
