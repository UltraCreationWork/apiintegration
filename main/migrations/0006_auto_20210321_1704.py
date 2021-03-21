# Generated by Django 3.1.6 on 2021-03-21 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210321_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placeorder',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of Order'),
        ),
        migrations.AlterField(
            model_name='placeorder',
            name='strategy_tag',
            field=models.CharField(choices=[('START1', 'START1'), ('START2', 'START2'), ('START3', 'START3')], max_length=50, verbose_name='StrategyTag'),
        ),
    ]
