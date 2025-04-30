"""views for adding models to the database"""
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

from cfc_report.utils.database_utils import create_player
from . import logger

# constant for session players key
SESSION_PLAYERS_KEY = "players"
# file constant
NEW_PLAYER_TEMPLATE = "cfc_report/create/add-player-system-form.html"
TOURNAMENT_PLAYER_FORM = "cfc_report/create/player-form.html"


def add_player_database(request: HttpRequest) -> HttpResponse:
    """View to add a player to the tournament player's database.

    Notes
    -----
    Side effects:
    - Modifies the database via `create_player`.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object.

    Returns
    -------
    HttpResponse
        The rendered response for the player add page.
    """
    logger.debug("Processing add_player_database for request method: %s",
                 request.method)

    if request.method != "POST":
        return render(request, NEW_PLAYER_TEMPLATE)

    player_data = request.POST
    logger.debug("Received POST data: %s", player_data)

    try:
        player_name = player_data["player_name"]
        player_cfc_id = int(player_data["player_cfc_id"])
        player = create_player(player_name, player_cfc_id)
        logger.info("Successfully added player: %s", player)
    except (ValueError, UnboundLocalError) as exc:
        logger.error("Failed to add player with CFC ID '%s': %s",
                     player_cfc_id, exc)
        return render(request, NEW_PLAYER_TEMPLATE, {
            "method": request.method,
            "error": "Invalid CFC ID format. Please use a 6-digit number."
        })

    return redirect("index")
