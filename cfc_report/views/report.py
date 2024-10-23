"""views for managing a cfc report"""
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
import logging
from django.shortcuts import render
from django.http.response import HttpResponse
from ..constants import LOGGER_NAME
from ..forms import TournamentForm
from ..services import database as db, session
# set up logger
# get the logger for cfc_report module. Should be set up.
logger = logging.getLogger(LOGGER_NAME)


def create(request):
    """show view to create a report for the cfc"""
    logger.debug("create_report entered with request: %s", request)
    # if is the form being submitted
    if request.method == "POST":
        query_dict = request.POST
        logger.debug("POST request with value: %s", query_dict)

        tournament_info = TournamentForm(request.POST)

        if tournament_info.is_valid():
            return HttpResponse("Good job")

        # TODO: create tournament report
        return HttpResponse("Bad job")

    form = TournamentForm()
    players = db.get_players()
    tournament_p = session.get_session_players()

    context = {"database_players": players,
               "tournament_players": tournament_p,
               "form": form}
    return render(request, "cfc_report/create/ctr-info.html", context)


def view(request):
    """display a CFC report"""

    logger.debug("view_report entered with request: %s", request)

    player_list = db.get_players()
    num_players = player_list.count()
    report = {
        "title": "The Masters",
        "province": "SK",
        "time_format": "blitz",
        "TD_cfc": TD.cfc_id,
        "TO_cfc": TO.cfc_id,
        "tournament_date": "06/06/87",
        "players": player_list,
        "num_players": num_players,
    }
    return render(request, "cfc_report/show/index.html", report)
