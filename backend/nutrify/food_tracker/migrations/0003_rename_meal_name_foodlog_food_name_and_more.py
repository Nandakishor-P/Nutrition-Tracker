# Generated by Django 5.1.2 on 2024-12-23 12:17

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_tracker', '0002_goal_waterlog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodlog',
            old_name='meal_name',
            new_name='food_name',
        ),
        migrations.RemoveField(
            model_name='foodlog',
            name='carbs',
        ),
        migrations.RemoveField(
            model_name='foodlog',
            name='date',
        ),
        migrations.RemoveField(
            model_name='foodlog',
            name='fats',
        ),
        migrations.RemoveField(
            model_name='foodlog',
            name='protein',
        ),
        migrations.AddField(
            model_name='foodlog',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foodlog',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='foodlog',
            name='calories',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
