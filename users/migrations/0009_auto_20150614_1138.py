# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar_path',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to=b'avatar', blank=True),
        ),
    ]
