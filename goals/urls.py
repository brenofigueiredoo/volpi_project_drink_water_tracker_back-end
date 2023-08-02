from django.urls import path
from . import views

urlpatterns = [
    path("goals/<uuid:user_id>", views.GoalView.as_view()),
    path("goals/<uuid:goal_id>/drinkwater", views.GoalDetailView.as_view()),
    # path("users/<uuid:user_id>", views.UserDetailView.as_view()),
]
