# Generated by Django 3.1.3 on 2020-12-11 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0006_auto_20201210_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apartment.district'),
        ),
    ]