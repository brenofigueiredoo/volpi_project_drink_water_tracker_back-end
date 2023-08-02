from rest_framework import serializers
from .models import Goals


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goals
        fields = [
            "id",
            "goal_of_the_day_ml",
            "remaining_goals_ml",
            "goal_consumed_ml",
            "goal_consumed_percentage",
            "user",
            "date",
        ]
        read_only_fields = [
            "goal_of_the_day_ml",
            "remaining_goals_ml",
            "user",
        ]
