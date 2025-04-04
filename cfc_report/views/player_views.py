# """views for cfc_report players"""
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
from django.shortcuts import render, reverse

from .. import logger
from ..models.person_with_cfc_id_models import Player


def _get_session_players(request) -> list[Player]:
    """get the players in current session

    Parameters
    ----------
    request : django http request
        Django request

    Notes
    -----
    Uses:
        the current session

    Returns
    -------
    players : list(Player)
        A list of the players in session
    """
    players = request.session["players"]

    return players


def _create_player(name: str, cfc_id: int) -> Player:
    """
    Helper function to create a player and save it to the database.

    Notes
    -----
    Adds player to db

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
    logger.debug("Created Player: %s with CFC ID: %s",
                 player.name, player.cfc_id)
    player.save()
    logger.info("Player %s saved to database.", player)
    return player


def add_player_database(request: HttpRequest) -> HttpResponse:
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
        player_data = request.POST
        logger.debug("Received POST data: %s", player_data)

        # Ensure necessary data exists in form submission
        player_name = player_data.get("player_name")
        player_cfc_id = player_data.get("player_cfc_id")

        if not player_name or not player_cfc_id:
            logger.warning(
                "Missing player_name or player_cfc_id in POST data.")
            return render(request, "cfc_report/create/player.html", {
                "method": request.method,
                "error": "Player Name and CFC ID are required."
            })

        try:
            player = _create_player(player_name, int(player_cfc_id))
            logger.info("Player %s successfully added.", player)
        except ValueError as exc:
            logger.error("Invalid CFC ID: %s. Exception: %s",
                         player_cfc_id, exc)
            return render(request, "cfc_report/create/player.html", {
                "method": request.method,
                "error": "Invalid CFC ID format. Please use a 6 char number."
            })

    return render(request, "cfc_report/create/player.html")


def set_tournament_players(request: HttpRequest) -> HttpResponse:
    """
    set information about what players in a tournament

    Notes
    -----
    Side effects:
        - Modifies the players in the session

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object.

    Returns
    -------
    HttpResponse
        The rendered response from the page.
    """

    db_players = Player.objects.all()
    tournament_players = _get_session_players()
    context = {
        "title": "choose tournament players",
        "action_url": reverse("create-report-players"),
        "players": db_players,
        "tournament_players": tournament_players,
        "include_nav_bar": False,
    }

    # if the request is a POST it is the form submission not initial get
    # needed if no new players are chosen, and you want to confirm players
    if request.method == "POST":
        player_info = request.POST
        logger.debug("TournamentInfoForm made from POST: %s", player_info)
        return render(request, "cfc_report/create/round.html", player_info)

    logger.debug(
        "db_players: %s \n tournament_players: %s \n context: %s",
        db_players,
        tournament_players,
        context,
    )
    return render(request, "cfc_report/create/toggle-players.html", context)


def toggle_player_session(request: HttpRequest, cfc_id=None) -> HttpResponse:
    """
    If a player with the cfc_id is in the session, remove it. If it is not found
     add it

    Notes
    -----
    -This uses htmx under the hood to replace on the DOM
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

    session_players = _get_session_players(request)

    for player in session_players:
        if player.cfc_id == int(cfc_id):
            session_players.remove(player)
            logger.info("Removed player with CFC ID: %s from session.", cfc_id)
            break
    else:
        # If not present, add player to session
        new_player = Player.objects.get(cfc_id=int(cfc_id))
        session_players.append(new_player)
        logger.info("Added player with CFC ID: %s to session.", cfc_id)

    # set players in session to changed value
    request.session["players"] = session_players

    db_players = Player.objects.all()

    context = {
        "players": db_players,
        "tournament_players": session_players,
        "include_nav_bar": False,
    }

    return render(request, "cfc_report/create/player-form.html", context)
