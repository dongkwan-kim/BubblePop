# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0004_auto_20171123_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_url',
            field=models.URLField(unique=True, verbose_name='URL 링크'),
        ),
    ]
