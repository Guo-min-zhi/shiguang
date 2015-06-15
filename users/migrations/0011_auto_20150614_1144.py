# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20150614_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_path',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
