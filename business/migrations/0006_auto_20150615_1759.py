# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_auto_20150615_1437'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shiguang',
            old_name='name',
            new_name='theme',
        ),
        migrations.RemoveField(
            model_name='shiguang',
            name='start_time',
        ),
    ]
