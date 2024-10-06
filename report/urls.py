from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.create_report, name='report-new'),
    path("view", views.view_report, name='report-view'),
]
