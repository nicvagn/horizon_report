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
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.vary import vary_on_headers

from .. import logger
from ..forms import MatchForm, RoundForm, TournamentInfoForm
from ..services import database as db
from ..services import session


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
        logger.debug("Report.initial entered with request: %s", request)
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
    @vary_on_headers("HX-Request")
    def players(cls, request):
        """set information about what players in a tournament"""

        # check if the request is an htmx request
        if request.htmx:
            logger.debug("htmx request with value: %s", request)

        if request.method == "POST":
            player_info = request.POST
            logger.debug("POST request with value: %s", player_info)
            # save tournament info to session
            logger.debug("TournamentInfoForm made from POST: %s",
                         player_info)
            return render(request, "cfc_report/create/rounds.html")

        db_players = db.get_players()
        tournament_players = session.get_players()
        context = {
            "title": "choose tournament players",
            "action_url": reverse("create-report-players"),
            "players": db_players,
            "tournament_players": tournament_players,
            "include_nav_bar": False,
        }
        return render(request, "cfc_report/create/toggle-players.html", context)

    @classmethod
    def rounds(cls, request):
        """Enter information about rounds
        Arguments
        ---------
        request : HttpRequest from the view
        """
        logger.debug("create_report entered with request: %s", request)
        # if is the form being submitted
        if request.method == "POST":
            round_info = request.POST
            logger.debug("POST request with value: %s", round_info)
            # save tournament info to session
            session.set_tournament_info(round_info)

            # redirect to view to finalize the report
            return redirect("create-report-finalize")

        # form = RoundsForm() TESTING game forum
        form = MatchForm()

        context = {
            "title": "Enter round information",
            "action_url": reverse("create-report-rounds"),
            "submit_btn_txt": "Finalize",
            "form": form
        }
        return render(request, "cfc_report/create/rounds.html", context)

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

    @classmethod
    def toggle_player_session(cls, request, cfc_id: "CfcId" = None):
        """Pick a player if it is not in the session, add it.
        If it is in the session, remove it.

        Side-effects
        ------------
        changes the CfcId's in session.

        Parameters
        ----------
        request : django request
            Dijango request
        cfc_id : "CfcId"
            The Player to add/removed to the session
        """

        logger.debug(
            "toggle_player_session entered with request: %s and  player CfcId: %s",
            request,
            cfc_id)
        assert cfc_id

        # if cfc id in session, remove it
        if cfc_id in session.get_player_ids():
            session.remove_player_by_id(cfc_id)
        else:
            # if not in session add to it
            session.add_player_by_id(cfc_id)

        db_players = db.get_players()
        tournament_players = session.get_players()

        context = {
            "players": db_players,
            "tournament_players": tournament_players,
            "include_nav_bar": False
        }

        return render(request, "cfc_report/create/player-form.html", context)


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
