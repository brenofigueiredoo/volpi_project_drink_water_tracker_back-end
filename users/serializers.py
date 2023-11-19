from rest_framework import serializers
from .models import User
from goals.models import Goals


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "weight_kg",
            "goal_ml",
            "email",
            "password",
        ]
        read_only_fields = [
            "goal_ml",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance


class ListAllUsersSerializer(serializers.ModelSerializer):
    completed_goals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
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
