from django.urls import path
from . import views

urlpatterns = [
    path(
        "user/<uuid:user_id>/goals/<str:date>",
        views.GoalRetrieveCreateByUserIdView.as_view(),
    ),
    path(
        "user/<uuid:user_id>/goals",
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
