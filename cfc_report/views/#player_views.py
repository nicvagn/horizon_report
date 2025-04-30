"""views for cfc_report players"""
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
from django.shortcuts import render, reverse, redirect

from .. import logger
from ..models.tournament import Roster, Tournament
from ..utils.session_utils import get_session_players, create_player

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


def set_tournament_players(request: HttpRequest) -> HttpResponse:
    """set information about what players in the tournament in session

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
        The rendered response for the player add page.
    """

    db_players = Player.objects.all()
    tournament_players = get_session_players(request)
    # if the request is POST it is the form submission not initial get
    # needed if no new players are chosen, and you want to confirm players
    if request.method == "POST":
        breakpoint()
        t_id = request.session["tournament_id"]
        tournament = Tournament.objects.get(pk=t_id)
        roster, created = Roster.objects.get_or_create(tournament_id=t_id)
        roster.save()
        roster.players.set(tournament_players)

        logger.info("Roster: %s created for tournament: %s", roster, tournament)
        return redirect("report-create-round")

    context = {
        "title": "choose tournament players",
        "action_url": reverse("report-tournament-players"),
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


def toggle_player_session_view(request: HttpRequest,
                               cfc_id=None) -> HttpResponse:
    """If a player with the cfc_id is in the session, remove it. Else add it

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
