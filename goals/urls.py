from django.urls import path
from . import views

urlpatterns = [
    path("goals/user/<uuid:user_id>", views.GoalView.as_view()),
    path("goals/<uuid:goal_id>", views.GoalRetrieveView.as_view()),
    path("goals/<uuid:goal_id>/drinkwater", views.GoalDetailView.as_view()),
]
