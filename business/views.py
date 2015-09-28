import os
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from .functions import *
from .models import Shiguang, Record, RecordPicture
import logging
from shiguang.settings import *
from django.template import RequestContext, loader

logger = logging.getLogger('shiguang')

# Create your views here.

def index(request):
	context = {'name': 'guominzhi'}
	return render(request, 'business/index.html', context)

def all(request):
	data = {}
	PAGE_SIZE = 5
	if request.method == 'GET':
		uid = request.GET.get('uid', '')
		page = request.GET.get('page', 1)
		logger.info('Get all shiguang, uid = %s, page = %s', uid, page)
		
		try:
			page = int(page)
			if page < 1:
				page = 1
		except Exception:
			page = 1

		data['data'] = []
		lists = Shiguang.objects.filter(user_id=uid)
		pager = Paginator(lists, PAGE_SIZE)
		try:
			lists = pager.page(page)
		except Exception:
			lists = pager.page(1)

		for item in lists:
			data['data'].append(jsonShiguang(item))

		data['code'] = 1
		#data['total_page'] = pager.num_pages
		data['msg'] = 'get all shiguang list'
		return JsonResponse(data)
	else:
		data['code'] = 0
		data['data'] = []
		data['msg'] = 'get shiguang list api need get method.'
		return JsonResponse(data)

def add(request):
	data = {}
	if request.method == 'POST':
		user_id = request.POST.get('uid', 1)
		theme = request.POST.get('name', '')
		description = request.POST.get('description', '')
		start_time = request.POST.get('start', '')
		end_time = request.POST.get('end', '')
		tags = request.POST.get('tags','')
		logger.info("add shiguang,user_id=%s,theme=%s,description=%s,start_time=%s,end_time=%s,tags=%s", user_id,theme,description,start_time,end_time,tags)

		try:
			cover = request.FILES['cover']
			cover_path = os.path.join(MEDIA_ROOT,'cover', user_id+'_cover_'+str(generateRandomNumber())+'.jpg')
			handle_shiguang_cover_file(cover, cover_path)
			logger.info("save cover success")	

			shiguang = Shiguang(theme=theme,description=description,start_time=start_time,end_time=end_time,tags=tags,user_id=user_id)
			shiguang.save()
			logger.info("save shiguang success")
		except Exception, e:
			logger.error(e)
			data['code'] = 0
			data['msg'] = 'create error'
			data['data'] = ''
			return JsonResponse(data)

		data['code'] = 1
		data['msg'] = 'Create shiguang success.'
		data['data'] = jsonShiguang(shiguang)
		return JsonResponse(data)
	else:
		data['code'] = 0
		data['msg'] = 'This api need post method'
		data['data'] = ''
		return JsonResponse(data)

def getLineOldPage(request):
	data = {}
	if request.method == 'GET':
		uid = request.GET.get('uid','')
		max_index = request.GET.get('max_index','')
		logger.info("Get %s's shiguang old then %s", uid, max_index)
		
		if uid != '' and max_index != '':
			data['data'] = []
			lists = Shiguang.objects.filter(user_id=uid).filter(id__lt=max_index).order_by('-create_time')[:5]
			for item in lists:
				data['data'].append(jsonShiguang(item))
			data['code'] = 1
			data['msg'] = 'get shiguang list small then %s' % uid
			return JsonResponse(data)
	
	data['code'] = 0
	data['msg'] = 'This api occurs error.'
	data['data'] = []
	return JsonResponse(data)

def getLineNew(request):
	data = {}
	if request.method == 'GET':
		uid = request.GET.get('uid','')
		min_index = request.GET.get('min_index','')
		logger.info("Get %s's all new shiguang new then %s", uid, min_index)

		if uid != '' and min_index != '':
			data['data'] = []
			lists = Shiguang.objects.filter(user_id=uid).filter(id__gt=min_index).order_by('-create_time')
			for item in lists:
				data['data'].append(jsonShiguang(item))
			data['code'] = 1
			data['msg'] = 'get shiguang list new then %s' % uid
			return JsonResponse(data)
	data['code'] = 0
	data['msg'] = 'This api occurs error.'
	data['data'] = []
	return JsonResponse(data)

def getUndoneOldPage(request):
	data = {}
	if request.method == 'GET':
		uid = request.GET.get('uid','')
		max_index = request.GET.get('max_index','')
		logger.info("Get %s's all unfinished shiguang old then %s", uid, max_index)
		if uid != '' and max_index != '':
			data['data'] = []
			lists = Shiguang.objects.filter(user_id=uid).filter(end_time=None).filter(id__lt=max_index).order_by('-create_time')[:5]
			for item in lists:
				data['data'].append(jsonShiguang(item))
			data['code'] = 1
			data['msg'] = "get user-%s's unfinished shiguang list small then %s" % (uid, max_index)
			return JsonResponse(data)
	data['code'] = 0
	data['msg'] = 'This api occurs error.'
	data['data'] = []
	return JsonResponse(data)

def getUndoneNew(request):
	data = {}
	if request.method == 'GET':
		uid = request.GET.get('uid','')
		min_index = request.GET.get('min_index', '')
		logger.info("Get %s's all unfinished shiguang new then %s", uid, min_index)
		if uid != '' and min_index != '':
			data['data'] = []
			lists = Shiguang.objects.filter(user_id=uid).filter(end_time=None).filter(id__gt=min_index).order_by('-create_time')
			for item in lists:
				data['data'].append(jsonShiguang(item))
			data['code'] = 1
			data['msg'] = "get user-%s's unfinished shiguang list new then %s" % (uid, min_index)
			return JsonResponse(data)
	data['code'] = 0
	data['msg'] = 'This api occurs error.'
	data['data'] = []
	return JsonResponse(data)

def addRecord(request):
	data = {}
	if request.method == 'POST':
		content = request.POST.get('content', '')

def getRecordsOfMonth(request):
	data = {}
	if request.method == 'GET':
		sid = request.GET.get('sid', None)
		month = request.GET.get('month', None)
		logger.info("get records of %s-shiguang and %s-month" % (sid, month))
		try:
			month = int(month)
			if sid != None and month != None:
				data['data'] = []
				records = Record.objects.filter(shiguang_id=sid)
				for record in records:
					if record.create_time.month == month:
						data['data'].append(record.create_time.day)

				data['code'] = 1
				data['msg'] = "get records of %s-shiguang and %s-month" % (sid, month)
				return JsonResponse(data)
		except Exception:
			pass
	data['code'] = 0
	data['msg'] = 'This api occurs error'
	data['data'] = []
	return JsonResponse(data)

def getAllRecordsOfShiguang(request):
	data = {}
	if request.method == 'GET':
		sid = request.GET.get('sid', None)
		logger.info("get records of shiguang id = %s", sid)
		try:
			data['data'] = []
			if sid != None:
				records = Record.objects.filter(shiguang_id=sid)
				for item in records:
					data['data'].append(jsonRecord(item))

			data['code'] = 1
			data['msg'] = "get records of %s-shiguang" % sid
			return JsonResponse(data)
		except Exception, e:
			raise e
			data['code'] = 0
			data['msg'] = 'This api occurs error.'
			data['data'] = []
			return JsonResponse(data)
	else:
		data['code'] = 0
		data['msg'] = 'This url need GET method.'
		data['data'] = []
		return JsonResponse(data)

def getRecordInfo(request):
	data = {}
	if request.method == 'GET':
		rid = request.GET.get('rid', None)
		logger.info("get record info of %s", rid)
		if rid != None:
			data['data'] = {}
			record = Record.objects.get(pk=rid)
			data['data']['info'] = jsonRecord(record)
			data['data']['pictures'] = []
			pictures = RecordPicture.objects.filter(record_id=rid)
			for p in pictures:
				data['data']['pictures'].append(p.picture)
			data['code'] = 1
			data['msg'] = 'get record info of %s' % rid
			return JsonResponse(data)


























