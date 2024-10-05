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
    return render(request, "home/index.html", {
        "reports": reports,
        "make_report_url": reverse("report-new")
    })


def new_report(request):
    return HttpResponseRedirect(reverse("report-new"))


def tournament_report(request, report):
    return render(request, reverse("report-view"), {"report": report})
