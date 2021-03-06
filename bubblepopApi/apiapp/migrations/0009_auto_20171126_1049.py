# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 10:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0008_merge_20171125_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(default='정치', max_length=10, null=True, verbose_name='분류'),
        ),
        migrations.AlterField(
            model_name='article',
            name='cluster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apiapp.Cluster', verbose_name='클러스터'),
        ),
    ]
