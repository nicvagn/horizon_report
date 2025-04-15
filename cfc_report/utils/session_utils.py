# """utils for managing sessions"""
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

from django.http import HttpRequest

from .. import logger
from ..models.person_with_cfc_id_models import Player
from ..serialize import PlayerSerializer

# constant for session players key
SESSION_PLAYERS_KEY = "players"
# file constant
NEW_PLAYER_TEMPLATE = "cfc_report/create/player.html"
TOURNAMENT_PLAYER_FORM = "cfc_report/create/player-form.html"


def get_session_players(request: HttpRequest) -> list[Player]:
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
    try:
        players = request.session["players"]

    # could be start of picking players
    except KeyError:
        logger.info("No session players got from request: %s", request)
        players = []

    players = PlayerSerializer.deserialize_list(players, Player)

    logger.debug("Players in session: %s", players)

    return players


def _is_cfc_id_valid(cfc_id: str | int) -> bool:
    """Validates whether the provided CFC ID is a 6-digit numeric identifier.

    Parameters
    ----------
    cfc_id : str
        The CFC ID string.

    Returns
    -------
    bool
        True if valid, False otherwise.
    """
    if isinstance(cfc_id, int):
        cfc_id = str(cfc_id)
    return cfc_id.isdigit() and len(cfc_id) == 6


def _validate_player_data(data: dict) -> str | None:
    """Validates player data from submitted form.

    Parameters
    ----------
    data : dict
        The submitted player data.

    Returns
    -------
    str | None
        An error message if validation fails, otherwise None.
    """
    player_name = data.get("player_name")
    player_cfc_id = data.get("player_cfc_id")

    if not player_name or not player_cfc_id:
        return "Both Player Name and CFC ID are required."
    if not _is_cfc_id_valid(player_cfc_id):
        return "CFC ID is invalid. Please provide a valid 6-digit number."
    return None


def create_player(name: str, cfc_id: int) -> Player:
    """Helper function to create a player and save it to the database.

    Notes
    -----
    Adds player to db

    Parameters
    ----------
    name : str
        The name of the player to be created.
    cfc_id : int
        The CFC ID of the player to be created.

    Raises
    ------
    valueError if name or cfc_id is invalid

    Returns
    -------
    Player
        The created Player instance.
    """
    if not name or not cfc_id:
        raise ValueError("Both Player Name and CFC ID are required.")
    # validate cfc id
    if not _is_cfc_id_valid(cfc_id):
        raise ValueError("CFC ID is invalid. Please provide a valid 6-digit number.")

    player = Player.create(name, cfc_id)

    logger.debug("Created Player: %s with CFC ID: %s",
                 player, player.cfc_id)

    player.save()
    logger.info("Player %s saved to database.", player)

    return player


def toggle_player_in_session(session_players: list[Player], cfc_id: int) -> list[Player]:
    """
    Adds or removes a player with the given CFC ID from the session players.

    Parameters
    ----------
    session_players : list[Player]
        Current list of players in the session.
    cfc_id : int
        The CFC ID of the player to toggle.

    Returns
    -------
    list[Player]
        Updated list of players in the session.
    """

    # Find a player in the session with the given CFC ID
    existing_player = next((player for player in session_players if player.cfc_id == cfc_id), None)

    # If the player exists, remove them; otherwise, add a new one
    if existing_player:
        session_players = [player for player in session_players if player.cfc_id != cfc_id]
        logger.info("Removed player with CFC ID: %s from session.", cfc_id)
    else:
        try:
            new_player = Player.objects.get(cfc_id=cfc_id)
            session_players.append(new_player)
            logger.info("Added player with CFC ID: %s to session.", cfc_id)
        except Player.DoesNotExist:
            logger.warning("Player with CFC ID: %s does not exist.", cfc_id)

    return session_players


def get_tournament_info(request: HttpRequest) -> dict | None:
    """Get the tournament currently being built in this session.

    Parameters
    ----------
    request : HttpRequest
        Django request object.

    Returns
    -------
    dict | None
        The tournament information if present in the session, otherwise None.

    Notes
    -----
    Logs appropriate warning if no tournament information is found in the session.
    """
    try:
        tournament = request.session.get("tournament_info", None)
        if not tournament:
            logger.warning("No tournament found in session for request: %s", request)
        return tournament
    except KeyError:
        logger.error("Error accessing tournament information from session for request: %s", request)
        return None
