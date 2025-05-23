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
from django.shortcuts import render, redirect
from django.views import View

from cfc_report.models.player import Player
from cfc_report.utils import cfc_api_utils
from . import logger

# constant for session players key
SESSION_PLAYERS_KEY = "players"
# file constant
NEW_PLAYER_TEMPLATE = "cfc_report/create/add-player-system-form.html"
TOURNAMENT_PLAYER_FORM = "cfc_report/create/player-form.html"


class TournamentPlayersView(View):
    """view for selecting players in a Report for a CFC Rated tournament."""

    template_name = "cfc_report/report/players/tournament-players.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET request - display available players."""

        players = request.session.get(SESSION_PLAYERS_KEY, default=[])

        return render(request, self.template_name, {'players': players})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle POST request - process selected players."""
        tournament_players = request.POST.getlist(SESSION_PLAYERS_KEY)
        if not tournament_players:
            return render(request, self.template_name, {
                'error': 'Please select at least one player'
            })

        request.session[SESSION_PLAYERS_KEY] = tournament_players
        return render(request, self.template_name, {'players': players})


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
        return redirect('report-tournament-players')

    player_data = request.POST
    logger.debug("Received POST data: %s", player_data)

    try:
        player = create_player_from_cfc_id(player_data.get("player_cfc_id"))

        player.save()  # SIDE EFFECT, player saved to database

        players = request.session.get(SESSION_PLAYERS_KEY, default=[])

        players.append(player_data.get("player_cfc_id"))

        request.session[SESSION_PLAYERS_KEY] = players
        logger.info("Added player: %s. Tournament players: %s", player, players)

        return redirect('report-tournament-players')
    except (ValueError, KeyError) as e:
        logger.error("Failed to add player: %s", str(e))
        # Here you might want to add proper error handling
        raise e


def create_player_from_cfc_id(cfc_id: str | None) -> Player:
    """Create a player from CFC ID by fetching data from CFC API.

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
        logger.info("Successfully created player from CFC ID: %s. Player info %s", player, player_info)
    else:
        logger.info("Successfully got player from CFC ID: %s. Player info %s", player, player_info)

    return player
