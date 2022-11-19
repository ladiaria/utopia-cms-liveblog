# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-11-18 23:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utopia_cms_liveblog', '0005_auto_20221117_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liveblog',
            name='notification',
            field=models.BooleanField(default=False, help_text='If checked and the blog status is active or to begin, shows an alert related to this blog in articles and publication home pages.', verbose_name='notification'),
        ),
        migrations.AlterField(
            model_name='liveblog',
            name='notification_target_pubs',
            field=models.ManyToManyField(blank=True, help_text='Alerts will be shown only in the pages (homes/articles) related to the publications selected.', to='core.Publication', verbose_name='notification target publications'),
        ),
    ]
