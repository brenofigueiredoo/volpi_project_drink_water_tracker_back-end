from django.urls import path
from . import views

urlpatterns = [
    path(
        "goals/date/<str:date>",
        views.GoalRetrieveCreateByUserIdView.as_view(),
    ),
    path(
        "goals",
        views.GoalListByUserIdView.as_view(),
    ),
    path(
        "goals/<uuid:goal_id>",
        views.GoalRetrieveDestroyByIdView.as_view(),
    ),
    path(
        "goals/<uuid:goal_id>/drinkwater",
        views.GoalUpdateByIdView.as_view(),
    ),
]
