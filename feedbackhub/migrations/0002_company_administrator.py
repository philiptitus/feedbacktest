# Generated by Django 5.0.2 on 2024-06-11 08:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feedbackhub", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="administrator",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="administered_companies",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
