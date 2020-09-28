# Generated by Django 3.1.1 on 2020-09-27 19:30

import django.db.models.deletion
import picklefield.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('game', picklefield.fields.PickledObjectField(blank=True, editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TicTacToeRoom',
            fields=[
                ('room_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='gamemaster.room')),
            ],
            bases=('gamemaster.room',),
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamemaster.room')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           related_name='seats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
