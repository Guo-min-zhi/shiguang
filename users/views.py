#!/usr/local/bin/python
#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from .models import Authcode, User, FeedBack
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
	try:
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
			print "step 1"
			avatar = request.FILES['avatar']
			print "step 2"
			avatar_name = 'avatar'+str(generateRandomNumber())+'.jpg'
			avatar_path = os.path.join(MEDIA_ROOT,'avatar', avatar_name)
			handle_uploaded_file(avatar, avatar_path)
			avatar_url = os.path.join(MEDIA_URL,'avatar', avatar_name)
		
			# print "step 1"
			# form = UploadFileForm(request.POST, request.FILES)
			# if form.is_valid():
			# 	print '=========='
			# 	print request.FILES['avatar']
			# 	print '============'
		
			#handle_uploaded_file(request.FILES['avatar'])

		except Exception as e:
			print e
			data['code'] = 0
			data['msg'] = "Do not have avatar."
			data['data'] = ''
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
		print("--------------------")

		
		
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
		user = User(phone_number=phone_number,phone_country_code=phone_country_code,password=password,nick_name=nick_name,sex=sex,birthday=birthday,avatar_path=avatar_url)
		user.save()
		# 5. Delete temp data in Authcode table.
		authcode.delete()

		data['code'] = 1
		data['msg'] = "Register success."
		data['data'] = jsonUser(user)
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)
	except Exception as ee:
		print ee
		data['code'] = 0
		data['msg'] = "Internal error."
		data['data'] = ''
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
		data['data'] = jsonUser(user)
		data['msg'] = "login success."
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
	except Exception:
		data['code'] = 0
		data['data'] = jsonUser(User())
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

def changeNickname(request):
	data = {}
	if request.method == 'POST':
		uid = request.POST.get('uid', '')
		nickname = request.POST.get('nickname', '')
		if uid == '' or nickname == '':
			data['code'] = 0
			data['msg'] = "User Id or Nick name can't be null."
			data['data'] = ''
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
		else:
			try:
				user = User.objects.get(pk=uid)
				user.nick_name = nickname
				user.save()
				data['code'] = 1
				data['msg'] = 'Change nickname to [%s] success of user [%s]' %  (nickname, uid)
				data['data'] = jsonUser(user)
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
			except Exception, e:
				data['code'] = 0
				data['msg'] = "Can't find user of %s." % uid
				data['data'] = '%s' % e
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
	else:
		data['code'] = 0
		data['msg'] = "This api need POST method."
		data['data'] = ''
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)

def changeSex(request):
	data = {}
	if request.method == 'POST':
		uid = request.POST.get('uid', '')
		sex = request.POST.get('sex', '')
		if uid == '' or sex == '':
			data['code'] = 0
			data['msg'] = "User Id or sex can't be null."
			data['data'] = ''
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
		else:
			try:
				user = User.objects.get(pk=uid)
				user.sex = sex
				user.save()
				data['code'] = 1
				data['msg'] = 'Change sex to [%s] success of user [%s]' %  (sex, uid)
				data['data'] = jsonUser(user)
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
			except Exception, e:
				data['code'] = 0
				data['msg'] = "Can't find user of %s." % uid
				data['data'] = '%s' % e
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
	else:
		data['code'] = 0
		data['msg'] = "This api need POST method."
		data['data'] = ''
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)


def changeBirthday(request):
	data = {}
	if request.method == 'POST':
		uid = request.POST.get('uid', '')
		birthday = request.POST.get('birthday', '')
		if uid == '' or birthday == '':
			data['code'] = 0
			data['msg'] = "User Id or birthday can't be null."
			data['data'] = ''
			logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
			return JsonResponse(data)
		else:
			try:
				user = User.objects.get(pk=uid)
				user.birthday = birthday
				user.save()
				data['code'] = 1
				data['msg'] = 'Change birthday to [%s] success of user [%s]' %  (birthday, uid)
				data['data'] = jsonUser(user)
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
			except Exception, e:
				data['code'] = 0
				data['msg'] = "Can't find user of %s." % uid
				data['data'] = '%s' % e.messages
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
	else:
		data['code'] = 0
		data['msg'] = "This api need POST method."
		data['data'] = ''
		logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
		return JsonResponse(data)

def changePassword(request):
	data = {}
	if request.method == 'POST':
		uid = request.POST.get('uid', '')
		password = request.POST.get('password', '')
		if uid == '' or password == '':
			data['code'] = 0
			data['msg'] = "User Id or password can't be null."
			data['data'] = ''
		else:
			try:
				user = User.objects.get(pk=uid)
				user.password = password
				user.save()
				data['code'] = 1
				data['msg'] = 'Change password success of user [%s]' % uid
				data['data'] = jsonUser(user)
			except Exception, e:
				data['code'] = 0
				data['msg'] = "Can't find user of %s." % uid
				data['data'] = '%s' % e.messages
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
	else:
		data['code'] = 0
		data['msg'] = "This api need POST method."
		data['data'] = ''
	logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
	return JsonResponse(data)

def changeTelephone(request):
	data = {}
	if request.method == 'POST':
		uid = request.POST.get('uid', '')
		phone_country_code = request.POST.get('areaCode', '')
		telephone = request.POST.get('telephone', '')
		authcode = request.POST.get('authcode', '')
		if uid == '' or telephone == '' or authcode == '':
			data['code'] = 0
			data['msg'] = "User Id [%s] or telephone number[%s] or authcode [%s] can't be null." % (uid, telephone, authcode)
			data['data'] = ''
		else:
			try:
				if isRegistered(telephone, phone_country_code):
					data['code'] = 0
					data['msg'] = "The phone number has been registered."
					data['data'] = ''
				else:
					authcode = Authcode.objects.get(phone_number=telephone,code=authcode)
					authcode.delete()
					user = User.objects.get(pk=uid)
					user.phone_number = telephone
					user.save()
					data['code'] = 1
					data['msg'] = 'Change telephone number to [%s] success of user [%s]' %  (telephone, uid)
					data['data'] = jsonUser(user)
			except Exception, e:
					data['code'] = 0
					data['msg'] = "phone number does not match auth code."
					data['data'] = '%s' % e.messages
					logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
					return JsonResponse(data)
	else:
		data['code'] = 0
		data['msg'] = "This api need POST method."
		data['data'] = ''
	logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
	return JsonResponse(data)


def changeAvatar(request):
	data = {}
	if request.method == 'POST':
		uid = request.POST.get('uid', '')
		print "step 1"
		avatar = request.FILES['avatar']
		print "step 2"
		if uid == '' or avatar == '':
			data['code'] = 0
			data['msg'] = "User Id or avatar can't be null."
			data['data'] = ''
		else:
			
			try:
				# upload avatar
				print("--------------------")
				avatar_name = 'avatar'+str(generateRandomNumber())+'.jpg'
				avatar_path = os.path.join(MEDIA_ROOT,'avatar', avatar_name)
				handle_uploaded_file(avatar, avatar_path)
				avatar_url = os.path.join(MEDIA_URL,'avatar', avatar_name)

				user = User.objects.get(pk=uid)
				user.avatar_path = avatar_url
				user.save()
				print("--------------------")
				data['code'] = 1
				data['msg'] = 'Change avatar to [%s] success of user [%s]' %  (avatar_path, uid)
				data['data'] = jsonUser(user)
			except Exception, e:
				print e
				data['code'] = 0
				data['msg'] = "Do not have avatar."
				data['data'] = '%s' % e.messages
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
	else:
		data['code'] = 0
		data['msg'] = "This api need POST method."
		data['data'] = ''
	logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
	return JsonResponse(data)

def authcodeVerify(request):
	data = {}
	if request.method == 'POST':
		phone = request.POST.get('telephone', '')
		code = request.POST.get('authcode', '')
		if phone == '' or code == '':
			data['code'] = 0
			data['msg'] = "Phone number or authcode can't be null."
			data['data'] = ''
		else:
			try:
				authcode = Authcode.objects.get(phone_number=phone,code=code)
				authcode.delete()
				data['code'] = 1
				data['msg'] = "Verify code is valid."
				data['data'] = code
			except Exception, e:
				data['code'] = 0
				data['msg'] = "phone number does not match auth code. [%s] " % e
				data['data'] = ''
				logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
				return JsonResponse(data)
	else:
		data['code'] = 0
		data['msg'] = "This api need POST method."
		data['data'] = ''
	logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
	return JsonResponse(data)

def findPasswordBefore(request):
	data = {}
	if request.method == 'GET':
		phone_number = request.GET.get('phone', '')
		phone_country_code = request.GET.get('phone_country_code', '')
		if phone_number == '' or phone_country_code == '':
			data['code'] = 0
			data['msg'] = "phone number or country code is null."
			data['data'] = ''
		else:
			if isRegistered(phone_number, phone_country_code):
				code = generateRandomNumber()
				if sendAuthcode(phone_number, code):
					authcode = Authcode(phone_number=phone_number, code=code, phone_country_code=phone_country_code)
					authcode.save()
					data['code'] = 1
					data['msg'] = "send auth success."
					data['data'] = ''
				else:
					data['code'] = 0
					data['msg'] = "Send authcode fail."
					data['data'] = ''
			else:
				data['code'] = 0
				data['msg'] = "This phone number [%s-%s] has not been registered." % (phone_country_code,phone_number)
				data['data'] = ''
	else:
		data['code'] = 0
		data['msg'] = "This method need POST method."
		data['data'] = ''
	logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
	return JsonResponse(data)
	
def findPassword(request):
	data = {}
	if request.method == 'POST':
		phone = request.POST.get('phone', '')
		password = request.POST.get('password', '')
		if phone == '' or password == '':
			data['code'] = 0
			data['msg'] = "Phone number or password can't be null."
			data['data'] = ''
		else:
			user = User.objects.get(phone_number=phone)
			user.password = password
			user.save()
			data['code'] = 1
			data['msg'] = 'Find password success of telephone [%s]' %  phone
			data['data'] = jsonUser(user)
	else:
		data['code'] = 0
		data['msg'] = "This api need POST method."
		data['data'] = ''
	logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
	return JsonResponse(data)




#----------------------------- for web page ----------------------------

def loginPage(request):
	context = {}
	if request.method == 'GET':
		return render(request, 'users/login.html', context)
	else:
		# 1. Has phone number and password
		phone_number = request.POST.get('phone', None)
		# login through user id 
		uid = request.POST.get('uid', None)
		password = request.POST.get('password', None)
		logger.info("phone_number=%s,uid=%s,password=%s", phone_number, uid, password)
		# 2. query the phone number and password.
		try:
			if phone_number == None:
				user = User.objects.get(uid=uid, password=password)
			else:
				user = User.objects.get(phone_number=phone_number, password=password)
		except Exception as e:
			print e
		return render(request, 'users/home.html', context)	

def registerPage(request):
	context = {}
	if request.method == 'GET':
		return render(request, 'users/register.html', context)
	elif request.method == 'POST':
		return HttpResponseRedirect('/users/info')
		# check if the phone number is equal to code
		# try:
		# 	authcode = Authcode.objects.get(phone_number=phone_number,code=code)
		# 	return render(request, 'users/home.html', context)
		# except Exception as e:
		# 	print e
		# 	return render(request, 'users/register.html', context)

def homePage(request):
	context = {}
	return render(request, 'users/home.html', context)

def setUserInfo(request):
	userId = 2
	user = User.objects.get(pk=userId)
	return render(request, 'users/userInfo.html', {'user': user})

def addFeedback(request):
	data = {}
	if request.method == 'POST':
		uid = request.POST.get('uid', '')
		feedback = request.POST.get('feedback','')
		contact = request.POST.get('contact','')
		if uid == '' or feedback == '':
			data['code'] = 0
			data['msg'] = "uid or feedback can't be null."
			data['data'] = ''
		else:
			try:
				fb = FeedBack(user_id=uid, feedback=feedback, contact=contact)
				fb.save()
				data['code'] = 1
				data['msg'] = "Add Feedback success."
				data['data'] = ''
			except Exception, e:
				data['code'] = 0
				data['msg'] = "Add Feedback fail."
				data['data'] = '%s' % e
	else:
		data['code'] = 0
		data['msg'] = "This api need POST method."
		data['data'] = ''
	logger.info("Return data: code=%s, msg=%s, data=%s.", data['code'], data['msg'], data['data'])
	return JsonResponse(data)






