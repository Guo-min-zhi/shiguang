# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20150614_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_path',
            field=models.ImageField(upload_to=b'avatar', blank=True),
        ),
    ]
