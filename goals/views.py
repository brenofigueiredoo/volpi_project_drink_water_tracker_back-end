from rest_framework import generics, status
from .serializers import GoalSerializer, GoalUpdateSerializer
from .models import Goals
from users.serializers import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import serializers
from .utils import validate_date_format
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwnerOfGoal, IsUserLogged
from drf_spectacular.utils import extend_schema


@extend_schema(
    description="{date} = yyyy-MM-dd",
    tags=["Goals"],
)
class GoalRetrieveCreateByUserIdView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserLogged]

    serializer_class = GoalSerializer

    def get_queryset(self):
        user = self.request.user
        date = self.kwargs["date"]
        validate_date_format(date)

        goals = Goals.objects.filter(user=user, date=date)

        if len(goals) <= 0:
            raise serializers.ValidationError({"detail": "Not found"})

        return goals

    def perform_create(self, serializer):
        user = self.request.user
        date = self.kwargs["date"]
        validate_date_format(date)

        date_exists = Goals.objects.filter(user=user, date=date)

        if date_exists:
            raise serializers.ValidationError({"detail": ["Date already exists"]})

        serializer.save(
            user=user,
            goal_of_the_day_ml=user.goal_ml,
            remaining_goals_ml=user.goal_ml,
            date=date,
        )


@extend_schema(tags=["Goals"])
class GoalListByUserIdView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserLogged]
    serializer_class = GoalSerializer

    def get_queryset(self):
        user = self.request.user
        return Goals.objects.filter(user=user)


@extend_schema(tags=["Goals"])
class GoalRetrieveDestroyByIdView(generics.RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOfGoal]

    serializer_class = GoalSerializer
    queryset = Goals.objects.all()
    lookup_url_kwarg = "goal_id"


@extend_schema(tags=["Goals"])
class GoalUpdateByIdView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOfGoal]

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

        goal_of_the_day_ml = goal.user.goal_ml

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
