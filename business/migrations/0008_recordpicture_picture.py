# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0007_record_shiguang'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordpicture',
            name='picture',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
