# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('sn', models.CharField(max_length=30)),
                ('extra', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'test',
            },
        ),
    ]
