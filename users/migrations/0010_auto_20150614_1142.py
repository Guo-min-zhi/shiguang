# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20150614_1138'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='avatar',
            new_name='avatar_path',
        ),
    ]
