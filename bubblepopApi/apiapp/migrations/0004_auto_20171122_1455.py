# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 14:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0003_auto_20171118_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(default='정치', max_length=10, verbose_name='분류'),
        ),
        migrations.AlterField(
            model_name='article',
            name='cluster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='apiapp.Cluster', verbose_name='클러스터'),
        ),
        migrations.AlterField(
            model_name='article',
            name='published_at',
            field=models.DateField(auto_now_add=True, verbose_name='발행일'),
        ),
    ]
