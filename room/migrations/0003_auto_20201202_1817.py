# Generated by Django 3.1.3 on 2020-12-02 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_auto_20201202_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='latitude',
            field=models.DecimalField(decimal_places=15, max_digits=20),
        ),
        migrations.AlterField(
            model_name='room',
            name='longitude',
            field=models.DecimalField(decimal_places=15, max_digits=20),
        ),
    ]
