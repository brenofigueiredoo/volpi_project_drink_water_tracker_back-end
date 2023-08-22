from rest_framework import generics
from .serializers import UserSerializer
from .models import User


class UserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        weight_kg = self.request.data["weight_kg"]
        goal_ml = round(weight_kg * 35, 2)

        serializer.save(goal_ml=goal_ml)


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
