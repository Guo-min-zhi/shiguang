# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_auto_20150615_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiguang',
            name='cover',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
