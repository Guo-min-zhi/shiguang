from django.shortcuts import render
from django.http import JsonResponse
from .models import Authcode, User
from .functions import *
# Create your views here.

# Send the auth code to phone number.
def auth(request):
	data = {}
	if request.method == 'GET':
		# 1. Has phone number.
		if not request.GET.has_key('phone') or not request.GET.has_key('phone_country_code'):
			data['code'] = 0
			data['msg'] = "Do not have phone number"
			data['data'] = ''
			return JsonResponse(data)
		# 2. Phone number has not been registered.
		try:
			phone_number = request.GET['phone']
			phone_country_code = request.GET['phone_country_code']
		except DoesNotExist:
			data['code'] = 0
			data['msg'] = "auth fail, do not have phone number."
			data['data'] = ''
			return JsonResponse(data)
		if isRegistered(phone_number, phone_country_code):
			data['code'] = 0
			data['msg'] = "The phone number has been registered."
			data['data'] = ''
			return JsonResponse(data)
		# 3. Generate the random auth code
		code = generateRandomNumber()
		# 4. Send message.
		if sendAuthcode(phone_number, code):
			# save the auth code to database.
			authcode = Authcode(phone_number=phone_number, code=code, phone_country_code=phone_country_code)
			authcode.save()
			data['code'] = 1
			data['msg'] = "auth success."
			data['data'] = ''
		else:
			data['code'] = 0
			data['msg'] = "auth fail."
			data['data'] = ''
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
	
	# 2. Phone number has not been registered.
	if isRegistered(phone_number, phone_country_code):
		data['code'] = 0
		data['msg'] = "The phone number has been registered."
		data['data'] = ''
		return JsonResponse(data)
	# 3. If phone number match the code.
	try:
		authcode = Authcode.objects.get(phone_number=phone_number,code=code)
	except Exception:
		data['code'] = 0
		data['msg'] = "phone number does not match auth code."
		data['data'] = ''
		return JsonResponse(data)
	# 4. Save registered user.
	user = User(phone_number=phone_number,phone_country_code=phone_country_code,password=password,nick_name=nick_name,sex=sex,birthday=birthday)
	user.save()
	# 5. Delete temp data in Authcode table.
	authcode.delete()

	data['code'] = 1
	data['msg'] = "Register success."
	data['data'] = user.id
	return JsonResponse(data)

def login(request):
	data = {}
	# 1. Has phone number and password
	# if not request.POST.has_key('phone') or not request.POST.has_key('password'):
	# 	data['code'] = 0
	# 	data['data'] = ''
	# 	data['msg'] = "Do not have phone number or password"
	# 	return JsonResponse(data)
	phone_number = request.POST.get('phone', None)
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
	except Exception:
		data['code'] = 0
		data['data'] = ''
		data['msg'] = "login fail."
	return JsonResponse(data)

def userInfo(request):
	data = {}
	if not request.POST.has_key('userId'):
		data['code'] = 0
		data['msg'] = "Do not have user id."
		return JsonResponse(data)
	try:
		userId = request.POST['userId']
		user = User.objects.get(pk=userId)
		data['code'] = 1
		data['msg'] = 'get user info success'
		data['user'] = jsonUser(user)
		return JsonResponse(data)
	except Exception:
		data['code'] = 0
		data['msg'] = "Can not find this user."
		return JsonResponse(data)

def all(request):
	user = User.objects.get(pk=1)
	return JsonResponse(jsonUser(user))









