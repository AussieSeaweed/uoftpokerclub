# Generated by Django 3.1.1 on 2020-09-30 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamemaster', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='restart_timeout',
            field=models.FloatField(default=5),
        ),
    ]