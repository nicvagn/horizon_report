from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.

reports = [{
    "name": "report1",
    "url": "report url"
}, {
    "name": "report2",
    "url": "report2 url"
}]


def index(request):
    return render(request, "home/index.html", {"reports": reports})


def new_report(request):
    return HttpResponseRedirect(reverse("report-new"))


def view_report(request, report):
    return HttpResponseRedirect(reverse("report-view"), {"report": report})
