# Generated by Django 4.2.7 on 2023-12-02 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tracker", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pricetracker",
            name="email",
            field=models.EmailField(default="default@example.com", max_length=254),
            preserve_default=False,
        ),
    ]