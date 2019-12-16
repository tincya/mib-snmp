from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', views.profile, name='home'),
    path('snmp/', views.snmp, name='snmp'),
    path('test.pcap', views.pcap, name='pcap'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]
