# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-09 18:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weights', '0012_auto_20170906_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pigeonuser',
            name='achievements',
        ),
    ]
