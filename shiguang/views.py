#!/usr/local/bin/python
#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import logging

logger = logging.getLogger('shiguang')

# Create your views here.
def homepage(request):
	return HttpResponse("<h1>Welcome to Shiguang !</h1>")