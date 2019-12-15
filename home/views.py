from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django import forms
from django.conf import settings
from django.contrib.auth.models import User

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

class UploadFileForm(forms.Form):
    file2up = forms.FileField()

def pcap(request):
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      with open(settings.BASE_DIR+'/upload/'+request.FILES['file2up'].name, 'wb+') as destination:
        for chunk in request.FILES['file2up'].chunks():
          destination.write(chunk)
      return HttpResponse("OK!")
    return HttpResponse("FAIL!")
  else:
    form = UploadFileForm()
    return render(request, 'home/upload.html', {'form': form})


class UserForm(forms.Form):
  user = forms.CharField(max_length=100, required=True)
  email = forms.EmailField(max_length=100)
  password = forms.CharField(max_length=100, required=True)
  re_password = forms.CharField(max_length=100, required=True)

def register(req):
  if req.method == 'POST':
    uf = UserForm(req.POST)
    if uf.is_valid() and uf.cleaned_data['password']==uf.cleaned_data['re_password']:
      user = uf.cleaned_data['user']
      email = uf.cleaned_data['email']
      password = uf.cleaned_data['password']
      User.objects.create_user(user, email, password)
  else:
    uf = UserForm(req.POST)
  return render(req, 'home/register.html', {'form':uf})
def login(req):
  return 0