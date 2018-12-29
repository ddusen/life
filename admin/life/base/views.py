import json

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from uuid import uuid4

from life.base.models import *


def index(request):
    return render(request, 'index.html')


def data(request):
    return render(request, 'data.html')


def chart(request):
    return render(request, 'chart.html')


def analytics(request):
    return render(request, 'analytics.html')


def api_index(request):
    data = {}
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def api_data(request):
    data = {}
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def api_chart(request):
    data = {}
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def api_analytics(request):
    data = {}
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
