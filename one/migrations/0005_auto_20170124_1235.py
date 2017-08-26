# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 09:35
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0004_tomonth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tomonth',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='one.TOMonth', verbose_name='\u0420\u043e\u0434\u0438\u0442\u0435\u043b\u044c'),
        ),
    ]
