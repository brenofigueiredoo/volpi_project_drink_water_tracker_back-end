from rest_framework import generics, status
from .serializers import GoalSerializer, GoalUpdateSerializer
from .models import Goals
from users.serializers import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import serializers


class GoalListCreateView(generics.ListCreateAPIView):
    serializer_class = GoalSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Goals.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.kwargs["user_id"]
        user = get_object_or_404(User, pk=user_id)

        dateExists = Goals.objects.filter(
            user_id=user_id, date=self.request.data["date"]
        )

        if dateExists:
            raise serializers.ValidationError({"date": ["Date already exists"]})

        goal_of_the_day_ml = round(user.weight_kg * 35, 2)

        serializer.save(user=user, goal_of_the_day_ml=goal_of_the_day_ml)


class GoalDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = GoalSerializer
    queryset = Goals.objects.all()
    lookup_url_kwarg = "goal_id"


class GoalUpdateView(generics.UpdateAPIView):
    serializer_class = GoalUpdateSerializer
    queryset = Goals.objects.all()
    lookup_url_kwarg = "goal_id"

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return GoalUpdateSerializer
        return GoalSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.refresh_from_db()  # Atualiza o objeto a partir do banco de dados
        serializer = GoalSerializer(
            instance
        )  # Cria um novo serializer com o objeto atualizado
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        quantity_ml = self.request.data["quantity"]

        goal_id = self.kwargs["goal_id"]
        goal = get_object_or_404(Goals, pk=goal_id)

        goal_of_the_day_ml = goal.goal_of_the_day_ml

        goal_consumed_ml = goal.goal_consumed_ml + quantity_ml

        remaining_goals_ml = goal.goal_of_the_day_ml - goal_consumed_ml

        if remaining_goals_ml < 0:
            remaining_goals_ml = 0

        goal_consumed_percentage = round(
            100 - (remaining_goals_ml / goal_of_the_day_ml) * 100, 2
        )

        if goal_consumed_percentage > 100:
            goal_consumed_percentage = 100

        return serializer.save(
            goal_of_the_day_ml=goal_of_the_day_ml,
            remaining_goals_ml=remaining_goals_ml,
            goal_consumed_ml=goal_consumed_ml,
            goal_consumed_percentage=goal_consumed_percentage,
        )
