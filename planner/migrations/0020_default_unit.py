# Generated by Django 3.0.6 on 2020-07-17 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0019_budgetestimate_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='default',
            name='unit',
            field=models.CharField(default='kilometres', max_length=255),
        ),
    ]
