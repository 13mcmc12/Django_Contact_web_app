# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-22 07:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='providertable',
            name='phone_no',
        ),
        migrations.AddField(
            model_name='providertable',
            name='list',
            field=models.CharField(blank=True, max_length=4),
        ),
    ]
