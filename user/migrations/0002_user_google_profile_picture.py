# Generated by Django 5.2 on 2025-04-18 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="google_profile_picture",
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
