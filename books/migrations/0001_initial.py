# Generated by Django 5.1a1 on 2024-06-09 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("author", models.CharField(max_length=255)),
                (
                    "cover",
                    models.CharField(
                        choices=[("1", "SOFT"), ("2", "HARD")], max_length=2
                    ),
                ),
                ("inventory", models.PositiveIntegerField()),
                ("daily_fee", models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
    ]
