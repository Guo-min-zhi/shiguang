from django.shortcuts import render
from django.http import JsonResponse
from .models import Authcode, User
from .functions import *
import logging
import os
from shiguang.settings import *

# Create your views here.

logger = logging.getLogger('shiguang')

# Send the auth code to phone number.
def auth(request):
	data = {}
	if request.method == 'GET':
		# 1. Has phone number.
		if not request.GET.has_key('phone') or not request.GET.has_key('phone_country_code'):
			data['code'] = 0
			data['msg'] = "Do not have phone number"
			data['data'] = ''
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
		# 2. Phone number has not been registered.
		try:
			phone_number = request.GET['phone']
			phone_country_code = request.GET['phone_country_code']
		except DoesNotExist:
			data['code'] = 0
			data['msg'] = "send auth fail, do not have phone number."
			data['data'] = ''
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
		if isRegistered(phone_number, phone_country_code):
			data['code'] = 0
			data['msg'] = "The phone number has been registered."
			data['data'] = ''
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
		# 3. Generate the random auth code
		code = generateRandomNumber()
		# 4. Send message.
		if sendAuthcode(phone_number, code):
			# save the auth code to database.
			authcode = Authcode(phone_number=phone_number, code=code, phone_country_code=phone_country_code)
			authcode.save()
			data['code'] = 1
			data['msg'] = "send auth success."
			data['data'] = ''
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		else:
			data['code'] = 0
			data['msg'] = "send auth fail."
			data['data'] = ''
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)

def register(request):
	data = {}

	# 1. valid phone number and code and password
	# if not request.POST.has_key('phone') or not request.POST.has_key('verifyCode') or request.POST.has_key('password'):
	# 	data['code'] = 0
	# 	data['msg'] = "Don't have 'phone' or 'verifyCode' or 'password'."
	# 	data['data'] = ''
	# 	return JsonResponse(data) 
	
	phone_number = request.POST.get('phone', '')
	phone_country_code = request.POST.get('phone_country_code','')
	code = request.POST.get('verifyCode','')
	password = request.POST.get('password','')
	nick_name = request.POST.get('username','')
	sex = request.POST.get('sex',0)
	birthday = request.POST.get('birthday',None)
	#avatar = request
	print("--------------------")
	try:
		avatar = request.FILES['avatar']
		avatar_path = os.path.join(MEDIA_ROOT,'avatar',user_id, 'avatar'+str(generateRandomNumber())+'.jpg')
		handle_uploaded_file(avatar, avatar_path)
	except Exception, e:
		data['code'] = 0
		data['msg'] = "Do not have avatar."
		data['data'] = ''
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)
	print("--------------------")

	# form = UploadFileForm(request.POST, request.FILES)
	# if form.is_valid():
	# 	print '=========='
	# 	print request.FILES['avatar']
	# 	print '============'
	
		#handle_uploaded_file(request.FILES['avatar'])
	
	# 2. Phone number has not been registered.
	if isRegistered(phone_number, phone_country_code):
		data['code'] = 0
		data['msg'] = "The phone number has been registered."
		data['data'] = ''
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)
	# 3. If phone number match the code.
	try:
		authcode = Authcode.objects.get(phone_number=phone_number,code=code)
	except Exception:
		data['code'] = 0
		data['msg'] = "phone number does not match auth code."
		data['data'] = ''
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)
	# 4. Save registered user.
	user = User(phone_number=phone_number,phone_country_code=phone_country_code,password=password,nick_name=nick_name,sex=sex,birthday=birthday,avatar_path=avatar_path)
	user.save()
	# 5. Delete temp data in Authcode table.
	authcode.delete()

	data['code'] = 1
	data['msg'] = "Register success."
	data['data'] = user.id
	logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
	return JsonResponse(data)

def login(request):
	data = {}
	# 1. Has phone number and password
	# if not request.POST.has_key('phone') or not request.POST.has_key('password'):
	# 	data['code'] = 0
	# 	data['data'] = ''
	# 	data['msg'] = "Do not have phone number or password"
	# 	return JsonResponse(data)
	# login through phone number
	phone_number = request.POST.get('phone', None)
	# login through user id 
	uid = request.POST.get('uid', None)
	password = request.POST.get('password', None)
	print 'phone_number=%s,uid=%s,password=%s' % (phone_number, uid, password)
	# 2. query the phone number and password.
	try:
		if phone_number == None:
			user = User.objects.get(uid=uid, password=password)
		else:
			user = User.objects.get(phone_number=phone_number, password=password)
		data['code'] = 1
		data['data'] = user.id
		data['msg'] = "login success."
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
	except Exception:
		data['code'] = 0
		data['data'] = ''
		data['msg'] = "login fail."
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
	return JsonResponse(data)

def userInfo(request):
	data = {}
	if not request.GET.has_key('uid'):
		data['code'] = 0
		data['msg'] = "Do not have user id."
		data['data'] = ""
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)
	try:
		userId = request.GET['uid']
		user = User.objects.get(pk=userId)
		data['code'] = 1
		data['msg'] = 'get user info success'
		data['data'] = jsonUser(user)
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)
	except Exception:
		data['code'] = 0
		data['msg'] = "Can not find this user."
		data['data'] = ""
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)

def all(request):
	logger.info('------')
	print '*********'
	user = User.objects.get(pk=1)
	return JsonResponse(jsonUser(user))

def handle_uploaded_file(f, f_path):
    with open(f_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)









