# Generated by Django 3.0.6 on 2020-08-11 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0028_currencies'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Currencies',
            new_name='Currency',
        ),
    ]
