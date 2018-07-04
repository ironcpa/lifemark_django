# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-03 11:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_delete_samplemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='lifemark',
            name='category',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='lifemark',
            name='desc',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='lifemark',
            name='due_date',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='lifemark',
            name='image_url',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='lifemark',
            name='is_complete',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='lifemark',
            name='link',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='lifemark',
            name='rating',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='lifemark',
            name='tags',
            field=models.TextField(default=''),
        ),
    ]