from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.create_report, name='report-new'),
    path("<report>", views.report_view, name='report-view')
]
