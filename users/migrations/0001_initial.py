# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authcode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=100)),
                ('auth_code', models.IntegerField()),
                ('send_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AuthcodeHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=100)),
                ('auth_code', models.IntegerField()),
                ('send_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=100)),
                ('nick_name', models.CharField(max_length=100)),
                ('real_name', models.CharField(max_length=100)),
                ('sex', models.IntegerField(default=0)),
                ('birthday', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('avatar_path', models.CharField(max_length=200)),
                ('register_date', models.DateTimeField()),
            ],
        ),
    ]
