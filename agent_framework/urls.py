"""
URL configuration for agent_framework project.
"""
from django.contrib import admin
from django.urls import path
from framework import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('features/', views.features, name='features'),
    path('documentation/', views.documentation, name='documentation'),
]

