# Generated by Django 4.2.3 on 2023-08-01 17:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("goals", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goals",
            name="created_at",
            field=models.DateField(auto_now_add=True),
        ),
    ]
