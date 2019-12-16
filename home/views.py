from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def pcap(request):
  if request.method == 'POST' or request.method == 'PUT':
    for file in request.FILES:
      with open(settings.BASE_DIR + '/upload/' + request.FILES[file].name, 'wb+') as destination:
        for chunk in request.FILES[file].chunks():
          destination.write(chunk)
    return render(request, 'home/upload.html')
  return render(request, 'home/upload.html', {'errors':'GET!'})

  # if request.method == 'POST' or request.method == 'PUT':
  #   if request.method == 'POST':
  #     form = UploadFileForm(request.POST, request.FILES)
  #   else:
  #     form = UploadFileForm(request.PUT, request.FILES)
  #   if form.is_valid():
  #     with open(settings.BASE_DIR+'/upload/'+request.FILES['file2up'].name, 'wb+') as destination:
  #       for chunk in request.FILES['file2up'].chunks():
  #         destination.write(chunk)
  #     return HttpResponse("OK!")
  #   return HttpResponse("FAIL!")
  # else:
  #   form = UploadFileForm()
  #   return render(request, 'home/upload.html', {'form': form})


class LoginForm(forms.Form):
  user_name = forms.CharField(max_length=100, label='user_name', required=True)
  password = forms.CharField(widget=forms.PasswordInput, max_length=100, label='password', required=True)
  remember = forms.BooleanField(label='remember', required=False)

class RegisterForm(LoginForm):
  email = forms.EmailField(max_length=100, label='email')
  re_password = forms.CharField(widget=forms.PasswordInput, max_length=100, label='re_password', required=True)

def register(req):
  if req.method == 'POST':
    uf = RegisterForm(req.POST)
    if uf.is_valid() and uf.cleaned_data['password']==uf.cleaned_data['re_password']:
      user_name = uf.cleaned_data['user_name']
      email = uf.cleaned_data['email']
      password = uf.cleaned_data['password']
      try:
        user = User.objects.create_user(user_name, email, password)
      except:
        return render(req, 'home/register.html', {'form':uf, 'errors':'Register Fail!'})
      return render(req, 'home/register.html', {'user':user, 'success':True})
  else:
    uf = RegisterForm()
  return render(req, 'home/register.html', {'form':uf})
def login(req):
  if req.method == 'POST':
    uf = LoginForm(req.POST)
    if uf.is_valid():
      user_name = uf.cleaned_data['user_name']
      password = uf.cleaned_data['password']
      try:
        user = authenticate(username=user_name, password=password)
        if user is not None:
          return render(req, 'home/login.html', {'user': user, 'success': True})
      except:
        return render(req, 'home/login.html', {'form':uf, 'errors':'Login Fail!'})
      return render(req, 'home/login.html', {'form': uf, 'errors': 'Login Fail!'})
  else:
    uf = LoginForm()
  return render(req, 'home/login.html', {'form':uf})
