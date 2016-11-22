# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 04:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0006_auto_20161121_0159'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='choice',
            field=models.CharField(choices=[('like', 'like'), ('normal', 'normal'), ('dislike', 'dislike')], max_length=10),
        ),
    ]
