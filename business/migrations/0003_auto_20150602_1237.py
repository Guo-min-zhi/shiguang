# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150529_1000'),
        ('business', '0002_auto_20150602_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiguang',
            name='end_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='shiguang',
            name='start_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='shiguang',
            name='user',
            field=models.ForeignKey(default=1, to='users.User'),
            preserve_default=False,
        ),
    ]
