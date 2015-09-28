from django.shortcuts import get_object_or_404
from .models import User
import random
from .CCPRestSDK import REST
import logging
# functions about users

logger = logging.getLogger('shiguang')

# account id
ACCOUNT_SID = "8a48b5514d32a2a8014d94686ad946c4"
# account token
ACCOUNT_TOKEN = "78def423d2764eabadf89b30d246e5fc"
# app id
APP_ID = "8a48b5514d32a2a8014d9468b91d46c7"
# server ip
SERVER_IP = "sandboxapp.cloopen.com"
# server port
SERVER_PORT = "8883"
# software version
SOFT_VERSION = "2013-12-26"

def generateRandomNumber():
	return random.randint(100000, 999999)

def sendAuthcode(phone_number, code):
	#init
	rest = REST(SERVER_IP, SERVER_PORT, SOFT_VERSION)
	rest.setAccount(ACCOUNT_SID, ACCOUNT_TOKEN)
	rest.setAppId(APP_ID)
	#send phone message auth code
	result = rest.sendTemplateSMS(phone_number,[code, '5'],1)	
	return result['statusCode'] == "000000"


def jsonUser(user):
	data = {}
	data['phone_number'] = user.phone_number
	data['nick_name'] = user.nick_name
	data['real_name'] = user.real_name
	data['sex'] = user.sex
	data['birthday'] = user.birthday
	data['email'] = user.email
	data['avatar_path'] = user.avatar_path
	data['register_date'] = user.register_date
	return data

def jsonAuthcode(authcode):
	data = {}
	data['phone_number'] = authcode.phone_number
	data['code'] = authcode.code
	data['send_time'] = authcode.send_time
	return data

def isRegistered(phone_number, phone_country_code):
	try:
		if User.objects.get(phone_number=phone_number, phone_country_code=phone_country_code):
			return True
		return False	
	except:
		return False

def returnData(code, msg, data):
	data = {}
	data['code'] = code
	data['msg'] = msg
	data['data'] = data
	logging.info("Return data: code=%s, msg=%s, data=%s.", code, msg, data)
	return data









