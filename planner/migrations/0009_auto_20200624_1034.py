# Generated by Django 3.0.6 on 2020-06-24 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0008_auto_20200624_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgetitem',
            name='days',
            field=models.FloatField(blank=True, max_length=11, null=True),
        ),
    ]