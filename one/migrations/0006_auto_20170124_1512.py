# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0005_auto_20170124_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='tomonth',
            name='asu',
            field=models.BooleanField(default=False, verbose_name='\u041e\u0431\u043e\u0440\u0443\u0434\u043e\u0432\u0430\u043d\u0438\u0435 \u0410\u0421\u0423?'),
        ),
        migrations.AddField(
            model_name='tomonth',
            name='kip',
            field=models.BooleanField(default=False, verbose_name='\u041e\u0431\u043e\u0440\u0443\u0434\u043e\u0432\u0430\u043d\u0438\u0435 \u041a\u0418\u041f?'),
        ),
        migrations.AddField(
            model_name='tomonth',
            name='prim',
            field=models.CharField(blank=True, default=b'', max_length=200, verbose_name='\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='tomonth',
            name='status',
            field=models.BooleanField(default=True, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441'),
        ),
    ]
