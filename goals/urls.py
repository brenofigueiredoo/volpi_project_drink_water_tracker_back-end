from django.urls import path
from . import views

urlpatterns = [
    path("goals/user/create/<uuid:user_id>", views.GoalCreateView.as_view()),
    path("goals/user/list/<uuid:user_id>", views.GoalsUserListView.as_view()),
    path("goals/<uuid:goal_id>", views.GoalDetailView.as_view()),
    path("goals/<uuid:goal_id>/drinkwater", views.GoalUpdateView.as_view()),
]
