from django.shortcuts import render
from django.http import HttpResponse

# from .core import index
# import core.index

def index(req):
  return HttpResponse("Hello, world. You're at the polls index.")
