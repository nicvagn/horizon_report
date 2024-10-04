from django.shortcuts import render
from django.urls import reverse

reports = [{
    "name": "report1",
    "url": "report url"
}, {
    "name": "report2 url",
    "url": "report2 url"
}]


def index(request):
    return render(request, "report/build_report.html", {
        "reports": reports,
        "make_report_url": reverse("report-new")
    })
