from rest_framework import serializers
from .models import Goals
from django.core.validators import MinValueValidator


class GoalSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

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

    def get_user(self, obj):
        user = obj.user
        return {
            "id": user.id,
            "name": user.name,
            "weight_kg": user.weight_kg,
            "goal_ml": user.goal_ml,
        }


class GoalUpdateSerializer(serializers.ModelSerializer):
    quantity = serializers.FloatField(validators=[MinValueValidator(0.0)])

    class Meta:
        model = Goals
        fields = ["quantity"]

    def validate(self, data):
        quantity = data.get("quantity")
        if quantity is None:
            raise serializers.ValidationError(
                {"quantity": ["O campo 'quantity' é obrigatório."]}
            )
        return data
