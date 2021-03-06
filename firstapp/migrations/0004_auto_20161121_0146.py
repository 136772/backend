# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 01:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('firstapp', '0003_auto_20161105_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to='avatar')),
                ('gender', models.CharField(choices=[(('0', '男'), ('1', '女'))], default='0', max_length=10)),
                ('belong_to', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='ticket',
            name='choice',
            field=models.CharField(choices=[('like', 'like'), ('dislike', 'dislike'), ('normal', 'normal')], max_length=10),
        ),
    ]
