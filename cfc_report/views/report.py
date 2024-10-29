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

from django.forms import CheckboxInput
from django.shortcuts import redirect, render
from django.urls import reverse

from ..constants import LOGGER_NAME
from ..forms import TournamentInfoForm, TournamentPlayerForm
from ..services import database as db
from ..services import session

# set up logger
# get the logger for cfc_report module. Should be set up.
logger = logging.getLogger(LOGGER_NAME)


class Create:
    """Contains view's to create tournament report

    Methods
    -------
    initial(cls, request) : show form to get the initial
    tournament information

    """

    @classmethod
    def initial(cls, request):
        """Get initial tournament info
        Arguments
        ---------
        request : HttpRequest from the view
        """
        logger.debug("create_report entered with request: %s", request)
        # if is the form being submitted
        if request.method == "POST":
            tournament_info = request.POST
            logger.debug("POST request with value: %s", tournament_info)
            # save tournament info to session
            session.set_tournament_info(tournament_info)
            logger.debug("TournamentInfoForm made from POST: %s",
                         tournament_info)

            # redirect to view to choose players
            return redirect("create-report-players")

        form = TournamentInfoForm()

        context = {
            "title": "Enter tournament information",
            "action_url": reverse("create-report-info"),
            "submit_btn_txt": "Pick Players",
            "form": form
        }
        return render(request, "cfc_report/base/base-form.html", context)

    @classmethod
    def players(cls, request):
        """set information about what players in a tournament"""

        db_players = db.get_players()
        tournament_players = session.get_players()
        context = {
            "title": "choose tournament players",
            "action_url": reverse("create-report-players"),
            "players": db_players,
            "tournament_players": tournament_players,
        }
        return render(request, "cfc_report/create/pick-players.html", context)

    @classmethod
    def finalize(cls, request):
        """finalize report"""
        # get the tournament info set in Create.initial()
        tournament_info = session.get_tournament_info()

        # get information on tournament players from the session

        players: list["Player"] = session.get_players()

        context = {
            "name": tournament_info["name"],
            "province": tournament_info["province"],
            "time_format": "blitz",
            "num_players": len(players),
            "players": players,
            "td_cfc": tournament_info["td_cfc"],
            "to_cfc": tournament_info["to_cfc"],
        }
        logger.debug("context: %s", context)
        return render(request, "cfc_report/show/index.html", context)


def view(request):
    """display a CFC report"""

    logger.debug("view_report entered with request: %s", request)

    player_list = db.get_players()
    num_players = player_list.count()
    report = {
        "name": "The Masters",
        "province": "SK",
        "time_format": "blitz",
        "td_cfc": "111111",  # FIXME
        "to_cfc": "222222",
        "date": "06/06/87",
        "players": player_list,
        "num_players": num_players,
    }
    return render(request, "cfc_report/show/index.html", report)
