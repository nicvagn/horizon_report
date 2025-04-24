"""Views to manage Players in sessions"""
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

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from cfc_report import logger

from cfc_report.models import Player

# constant for session players key
SESSION_PLAYERS_KEY = "players"
# file constant
NEW_PLAYER_TEMPLATE = "cfc_report/create/add-player-system-form.html"
TOURNAMENT_PLAYER_FORM = "cfc_report/create/player-form.html"
def toggle_cfc_id_session_view(request: HttpRequest,
                               cfc_id=None) -> HttpResponse:
    """

    Notes
    -----
    - This uses htmx under the hood to replace on the DOM
    Side effects:
        - changes Players in session.

    Parameters
    ----------
    request : HttpRequest
        http request from the view, used to get the session
    cfc_id : "CfcId"
        The cfc id of the Player to add/removed to the session
    """

    logger.debug(
        "toggle_player_session entered with request: \
        %s and  player CfcId: %s",
        request,
        cfc_id,
    )
    assert cfc_id

    # get the session players from request
    session_players = get_session_players(request)

    for player in session_players:
        logger.debug(
            "player: %s", player,
        )
        if player.cfc_id == int(cfc_id):
            session_players.remove(player)
            logger.info("Removed player with CFC ID: %s from session.", cfc_id)
            break
    else:
        # If not present, add player to session
        added_player: Player = Player.objects.get(cfc_id=int(cfc_id))
        session_players.append(added_player)
        logger.info("Added player with CFC ID: %s to session.", cfc_id)

    # Serialize and set players in session to changed value
    request.session["players"] = session_players

    db_players = Player.objects.all()

    context = {
        "players": db_players,
        "tournament_players": session_players,
        "include_nav_bar": False,
    }

    return render(request, TOURNAMENT_PLAYER_FORM, context)
