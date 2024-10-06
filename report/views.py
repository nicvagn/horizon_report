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

from django.shortcuts import render, reverse


def view_report(request):
    """display a CFC report"""
    context = {"players": ["11111", "222222", "333333", "44444"]}
    return render(request, "report/view_report.html", context)


def create_report(request):
    """create a report for the cfc"""
    context = {"players": ["11111", "222222", "333333", "44444"]}
    return render(request, "report/create_report.html", context)
