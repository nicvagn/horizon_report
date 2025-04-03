"""views for cfc_report players"""
from django.http import HttpRequest, HttpResponse
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
from django.shortcuts import render

from .. import logger
from ..models.person_with_cfc_id_models import Player


def _create_player(name: str, cfc_id: int) -> Player:
    """
    Helper function to create a player and save it to the database.

    Parameters
    ----------
    name : str
        The name of the player to be created.
    cfc_id : int
        The CFC ID of the player to be created.

    Returns
    -------
    Player
        The created Player instance.
    """
    player = Player.create(name, cfc_id)
    logger.debug("Created Player: %s with CFC ID: %s", player.name, player.cfc_id)
    player.save()
    logger.info("Player %s saved to database.", player)
    return player


def add_player(request: HttpRequest) -> HttpResponse:
    """
    View to add a player to the tournament players database.

    Notes
    -----
    Side effects:
        - Modifies the database via `_create_player`.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object.

    Returns
    -------
    HttpResponse
        The rendered response for the player add page.
    """
    logger.debug("add_player view invoked with request: %s", request)

    if request.method == "POST":
        form_data = request.POST
        logger.debug("Received POST data: %s", form_data)

        # Ensure necessary data exists in form submission
        player_name = form_data.get("player_name")
        player_cfc_id = form_data.get("player_cfc_id")

        if not player_name or not player_cfc_id:
            logger.warning("Missing player_name or player_cfc_id in POST data.")
            return render(request, "cfc_report/create/player.html", {
                "method": request.method,
                "error": "Player Name and CFC ID are required."
            })

        try:
            player = _create_player(player_name, int(player_cfc_id))
            logger.info("Player %s successfully added.", player)
        except ValueError as exc:
            logger.error("Invalid CFC ID: %s. Exception: %s", player_cfc_id, exc)
            return render(request, "cfc_report/create/player.html", {
                "method": request.method,
                "error": "Invalid CFC ID format. Please use a 6 char number."
            })

    return render(request, "cfc_report/create/player.html", {"method": request.method})
