# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150529_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_country_code',
            field=models.CharField(default=b'86', max_length=20),
        ),
    ]
