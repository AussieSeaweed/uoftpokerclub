# Generated by Django 3.1.2 on 2020-10-10 04:10

import annoying.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('user', annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('members',
                 models.ManyToManyField(blank=True, related_name='organizations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NLHEStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payoffs', models.BigIntegerField(default=0)),
                ('wins', models.BigIntegerField(default=0)),
                ('losses', models.BigIntegerField(default=0)),
                ('ties', models.BigIntegerField(default=0)),
                ('num_plays', models.BigIntegerField(default=0)),
                ('career',
                 annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, to='community.career')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
