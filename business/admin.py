#!/usr/local/bin/python
#-*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.
from models import Shiguang, Record, RecordPicture


admin.site.register(Shiguang)
admin.site.register(Record)
admin.site.register(RecordPicture)
