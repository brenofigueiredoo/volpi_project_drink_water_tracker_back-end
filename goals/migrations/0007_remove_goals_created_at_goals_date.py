# Generated by Django 4.2.3 on 2023-08-02 14:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("goals", "0006_alter_goals_goal_consumed_ml_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="goals",
            name="created_at",
        ),
        migrations.AddField(
            model_name="goals",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
