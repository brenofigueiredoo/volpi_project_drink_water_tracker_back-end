from rest_framework import serializers
from .models import User


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
