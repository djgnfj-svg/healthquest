# Generated by Django 4.2.7 on 2025-06-29 11:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0002_supplement_usersupplement_supplementlog_nutritionlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutritionlog',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
