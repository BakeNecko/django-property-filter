# Generated by Django 3.0.8 on 2020-09-01 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_filter', '0042_benchmarktestmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='benchmarktestmodel',
            name='uuid',
            field=models.UUIDField(null=True),
        ),
    ]