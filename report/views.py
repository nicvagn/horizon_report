from django.shortcuts import render, reverse


#TODO: these views do not work.
def view_report(request):
    """display a CFC report"""
    context = {"players": ["11111", "222222", "333333", "44444"]}
    return render(request, "report/view_report.html", context)


def create_report(request):
    """create a report for the cfc"""
    context = {"players": ["11111", "222222", "333333", "44444"]}
    return render(request, "report/create_report.html", context)
