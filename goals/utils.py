from datetime import datetime
from rest_framework import serializers


def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise serializers.ValidationError({"detail": ["Invalid date format"]})
