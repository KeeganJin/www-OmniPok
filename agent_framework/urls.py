"""
URL configuration for agent_framework project.
"""
from django.contrib import admin
from django.urls import path
from framework import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('omnipok-agent/', views.omnipok_agent, name='omnipok_agent'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

