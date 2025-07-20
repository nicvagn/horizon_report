"""view for selecting players in a Report for a CFC Rated tournament."""
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
from django.shortcuts import redirect, render
from django.views import View

from cfc_report.models.player import Player
from cfc_report.utils import cfc_api_utils
from . import logger

# constant for session players key
SESSION_PLAYERS_KEY = "players"
# file constant
NEW_PLAYER_TEMPLATE = "cfc_report/create/add-player-system-form.html"
TOURNAMENT_PLAYER_FORM = "cfc_report/report/players/tournament-players.html"


class TournamentPlayersView(View):
    """view for selecting players in a Report for a CFC Rated tournament."""

    def get(self, request: HttpRequest, error=None) -> HttpResponse:
        """Handle GET request - display available players."""

        player_ids = request.session.get(SESSION_PLAYERS_KEY, default=[])
        players = []
        for cfc_id in player_ids:
            p = get_player_from_cfc_id(cfc_id)

            if not p:
                raise RuntimeError("player no got from cfc_id: %s", cfc_id)

            logger.info("added Player %s to tournament players", p)
            players.append(p)

        return render(request, TOURNAMENT_PLAYER_FORM, {
            'players': players,
            'error': error
        })

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle POST request - process selected players."""
        players = request.POST.getlist(SESSION_PLAYERS_KEY)
        if not players:
            return render(request, TOURNAMENT_PLAYER_FORM,
                          {'error': 'Please select at least one player'})

        request.session[SESSION_PLAYERS_KEY] = players
        return render(request, TOURNAMENT_PLAYER_FORM, {'players': players})


def add_player_tournament(request: HttpRequest) -> HttpResponse:
    """View to add a player to the report/tournament.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object.

    Returns
    -------
    HttpResponse
        Redirects to tournament players page
    """
    logger.debug("Processing add_player_tournament for request: %s", request)

    if request.method != "POST":
        return redirect('report-players')

    player_data = request.POST
    logger.debug("Received POST data: %s", player_data)

    player_cfc_id = player_data.get("player_cfc_id")
    report_players = request.session.get(SESSION_PLAYERS_KEY, default=[])
    try:
        player = get_player_from_cfc_id(player_cfc_id)
        report_players.append(player_data.get("player_cfc_id"))

        request.session[SESSION_PLAYERS_KEY] = report_players
        logger.info("Added player: %s. Report players: %s", player,
                    report_players)
        request.session.modified = True
        return redirect('report-players')

    except (ValueError, KeyError) as e:
        logger.error("Failed to add player: %s", str(e))
        return redirect('report-players')


def remove_player_tournament(request: HttpRequest,
                             cfc_id=None) -> HttpResponse:
    """View to remove a player from the report/tournament.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object.
    cfc_id : id of player to remove

    Returns
    -------
    HttpResponse
        an empty response to swap into html
    """

    if cfc_id is None:
        logger.error("remove_player_tournament called without cfc id")
        return redirect('report-players')

    logger.debug("Processing remove_player_tournament for request: %s",
                 request)

    # remove id from the SESSION_PLAYERS list
    if cfc_id in request.session[SESSION_PLAYERS_KEY]:
        request.session[SESSION_PLAYERS_KEY].remove(cfc_id)
        # tell django that the session has changed
        request.session.modified = True
    else:
        logger.error(
            "remove_player_tournament called with cfc_id not in tournament. id: %s",
            cfc_id)

    # return an empty response to be swaped in
    return HttpResponse("")


def get_player_from_cfc_id(cfc_id: str) -> Player:
    """Get or create a player from CFC ID by fetching data from CFC API.

    Parameters
    ----------
    cfc_id : str | None
        The CFC ID of the player

    Returns
    -------
    Player
        Created player instance

    Raises
    ------
    ValueError
        If CFC ID is invalid or player info cannot be retrieved
    """
    if not cfc_id:
        raise ValueError("CFC ID is required")

    player_info = cfc_api_utils.get_player_info(cfc_id)

    player, created = Player.create_player_if_not_exists(player_info)
    if created:
        logger.info(
            "Successfully created (saved) player from CFC ID: %s. Player info %s",
            player, player_info)
    else:
        logger.info("Successfully got player from CFC ID: %s. Player info %s",
                    player, player_info)

    return player
