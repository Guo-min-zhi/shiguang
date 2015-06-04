# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shiguang',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('first_level_tag', models.CharField(max_length=100, choices=[(b'LIFE', b'life'), (b'WORK', b'work')])),
                ('cover', models.ImageField(upload_to=b'covers')),
            ],
        ),
    ]
