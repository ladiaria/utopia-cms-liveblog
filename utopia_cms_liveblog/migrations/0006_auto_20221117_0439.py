# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-11-17 04:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utopia_cms_liveblog', '0005_auto_20221117_0412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liveblog',
            name='notification_target_pubs',
            field=models.ManyToManyField(blank=True, to='core.Publication', verbose_name='notification target publications'),
        ),
    ]