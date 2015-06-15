# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0006_auto_20150615_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='shiguang',
            field=models.ForeignKey(default='', to='business.Shiguang'),
            preserve_default=False,
        ),
    ]
