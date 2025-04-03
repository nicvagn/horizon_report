"""view for managing players in cfc report"""

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

from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse

from cfc_report import logger
from cfc_report.models import Player
from cfc_report.services import database as db_services
from cfc_report.services import player as player_services
from cfc_report.services import session_services


def set_in_report(request) -> HttpRequest:
    """set what players in the report. This is the entrypoint fror that.

    Purpose
    -------
    display the template thaet lets you pick the players in the report
    """

    # if the request is a POST it is the form submission not initial get
    # needed if no new players are choosen and you want to confirm players
    if request.method == "POST":
        player_info = request.POST
        logger.debug("TournamentInfoForm made from POST: %s", player_info)
        return render(request, "cfc_report/create/round.html", player_info)

    db_players = db_services.get_players()
    tournament_players = session_services.player.get_players()
    context = {
        "title": "choose tournament players",
        "action_url": reverse("create-report-players"),
        "players": db_players,
        "tournament_players": tournament_players,
        "include_nav_bar": False,
    }

    logger.debug(
        "db_players: %s \n tournament_players: %s \n context: %s",
        db_players,
        tournament_players,
        context,
    )
    return render(request, "cfc_report/create/toggle-players.html", context)


def toggle_player_session(request, cfc_id=None):
    """Pick a player if it is not in the session_services, add it.
    If it is in the session_services, remove it. This uses htmx under the hood
    to replace on the DOM
    Notes
    -----
    Side effects:
        changes the CfcId's in session_services.

    Parameters
    ----------
    request : django request
    cfc_id : "CfcId"
        The Player to add/removed to the session_services
    """

    logger.debug(
        "toggle_player_session entered with request: \
        %s and  player CfcId: %s",
        request,
        cfc_id,
    )
    assert cfc_id

    # if cfc id in session_services, remove it
    if cfc_id in session_services.player.get_player_ids():
        session_services.player.remove_player_by_id(cfc_id)
    else:
        # if not in session_services add to it
        session_services.player.add_player_by_id(cfc_id)

    db_players = db_services.get_players()
    tournament_players = session_services.player.get_players()

    context = {
        "players": db_players,
        "tournament_players": tournament_players,
        "include_nav_bar": False,
    }

    return render(request, "cfc_report/create/player-form.html", context)


def new_player(request) -> HttpRequest:
    """view to add player to tournament players database
    Notes
    -----

    Side effects:
        modifies the database via services.db.add_player
    """
    logger.debug("add_player entered with request %s", request)
    # if is the form being submitted
    if request.method == "POST":
        query_dict = request.POST
        logger.debug("POST request with value: %s", query_dict)

        player: Player = player_services.create_player(
            query_dict["player_name"], query_dict["player_cfc_id"])
        logger.debug("Player %s made.", player)
        # add player to db
        db_services.add_player(player)
        logger.debug("Made Player added to database")

    # render the requested page.
    return render(request, "cfc_report/create/player.html",
                  {"method": request.method})
