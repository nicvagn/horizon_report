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

from cfc_report.models.player import Player
from cfc_report.utils import cfc_api_utils
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
        player_cfc_id = player_data["player_cfc_id"]

        # get player info from cfc api
        p_info = cfc_api_utils.get_player_info(player_cfc_id)

        logger.debug("Received player info: %s", p_info)

        if not p_info["name_first"]:
            return render(request, NEW_PLAYER_TEMPLATE, {
                "error": f"Could not find player with CFC ID: {player_cfc_id}"
            })

        try:
            player = Player.create(p_info)
            player.save()
            logger.info("Successfully created (and saved) player from CFC ID: %s. Player info %s", player, p_info)
        except ValueError as exc:
            logger.error("Failed to create player with CFC ID '%s' -- %s",
                         player_cfc_id, exc)
            return render(request, NEW_PLAYER_TEMPLATE, {
                "error": str(exc)
            })

        logger.info("Successfully added player: %s", player)
        return redirect('index')
    except (ValueError, UnboundLocalError) as exc:
        logger.error("Failed to add player - %s", exc)
        return render(request, NEW_PLAYER_TEMPLATE, {
            "method": request.method,
            "error": "No player returned from CFC API."
        })


'''
def add_player_database(request: HttpRequest, cfc_id: str = None) -> HttpResponse:
    """View to add a player to the tournament player's database using CFC ID.

    This view retrieves player information from the CFC API using the provided
    CFC ID and creates a new player entry in the database.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object from Django.
    cfc_id : str
        The Chess Federation of Canada (CFC) ID of the player to be added.

    Returns
    -------
    HttpResponse
        A redirect response to the tournament players page on success,
        or a rendered error template on failure.

    Notes
    -----
    Side effects:
        - Queries the CFC API for player information
        - Creates a new player in the database via `create_player`
        - Logs debug and error information
    """
    logger.debug("Processing add_player_database for request method: %s",
                 request.method)

    # only process the request if it is a POST, else show the 'add player' form
    if request.method != "POST":
        return render(request, NEW_PLAYER_TEMPLATE)

    # if the cfc id is not included in the url, get it form the form
    if not cfc_id:
        cfc_id = request.POST.get("cfc_id")

    p_info = cfc_api_utils.get_player_info(cfc_id)

    logger.debug("Received player info: %s", p_info)

    if not p_info["player"]["name_first"]:
        return render(request, NEW_PLAYER_TEMPLATE, {
            "error": f"Could not find player with CFC ID: {cfc_id}"
        })

    try:
        player = create_player(p_info)
        logger.info("Successfully created player from CFC ID: %s", player)
    except ValueError as exc:
        logger.error("Failed to create player with CFC ID '%s': %s",
                     cfc_id, exc)
        return render(request, NEW_PLAYER_TEMPLATE, {
            "error": str(exc)
        })

    return redirect('index')
    '''
