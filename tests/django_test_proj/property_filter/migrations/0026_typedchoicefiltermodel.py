# Generated by Django 3.0.7 on 2020-07-04 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_filter', '0025_choicefiltermodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypedChoiceFilterModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('truth', models.CharField(max_length=32)),
            ],
        ),
    ]
