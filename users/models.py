from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=127, unique=True)
    weight_kg = models.FloatField()
    goal_ml = models.FloatField(default=0)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    last_login = None
    first_name = None
    last_name = None
    date_joined = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
