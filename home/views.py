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

from .core.nasgram import exec_diagram
def snmp(req):
  argvs = ['-r', 'demo.snmplabs.com', '-o', 'network.svg']
  data=exec_diagram(argvs)
  print(data)
  return JsonResponse(data, safe=False)
# python3 natlas-cli.py diagram -r demo.snmplabs.com -o .\network.svg