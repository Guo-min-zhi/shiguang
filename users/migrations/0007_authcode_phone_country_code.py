# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_phone_country_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='authcode',
            name='phone_country_code',
            field=models.CharField(default=b'86', max_length=20),
        ),
    ]
