from django.shortcuts import render
from django.urls import reverse

# Create your views here.

reports = ["report1", "report2"]


def index(request):
    return render(request, "home/index.html", {"reports": reports})
