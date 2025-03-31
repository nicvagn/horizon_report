"""module for creating a cfc report"""

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
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from cfc_report import logger
from cfc_report.forms import TournamentInfoForm
from cfc_report.models import (CTR, Match, Player, Round, Tournament,
                               TournamentDirector, TournamentOrganizer)
from cfc_report.models.fields import CfcIdField
from cfc_report.services import database as db
from cfc_report.services import session
from cfc_report.services.ctr_builder import CTR_builder


def initial(request):
    """Get initial tournament info
    Arguments
    ---------
    request : HttpRequest from the view
    """
    logger.debug("Report.initial entered with request: %s", request)
    # if is the form being submitted
    if request.method == "POST":
        # get the tournament info from the form submit
        tournament_info = request.POST
        breakpoint()
        return redirect("create-report-players")

    form = TournamentInfoForm()

    context = {
        "title": "Enter tournament information",
        "action_url": reverse("create-report-info"),
        "submit_btn_txt": "Pick Players",
        "form": form,
    }
    return render(request, "cfc_report/base/base-form.html", context)
