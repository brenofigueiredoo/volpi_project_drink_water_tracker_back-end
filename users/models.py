from django.db import models
import uuid


class User(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=127)
    weight_kg = models.FloatField()
    goal_ml = models.FloatField(default=0)
