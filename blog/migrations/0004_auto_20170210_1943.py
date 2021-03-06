# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170210_0941'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-create_time']},
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag'),
        ),
        migrations.AddField(
            model_name='tag',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='tag',
            name='article',
        ),
    ]
