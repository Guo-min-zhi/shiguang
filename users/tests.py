#!/usr/local/bin/python
#-*- coding:utf-8 -*-
from django.test import TestCase
from functions import *

# Create your tests here.

if __name__ == '__main__':
	phone = '13146174160'
	code = '12212'
	s = sendAuthcode(phone, code)
	print s