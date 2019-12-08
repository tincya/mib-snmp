from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets

# from .core import index
# import core.index

def index(req):
  return HttpResponse("Hello world!")

def home(req):
  ctx = {'data':'Hello, this is my baseline!'}
  return render(req, 'home/home.html', ctx)

def profile(req):
  data = {
    'name': 'Vitor',
    'location': 'Finland',
    'is_active': True,
    'count': 28
  }
  return JsonResponse(data)

# python3 natlas-cli.py diagram -r demo.snmplabs.com -o .\network.svg