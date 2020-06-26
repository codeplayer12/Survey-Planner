# Generated by Django 3.0.6 on 2020-06-24 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0006_auto_20200624_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetitem',
            name='days',
            field=models.FloatField(blank=True, default=1, max_length=11),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='budgetitem',
            name='department',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='planner.Department'),
        ),
        migrations.AlterField(
            model_name='budgetitem',
            name='unit',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='budgetitem',
            name='unitCost',
            field=models.IntegerField(blank=True),
        ),
    ]