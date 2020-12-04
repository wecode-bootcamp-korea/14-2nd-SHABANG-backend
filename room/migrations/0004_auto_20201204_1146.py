# Generated by Django 3.1.3 on 2020-12-04 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0003_auto_20201202_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='available_date',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='maintenance_cost',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='rent',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='trade_date',
            field=models.DateTimeField(null=True),
        ),
    ]
