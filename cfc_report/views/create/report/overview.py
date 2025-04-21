"""general overwiew view for creating a Report for a CFC Rated tournament."""
# Copyright (C) 2024 Nicolas Vaagen
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

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from cfc_report import logger
from cfc_report.models import Tournament, Round
from cfc_report.types import TournamentInfo


class CreateReportView(View):
    """general Report overview for report in construction."""
    # TODO: a general overview

    def get(self, request, *args, **kwargs):
        t_info = request.session["tournament_info"]
        context = {"tournament_name": t_info["name"], "rounds": t_info["rounds"]}
        return render(request, "cfc_report/create/report.html", context)
