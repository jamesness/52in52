# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-15 18:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20170115_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieListTitle',
            fields=[
                ('uid', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
    ]
