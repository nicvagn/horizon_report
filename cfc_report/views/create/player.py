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

from django.shortcuts import render
from django.urls import reverse

from cfc_report.models import Player
from cfc_report import logger
from cfc_report.services import database as db_services
from cfc_report.services import player as player_services
from cfc_report.services import session


def set_in_report(request):
    """set information about what players in a tournament"""

    # if the request is a POST it is the form submission not initial get
    # needed if no new players are choosen and you want to confirm players
    if request.method == "POST":
        player_info = request.POST
        logger.debug("TournamentInfoForm made from POST: %s", player_info)
        return render(request, "cfc_report/create/round.html", player_info)

    db_players = db_services.get_players()
    tournament_players = session.player.get_players()
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


def new_player(request):
    """view to add player to tournament players database

    Side-effects
    ------------
    modify's the datebase via services.db.add_player
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
