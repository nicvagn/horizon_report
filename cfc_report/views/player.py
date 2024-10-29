"""views for cfc_report players"""
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

from django.shortcuts import redirect, render

from ..constants import LOGGER_NAME
from ..models import Player, TournamentDirector, TournamentOrganizer
from ..services import database as db_services
from ..services import player as player_services
from ..services import session as session_services

# set up logger
# get the logger for cfc_report module. Should be set up.
logger = logging.getLogger(LOGGER_NAME)


def pick_player(request, cfc_id=None) -> None:
    """Pick a player if it is not in the session, add it. 
    If it is in the session, remove it. Update the page

    Parameters
    ----------
    request : django request
        Dijango request
    player : Player
        The Player to add/removed to the session
    """

    logger.debug("Player with cfc_id %s picked", cfc_id)
    if cfc_id:
        session_services.add_player_by_id(cfc_id)

    players = db_services.get_players()

    context = {
        "players": players,
        "tournament_players": session_services.get_players()
    }
    # TODO: visually update players in tournament using
    #   { % for player in tournament_players % }
    # return (request, "cfc_report/create/index.html", context)
    return redirect("create-report-players")


def add_player(request):
    """view to add player to tournament players database"""
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
    return render(request, "cfc_report/add_player/index.html",
                  {"method": request.method})
