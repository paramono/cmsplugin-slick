# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-28 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_slick', '0004_auto_20170429_0124'),
    ]

    operations = [
        migrations.AddField(
            model_name='carousel',
            name='height',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='height'),
        ),
    ]
