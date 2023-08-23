from rest_framework import generics
from rest_framework.response import Response
from .serializers import UserSerializer, ListAllUsersSerializer
from .models import User


class UserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        weight_kg = self.request.data["weight_kg"]
        goal_ml = round(weight_kg * 35, 2)

        serializer.save(goal_ml=goal_ml)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ListAllUsersSerializer
        return UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        total_goals = sum(user.goal_ml for user in queryset)
        total_average_of_goals = round(total_goals / len(queryset), 2)

        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        custom_object = {"total_average_of_goals": total_average_of_goals}
        serialized_data.append(custom_object)

        return Response(serialized_data)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "user_id"

    def perform_update(self, serializer):
        if "weight_kg" in self.request.data:
            weight_kg = self.request.data["weight_kg"]

            goal_ml = round(weight_kg * 35, 2)

            serializer.save(goal_ml=goal_ml)

        return serializer.save()
