# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_auto_20150602_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=1000)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecordPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('record', models.ForeignKey(to='business.Record')),
            ],
        ),
        migrations.RemoveField(
            model_name='shiguang',
            name='first_level_tag',
        ),
        migrations.AddField(
            model_name='shiguang',
            name='tags',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='shiguang',
            name='cover',
            field=models.ImageField(upload_to=b''),
        ),
    ]
