# Generated by Django 3.0.6 on 2020-07-17 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0025_plannervalue_area_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaSizeAndUnits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('unit', models.CharField(max_length=40)),
            ],
        ),
    ]
