# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0009_shiguang_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiguang',
            name='description',
            field=models.CharField(max_length=2000),
        ),
    ]
