import random
import logging

logger = logging.getLogger('shiguang')

def jsonShiguang(shiguang):
	data = {}
	data['id'] = shiguang.id
	data['theme'] = shiguang.theme
	data['description'] = shiguang.description
	data['create_time'] = shiguang.create_time
	data['end_time'] = shiguang.end_time
	data['tags'] = shiguang.tags
	data['cover'] = shiguang.cover
	return data

def jsonRecord(record):
	data = {}
	data['content'] = record.content
	data['create_time'] = record.create_time
	return data

def generateRandomNumber():
	return random.randint(100000, 999999)


def handle_shiguang_cover_file(f, path):
	logger.info('save image %s to %s', f, path)
	with open(path, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
