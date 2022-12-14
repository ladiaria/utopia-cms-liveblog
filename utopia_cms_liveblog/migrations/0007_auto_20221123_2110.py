# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-11-23 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utopia_cms_liveblog', '0006_auto_20221118_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liveblog',
            name='description',
            field=models.CharField(blank=True, max_length=140, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='liveblog',
            name='title',
            field=models.CharField(max_length=128, unique=True, verbose_name='title'),
        ),
    ]
