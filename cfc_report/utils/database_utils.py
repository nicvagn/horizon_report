"""Helpers for database"""
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

from .. import logger
from ..models.player import Player

# constant for session players key
SESSION_PLAYERS_KEY = "players"
# file constant
NEW_PLAYER_TEMPLATE = "cfc_report/create/add-player-system-form.html"
TOURNAMENT_PLAYER_FORM = "cfc_report/create/player-form.html"


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
    ValueError if parameter name or cfc_id is invalid

    Returns
    -------
    Player
        The created Player instance.
    """
    if not name or not cfc_id:
        raise ValueError("Both Player Name and CFC ID are required.")
    # validate cfc id
    if not is_cfc_id_valid(cfc_id):
        raise ValueError("CFC ID is invalid. Please provide a valid 6-digit number.")

    player = Player.create(name, cfc_id)

    logger.debug("Created Player: %s with CFC ID: %s",
                 player, player.cfc_id)

    player.save()
    logger.info("Player %s saved to database.", player)

    return player
