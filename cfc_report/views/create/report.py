"""view for creating a cfc report"""

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
from django.shortcuts import redirect, render
from django.urls import reverse

from cfc_report import logger
from cfc_report.forms import TournamentInfoForm
from cfc_report.services import session
from cfc_report.services.ctr_builder import CTR_builder


def initial_form(request) -> HttpResponse:
    """Prepaire and present initial tournament info form. Then
    handle gettind the data from the form

    Arguments
    ---------
    request : HttpRequest sent to the view
    """
    logger.debug("Report.initial entered with request: %s", request)
    # if is the form being submitted
    if request.method == "POST":
        # get the tournament info from the form submit
        tournament_info = request.POST
        logger.info("request.POST containig tournament_info: %s"
                    % tournament_info)
        # Set session["building_round"]
        session.tournament.set_building_round_number(1)
        # next procede to get the player info
        return redirect("create-report-players")

    form = TournamentInfoForm()

    context = {
        "title": "Enter tournament information",
        "action_url": reverse("create-report-info"),
        "submit_btn_txt": "Pick Players",
        "form": form,
    }
    return render(request, "cfc_report/base/base-form.html", context)


def cfc_report(request) -> HttpResponse:
    """Create report"""

    tournament_info = session.get_tournament_info()
    context = {
        "tournament_name": tournament_info["name"],
        "round_number": session.get_building_round_number(),
        "matches": session.get_matches(),
        "players": session.get_players(),
    }
    return render(request, "cfc_report/create/report.html", context)


def preview_report(request) -> HttpResponse:
    """Preview chess report, see all the players, rounds and games that will be
    in the report

    Arguments
    ---------
    request : HttpRequest
    """

    logger.debug("create.preview_report entered with request: %s", request)
    # get tournament information
    t_info = session.get_tournament_info()

    logger.debug("Tournament Info got: %s", t_info)
    ctr = CTR_builder(t_info, session)
    logger.debug("|CTR| created: %s", ctr)

    context = {
        "tournament_name": session.get_tournament_name(),
        "ctr": str(ctr),
        "tms": "TMS NOT DONE",
    }

    return render(request, "cfc_report/show/preview-report.html", context)


def finalize_report(request) -> HttpResponse:
    """Finalize a chess tournament report

    Arguments
    ---------
    request : HttpRequest
    """
    logger.debug("Create.finalize_report entered with request: %s", request)
    # get tournament information
    t_info = session.get_tournament_info()

    logger.debug("Tournament Info got: %s", t_info)
    ctr = CTR_builder(t_info, session)
    ctr.save()
    logger.debug("|CTR| created and saved: %s", ctr)

    ctr.write_file(t_info)
    context = {"ctr": str(ctr)}

    return render(request, "cfc_report/show/ctr.html", context)
