#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import os, time
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from .functions import *
from .models import Shiguang, Record, RecordPicture
import logging
from shiguang.settings import *
from django.template import RequestContext, loader
from django.db.models import Q
from django.shortcuts import get_object_or_404

logger = logging.getLogger('shiguang')

# Create your views here.


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
		lists = Shiguang.objects.filter(user_id=uid).order_by('-create_time')
		pager = Paginator(lists, PAGE_SIZE)
		try:
			listsOfPage = pager.page(page)
			for item in listsOfPage.object_list:
				data['data'].append(jsonShiguang(item))

			data['code'] = 1
			#data['total_page'] = pager.num_pages
			data['msg'] = 'get all shiguang list of page = %s' % page
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
		except Exception:
			data['code'] = 1
			#data['total_page'] = pager.num_pages
			data['msg'] = 'get all shiguang list of page = %s' % page
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
			
	else:
		data['code'] = 0
		data['data'] = []
		data['msg'] = 'get shiguang list api need get method.'
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)

def add(request):
	data = {}
	if request.method == 'POST':
		user_id = request.POST.get('uid', 1)
		theme = request.POST.get('name', None)
		description = request.POST.get('description', '')
		start_time = request.POST.get('start', None)
		end_time = request.POST.get('end', None)
		if end_time == "":
			end_time = None
		tags = request.POST.get('tags',None)
		logger.info("add shiguang,user_id=%s,theme=%s,description=%s,start_time=%s,end_time=%s,tags=%s", user_id,theme,description,start_time,end_time,tags)

		try:
			cover = request.FILES['cover']
			cover_name = user_id+'_cover_'+str(generateRandomNumber())+'.jpg'
			cover_path = os.path.join(MEDIA_ROOT,'cover', cover_name)
			handle_shiguang_file(cover, cover_path)
			cover_url = os.path.join(MEDIA_URL,'cover', cover_name)
			logger.info("save cover success")	

			shiguang = Shiguang(theme=theme,description=description,start_time=start_time,end_time=end_time,tags=tags,user_id=user_id,cover=cover_url)
			shiguang.save()
			logger.info("save shiguang success")
		except Exception, e:
			logger.error(e)
			data['code'] = 0
			data['msg'] = 'create error'
			data['data'] = jsonShiguang(Shiguang())
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)

		data['code'] = 1
		data['msg'] = 'Create shiguang success.'
		data['data'] = jsonShiguang(shiguang)
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)
	else:
		data['code'] = 0
		data['msg'] = 'This api need post method'
		data['data'] = jsonShiguang(Shiguang())
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
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
	# date text pic0 pic1 ...	
	if request.method == 'POST':
		try:
			content = request.POST.get('text', '')
			date = request.POST.get('date', '')
			shiguang_id = request.POST.get('timeSetId', '')
			logger.info("Receive shiguang_id=%s, content=%s, date=%s", shiguang_id, content, date)

			record = Record(content=content, date=date, shiguang_id=shiguang_id)
			record.save()
			logger.info("Record save success, record_id = %s", record.id)

			try:
				pic0 = request.FILES['pic0']
				if pic0:
					pic0_name = 'record'+str(generateRandomNumber())+'.jpg'
					pic0_path = os.path.join(MEDIA_ROOT,'record', pic0_name)
					handle_shiguang_file(pic0, pic0_path)
					pic0_url = os.path.join(MEDIA_URL,'record', pic0_name)

					recordPicture = RecordPicture(picture=pic0_url, record_id=record.id)
					recordPicture.save()
					logger.info("Save picture 1 success.")
			except Exception, e:
				print e
				pass

			try:
				pic1 = request.FILES['pic1']
				if pic1:
					pic1_name = 'record'+str(generateRandomNumber())+'.jpg'
					pic1_path = os.path.join(MEDIA_ROOT,'record', pic1_name)
					handle_shiguang_file(pic1, pic1_path)
					pic1_url = os.path.join(MEDIA_URL,'record', pic1_name)
					recordPicture = RecordPicture(picture=pic1_url, record_id=record.id)
					recordPicture.save()
					logger.info("Save picture 2 success")
			except Exception, e:
				print e
				pass

			try:
				pic2 = request.FILES['pic2']
				if pic2:
					pic2_name = 'record'+str(generateRandomNumber())+'.jpg'
					pic2_path = os.path.join(MEDIA_ROOT,'record', pic2_name)
					handle_shiguang_file(pic2, pic2_path)
					pic2_url = os.path.join(MEDIA_URL,'record', pic2_name)
					recordPicture = RecordPicture(picture=pic2_url, record_id=record.id)
					recordPicture.save()
					logger.info("Save picture 3 success")
			except Exception, e:
				print e
				pass

			try:
				pic3 = request.FILES['pic3']
				if pic3:
					pic3_name = 'record'+str(generateRandomNumber())+'.jpg'
					pic3_path = os.path.join(MEDIA_ROOT,'record', pic3_name)
					handle_shiguang_file(pic3, pic3_path)
					pic3_url = os.path.join(MEDIA_URL,'record', pic3_name)
					recordPicture = RecordPicture(picture=pic3_url, record_id=record.id)
					recordPicture.save()
					logger.info("Save picture 4 success")
			except Exception, e:
				print e
				pass

			try:
				pic4 = request.FILES['pic4']
				if pic4:
					pic4_name = 'record'+str(generateRandomNumber())+'.jpg'
					pic4_path = os.path.join(MEDIA_ROOT,'record', pic4_name)
					handle_shiguang_file(pic4, pic4_path)
					pic4_url = os.path.join(MEDIA_URL,'record', pic4_name)
					recordPicture = RecordPicture(picture=pic4_url, record_id=record.id)
					recordPicture.save()
					logger.info("Save picture 5 success")
			except Exception, e:
				print e
				pass

			try:
				pic5 = request.FILES['pic5']
				if pic5:
					pic5_name = 'record'+str(generateRandomNumber())+'.jpg'
					pic5_path = os.path.join(MEDIA_ROOT,'record', pic5_name)
					handle_shiguang_file(pic5, pic5_path)
					pic5_url = os.path.join(MEDIA_URL,'record', pic5_name)
					recordPicture = RecordPicture(picture=pic5_url, record_id=record.id)
					recordPicture.save()
					logger.info("Save picture 6 success")
			except Exception, e:
				print e
				pass

			data['code'] = 1
			data['msg'] = "Add record success."
			dataOfData = {}
			dataOfData['id'] = record.id
			dataOfData['date'] = date
			data['data'] = dataOfData
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)

		except Exception as e:
			print e
			data['code'] = 0
			data['msg'] = "Add record fail"
			data['data'] = 'error'
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)

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
				records = Record.objects.filter(shiguang_id=sid).order_by('date')
				for item in records:
					data['data'].append(jsonRecordForAll(item))

			data['code'] = 1
			data['msg'] = "get records of %s-shiguang" % sid
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
		except Exception, e:
			raise e
			data['code'] = 0
			data['msg'] = 'This api occurs error.'
			data['data'] = []
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
	else:
		data['code'] = 0
		data['msg'] = 'This url need GET method.'
		data['data'] = []
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)

def getRecordInfo(request):
	data = {}
	if request.method == 'GET':
		rid = request.GET.get('rid', None)
		logger.info("get record info of %s", rid)
		if rid != None:
			data['data'] = {}
			record = Record.objects.get(pk=rid)
			data['data'] = jsonRecord(record)
			data['data']['pictures'] = []
			pictures = RecordPicture.objects.filter(record_id=rid)
			for p in pictures:
				data['data']['pictures'].append(p.picture)
			data['code'] = 1
			data['msg'] = 'get record info of %s' % rid
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)

def deleteOneRecord(request):
	data = {}
	if request.method == 'GET':
		rid = request.GET.get('rid', None)
		logger.info("Receive record id = %s", rid)
		if rid != None:
			try:
				record = Record.objects.get(pk=rid)
				record.delete()
				data['code'] = 1
				data['msg'] = 'delete record of %s' % rid
				data['data'] = rid
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
			except Record.DoesNotExist:
				data['code'] = 0
				data['msg'] = 'Does not exist of record %s' % rid
				data['data'] = rid
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
		else:
			data['code'] = 0
			data['msg'] = 'there is no record id'
			data['data'] = ''
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
	else:
		data['code'] = 0
		data['msg'] = 'This method need GET method'
		data['data'] = ''
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)

def deleteOneShiguang(request):
	data = {}
	if request.method == 'GET':
		sid = request.GET.get('sid', None)
		logger.info("Receive shiguang id = %s", sid)
		if sid != None:
			try:
				shiguang = Shiguang.objects.get(pk=sid)
				shiguang.delete()
				data['code'] = 1
				data['msg'] = 'delete shiguang of %s' % sid
				data['data'] = sid
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
			except Shiguang.DoesNotExist:
				data['code'] = 0
				data['msg'] = 'Does not exist of shiguang %s' % sid
				data['data'] = sid
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
				
		else:
			data['code'] = 0
			data['msg'] = 'there is no shiguang id'
			data['data'] = ''
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
	else:
		data['code'] = 0
		data['msg'] = 'This method need GET method'
		data['data'] = ''
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)


def shiguangComplete(request):
	data = {}
	if request.method == 'GET':
		sid = request.GET.get('sid', None)
		logger.info("Receive shiguang id = %s", sid)
		if sid != None:
			try:
				shiguang = Shiguang.objects.get(pk=sid)
				competeTime = time.strftime('%Y-%m-%d %H:%I:%M',time.localtime(time.time()))
				shiguang.end_time = competeTime
				shiguang.save()
				data['code'] = 1
				data['msg'] = 'Complete shiguang of %s' % sid
				data['data'] = sid
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
			except Shiguang.DoesNotExist:
				data['code'] = 0
				data['msg'] = 'Does not exist of shiguang %s' % sid
				data['data'] = rid
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
				
		else:
			data['code'] = 0
			data['msg'] = 'there is no shiguang id'
			data['data'] = ''
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
	else:
		data['code'] = 0
		data['msg'] = 'This method need GET method'
		data['data'] = ''
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)

def getUndoneShiguang(request):
	data = {}
	PAGE_SIZE = 5
	if request.method == 'GET':
		uid = request.GET.get('uid', '')
		page = request.GET.get('page', 1)
		logger.info('Get undone shiguang, uid = %s, page = %s', uid, page)
		
		try:
			page = int(page)
			if page < 1:
				page = 1
		except Exception:
			page = 1

		data['data'] = []
		lists = Shiguang.objects.filter(Q(user_id=uid) & Q(end_time=None)).order_by('-create_time')
		pager = Paginator(lists, PAGE_SIZE)
		try:
			listsOfPage = pager.page(page)
			for item in listsOfPage.object_list:
				data['data'].append(jsonShiguang(item))

			data['code'] = 1
			#data['total_page'] = pager.num_pages
			data['msg'] = 'get undone shiguang list of page = %s' % page
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
		except Exception:
			data['code'] = 1
			#data['total_page'] = pager.num_pages
			data['msg'] = 'get undone shiguang list of page = %s' % page
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
	else:
		data['code'] = 0
		data['data'] = []
		data['msg'] = 'get undone shiguang list api need get method.'
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)
		


# ============= for web page ===============

def index(request):
	datas = []
	if request.method == 'GET':
		uid = request.GET.get('uid', '')
		if uid != '':
			lists = Shiguang.objects.filter(user_id=uid)
			for item in lists:
				datas.append(jsonShiguang(item))
	context = {'data': datas}
	return render(request, 'business/index.html', context)


def shiguangIndex(request):
	data = []
	if request.method == 'GET':
		sid = request.GET.get('sid', '')
		if sid != '':
			shiguang = Shiguang.objects.get(id=sid)
			recordList = Record.objects.filter(shiguang_id=sid).order_by('-date')
			for record in recordList:
				rid = record.id
				record.pictures = []
				pictureList = RecordPicture.objects.filter(record_id=rid)
				if len(pictureList) != 0:
					record.pictures.append(pictureList[0])

				# for picture in pictureList:
				# 	record.pictures.append(picture)
				# data.append(jsonRecordForWeb(record))
				data.append(record)
	context= {}
	context['records'] = data
	context['shiguang'] = shiguang
	# context = {'records': data}

	return render(request, 'business/shiguang.html', context)

def recordSharePage(request):
	data = []
	if request.method == 'GET':
		rid = request.GET.get('rid', '')
		if rid != '':
			record = get_object_or_404(Record, id=rid)
			sid = record.shiguang_id
			shiguang = get_object_or_404(Shiguang, id=sid)
			record.pictures = []
			pictureList = RecordPicture.objects.filter(record_id=rid)
			for picture in pictureList:
				record.pictures.append(picture)

	context = {}
	context['record'] = record
	context['shiguang'] = shiguang
	context['show'] = len(record.pictures)
	return render(request, 'business/day.html', context)






















