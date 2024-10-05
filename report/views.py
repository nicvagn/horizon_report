from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


#TODO: these views do not work.
def report_view(request, report):
    """display a CFC report"""
    return render(request, "report/show_report.html", report)


def create_report(request):
    """create a report for the cfc"""
    return render(request, "report/create_report.html")
