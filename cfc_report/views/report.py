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
from django.urls import reverse
from django.shortcuts import render
from django.http.response import HttpResponse
from ..constants import LOGGER_NAME
from ..forms import TournamentForm
from ..services import database as db, session
# set up logger
# get the logger for cfc_report module. Should be set up.
logger = logging.getLogger(LOGGER_NAME)


class create:
    @classmethod
    def initial(cls, request):
        """Get initial tournament info"""
        logger.debug("create_report entered with request: %s", request)
        # if is the form being submitted
        if request.method == "POST":
            logger.debug("POST request with value: %s", request.POST)

            tournament_info = TournamentForm(request.POST)
            logger.debug("TournamentForm made: %s", tournament_info)
            if tournament_info.is_valid():
                return HttpResponse("Good job! Valid form")

            # TODO: create tournament report
            return HttpResponse("Bad job. Invalid")

        form = TournamentForm()

        context = {"title": "Enter tornament information",
                   "action_url": reverse("create-report"),
                   "form": form}
        return render(request, "cfc_report/base/base-form.html", context)

    @classmethod
    def players(cls, request):
        """set information about what players in a tournament"""

        players = db.get_players()
        tournament_p = session.get_session_players()
        context = {}
        return render(request, "cfc_report/create/pick-players.html", context)


def view(request):
    """display a CFC report"""

    logger.debug("view_report entered with request: %s", request)

    player_list = db.get_players()
    num_players = player_list.count()
    report = {
        "title": "The Masters",
        "province": "SK",
        "time_format": "blitz",
        "TD_cfc": "111111",  # FIXME
        "TO_cfc": "222222",
        "tournament_date": "06/06/87",
        "players": player_list,
        "num_players": num_players,
    }
    return render(request, "cfc_report/show/index.html", report)
