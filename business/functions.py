#!/usr/local/bin/python
#-*- coding:utf-8 -*-
import random
import logging
import datetime

logger = logging.getLogger('shiguang')

def jsonShiguang(shiguang):
	data = {}
	data['id'] = shiguang.id
	data['theme'] = shiguang.theme
	data['description'] = shiguang.description
	data['create_time'] = shiguang.create_time
	data['start_time'] = shiguang.start_time
	data['end_time'] = shiguang.end_time
	data['tags'] = shiguang.tags
	data['cover'] = shiguang.cover
	return data

def jsonRecord(record):
	data = {}
	data['id'] = record.id
	data['content'] = record.content
	data['create_time'] = record.create_time.strftime('%Y-%m-%d %H:%M:%S')
	return data

def jsonRecordForWeb(record):
	data = {}
	data['id'] = record.id
	data['content'] = record.content
	data['date'] = record.date
	data['create_time'] = record.create_time.strftime('%Y-%m-%d %H:%M:%S')
	return data

def jsonRecordForAll(record):
	data = {}
	data['id'] = record.id
	data['date'] = record.date.strftime('%Y-%m-%d')
	return data

def generateRandomNumber():
	return random.randint(100000, 999999)


def handle_shiguang_file(f, path):
	logger.info('save image %s to %s', f, path)
	with open(path, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
