# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 09:37
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0009_journal_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentitem',
            name='text',
            field=ckeditor.fields.RichTextField(verbose_name='\u0422\u0435\u043a\u0441\u0442'),
        ),
    ]
