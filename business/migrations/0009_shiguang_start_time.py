# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0008_recordpicture_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiguang',
            name='start_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
