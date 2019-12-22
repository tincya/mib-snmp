from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', views.profile, name='home'),
    path('snmp/', views.snmp, name='snmp'),
    path('upload/', views.pcap, name='pcap'),
    path('pcap-all/', views.pcap_all, name='pcap-all'),
    path('pcap-data/<int:pk>', views.pcap_data, name='pcap-data'),
    path('pcap-info/<int:pk>', views.pcap_info, name='pcap-info'),
    path('users/', views.allusers, name='users'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
]
