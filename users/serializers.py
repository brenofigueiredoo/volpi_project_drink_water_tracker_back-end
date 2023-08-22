from rest_framework import serializers
from .models import User
from goals.models import Goals


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "weight_kg",
            "goal_ml",
        ]
        read_only_fields = [
            "goal_ml",
        ]


class ListAllUsersSerializer(serializers.ModelSerializer):
    completed_goals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "goal_ml",
            "completed_goals",
        ]

    def get_completed_goals(self, obj: User):
        quantity_of_goals = len(Goals.objects.filter(user_id=obj.id))
        completed_goals = 0

        for goals in Goals.objects.filter(user_id=obj.id):
            if goals.goal_consumed_percentage == 100:
                completed_goals += 1

        return f"{completed_goals}/{quantity_of_goals}"
