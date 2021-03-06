# Generated by Django 3.1.3 on 2020-12-02 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='latitude',
            field=models.DecimalField(decimal_places=15, max_digits=20),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='longitude',
            field=models.DecimalField(decimal_places=15, max_digits=20),
        ),
        migrations.AlterField(
            model_name='convenientstore',
            name='latitude',
            field=models.DecimalField(decimal_places=15, max_digits=20),
        ),
        migrations.AlterField(
            model_name='convenientstore',
            name='longitude',
            field=models.DecimalField(decimal_places=15, max_digits=20),
        ),
        migrations.AlterField(
            model_name='school',
            name='latitude',
            field=models.DecimalField(decimal_places=15, max_digits=20),
        ),
        migrations.AlterField(
            model_name='school',
            name='longitude',
            field=models.DecimalField(decimal_places=15, max_digits=20),
        ),
        migrations.AlterField(
            model_name='subway',
            name='latitude',
            field=models.DecimalField(decimal_places=15, max_digits=20),
        ),
        migrations.AlterField(
            model_name='subway',
            name='longitude',
            field=models.DecimalField(decimal_places=15, max_digits=20),
        ),
    ]
