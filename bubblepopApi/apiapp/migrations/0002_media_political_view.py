# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-13 12:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='political_view',
            field=models.FloatField(default=0.1, verbose_name='성향'),
            preserve_default=False,
        ),
    ]
