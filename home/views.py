# horizon_pair
# Copyright (C) 2024  Nicolas Vaagen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
