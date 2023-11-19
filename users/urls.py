from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("users", views.UserView.as_view()),
    path("users/detail", views.UserDetailView.as_view()),
    path("login", TokenObtainPairView.as_view()),
]
