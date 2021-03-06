from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

# from .core import index
# import core.index
import os
import json
import numpy as np
from django.utils import timezone
from home.models import PCAP
from home.utils.pcap_analytics import toJSON
from shutil import copyfile

UPLOAD_DIR = './upload'
UPLOAD_TMP_DIR= './upload_tmp'

def index(req):
  ctx = {}
  ctx['user_data'] = auth_ctx(req)
  return render(req, 'home/home.html', ctx)


def home(req):
  ctx = {'data': 'Hello, this is my baseline!'}
  ctx['user_data'] = auth_ctx(req)
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
  data = exec_diagram(argvs)
  print(data)
  return JsonResponse(data, safe=False)


# python3 natlas-cli.py diagram -r demo.snmplabs.com -o .\network.svg

@csrf_exempt
def pcap(req):
  ctx = {}
  ctx['user_data'] = auth_ctx(req)
  if ctx['user_data']:
    syncdb()
    if req.method == 'POST':
      if 'delete_file' in req.POST and ctx['user_data']['is_superuser']:
        try:
          fid = int(req.POST['delete_file'])
          pcf = PCAP.objects.get(pk=fid)
          file_name = pcf.file_name
          pcf.delete()
          os.remove(UPLOAD_DIR + '/' + file_name)
          ctx['message'] = 'Delete "' + req.POST['delete_file'] + '" Success!'
        except:
          ctx['message'] = 'Delete error!!!'
      elif 'syncdb' in req.POST:
        syncdb()
      elif req.FILES:
        for file in req.FILES:
          with open(settings.BASE_DIR + '/upload/' + req.FILES[file].name, 'wb+') as destination:
            if req.FILES[file].name.endswith('.pcap'):
              PCAP(file_name=req.FILES[file].name, pub_date=timezone.now()).save()
            for chunk in req.FILES[file].chunks():
              destination.write(chunk)
          ctx['message'] = 'Upload "' + req.FILES[file].name + '" Success!'
  else:
    return redirect('user_login')
  ctx['list_files'] = PCAP.objects.all()
  return render(req, 'home/upload-base.html', ctx)

def pcap_data(req, pk):
  try:
    pcapfile = PCAP.objects.get(pk=pk)
    return HttpResponse(pcapfile.json_data)
  except (KeyError, PCAP.DoesNotExist):
    pass
  return HttpResponse("{'error':'???'}")

def pcap_all(req):
  ctx = {}
  ctx['user_data'] = auth_ctx(req)
  if not ctx['user_data']:
    return redirect('user_login')
  pcapfile={
    'dnsCount': {},
    'timeSeries': {},
    'portTraffd': {},
    'portTraffs': {},
    'ipCountd': {},
    'ipCounts': {}
  }
  pcapfiles = PCAP.objects.all()
  for pcc in pcapfiles:
    jdt = json.loads(pcc.json_data)
    for dcs in jdt:
      for keyv in jdt[dcs]:
        if keyv in pcapfile[dcs]:
          if type(jdt[dcs][keyv])==type({}) and 'count' in pcapfile[dcs][keyv]:
            pcapfile[dcs][keyv]['count'] += jdt[dcs][keyv]['count']
            pcapfile[dcs][keyv]['ip'] += jdt[dcs][keyv]['ip']
          else:
            pcapfile[dcs][keyv]+=jdt[dcs][keyv]
        else:
          if type(jdt[dcs][keyv])==type({}) and 'count' in jdt[dcs][keyv]:
            pcapfile[dcs][keyv]={'count':jdt[dcs][keyv]['count'],'ip':jdt[dcs][keyv]['ip']}
          else:
            pcapfile[dcs][keyv] = jdt[dcs][keyv]
  ctx['pcapfile']={
    'id':0,
    'file_name':'All',
    'json_data':pcapfile
  }
  return render(req, 'home/allfile-info.html', ctx)

def pcap_info(req, pk):
  ctx = {}
  ctx['user_data'] = auth_ctx(req)
  if not ctx['user_data']:
    return redirect('user_login')
  pcapfile={}
  try:
    pcapfile = PCAP.objects.get(pk=pk)
  except (KeyError, PCAP.DoesNotExist):
    pass
  ctx['pcapfile']=pcapfile
  return render(req, 'home/file-info.html', ctx)

class LoginForm(forms.Form):
  user_name = forms.CharField(max_length=100, label='user_name', required=True)
  password = forms.CharField(widget=forms.PasswordInput, max_length=100, label='password', required=True)
  remember = forms.BooleanField(label='remember', required=False)


class RegisterForm(LoginForm):
  email = forms.EmailField(max_length=100, label='email')
  re_password = forms.CharField(widget=forms.PasswordInput, max_length=100, label='re_password', required=True)


def user_register(req):
  if req.method == 'POST':
    uf = RegisterForm(req.POST)
    if uf.is_valid() and uf.cleaned_data['password'] == uf.cleaned_data['re_password']:
      user_name = uf.cleaned_data['user_name']
      email = uf.cleaned_data['email']
      password = uf.cleaned_data['password']
      try:
        user = User.objects.create_user(user_name, email, password)
      except:
        return render(req, 'home/register.html', {'form': uf, 'errors': 'Register Fail!'})
      return redirect('user_login')
  else:
    uf = RegisterForm()
  return render(req, 'home/register.html', {'form': uf})


def user_login(req):
  if req.user.is_authenticated:
    return redirect('index')
  if req.method == 'POST':
    uf = LoginForm(req.POST)
    if uf.is_valid():
      user_name = uf.cleaned_data['user_name']
      password = uf.cleaned_data['password']
      try:
        user = authenticate(username=user_name, password=password)
        if user is not None:
          login(req, user)
          return redirect('index')
      except:
        return render(req, 'home/login.html', {'form': uf, 'errors': 'Login Fail!'})
      return render(req, 'home/login.html', {'form': uf, 'errors': 'Not Valid!'})
  else:
    uf = LoginForm()
  return render(req, 'home/login.html', {'form': uf})


def user_logout(req):
  logout(req)
  return redirect('user_login')


def allusers(req):
  ctx = {}
  ctx['user_data'] = auth_ctx(req)
  if ctx['user_data']:
    if req.method == 'POST' and 'delete_user' in req.POST and ctx['user_data']['is_superuser']:
      duser = User.objects.get(pk=req.POST['delete_user'])
      if not duser.is_superuser:
        ctx['message'] = 'Delete user "' + duser.username + '" success!'
        duser.delete()
      else:
        ctx['message'] = 'Delete user "' + duser.username + '" error!'
    users = User.objects.filter(is_superuser=False)
    ctx['users'] = users
  else:
    return redirect('user_login')
  return render(req, 'home/all-users.html', ctx)


def auth_ctx(req):
  if req.user.is_authenticated:
    return {
      'username': req.user.username,
      'email': req.user.email,
      'is_superuser': req.user.is_superuser,
    }
  return None


def syncdb():
  for r, d, f in os.walk(UPLOAD_DIR):
    break
  for pfile in f:
    if pfile.endswith('.pcap'):
      try:
        pc = PCAP.objects.get(file_name=pfile)
      except (KeyError, PCAP.DoesNotExist):
        pc=None
      pjs = toJSON(file_name=UPLOAD_DIR + '/' + pfile, limit=-1)
      if not pc:
        pc = PCAP(file_name=pfile, pub_date=timezone.now(), json_data=pjs)
      else:
        pc.json_data=pjs
      pc.save()
      try:
        copyfile(UPLOAD_DIR + '/' + pfile, UPLOAD_TMP_DIR + '/' + pfile)
        os.remove(UPLOAD_DIR + '/' + pfile)
      except:
        return 0

  return 1
