# Generated by Django 3.1.4 on 2021-01-15 04:35

from django.db import migrations, models
import django.db.models.deletion
import picklefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('timeout', models.FloatField(default=1)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('game', picklefield.fields.PickledObjectField(blank=True, editable=False, null=True)),
                ('_seats', picklefield.fields.PickledObjectField(blank=True, editable=False, null=True)),
            ],
            options={
                'verbose_name': 'Room',
            },
        ),
        migrations.CreateModel(
            name='SequentialRoom',
            fields=[
                ('room_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gamemaster.room')),
            ],
            options={
                'verbose_name': 'Sequential Room',
            },
            bases=('gamemaster.room',),
        ),
        migrations.CreateModel(
            name='TicTacToeRoom',
            fields=[
                ('sequentialroom_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gamemaster.sequentialroom')),
            ],
            options={
                'verbose_name': 'Tic Tac Toe Room',
            },
            bases=('gamemaster.sequentialroom',),
        ),
    ]
