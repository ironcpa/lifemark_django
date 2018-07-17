# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-12 07:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lifemark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('link', models.TextField(blank=True, default='')),
                ('category', models.TextField(blank=True, default='')),
                ('is_complete', models.TextField(blank=True, default='')),
                ('due_datehour', models.TextField(blank=True, default='')),
                ('rating', models.TextField(blank=True, default='')),
                ('tags', models.TextField(blank=True, default='')),
                ('desc', models.TextField(blank=True, default='')),
                ('image_url', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default=None, null=True)),
                ('category', models.TextField(default='', null=True)),
                ('state', models.TextField(null=True)),
            ],
        ),
    ]
