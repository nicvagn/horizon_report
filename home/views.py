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
