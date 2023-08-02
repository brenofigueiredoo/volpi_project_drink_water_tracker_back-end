from typing import Any
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


class Goals(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    goal_of_the_day_ml = models.FloatField(validators=[MinValueValidator(0.0)])
    remaining_goals_ml = models.FloatField(
        default=0, validators=[MinValueValidator(0.0)]
    )
    goal_consumed_ml = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
    goal_consumed_percentage = models.FloatField(
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )
    date = models.DateField(unique=True)

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="goals"
    )
