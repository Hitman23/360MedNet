# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-01 12:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_qualification_field_of_study'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profession',
            options={'verbose_name_plural': 'Professions'},
        ),
        migrations.AlterModelOptions(
            name='specialization',
            options={'verbose_name_plural': 'Specializations'},
        ),
    ]
