"""services relating to sessions in cfc_report app"""
# Copyright (C) 2024  Nicolas Vaagen
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
import logging
from django.contrib.sessions.backends.db import SessionStore

from ..constants import LOGGER_NAME
from ..models import Player
logger = logging.getLogger(LOGGER_NAME)

# get the current session
session = SessionStore()


def get_session_players() -> list[Player]:
    """get the players in current session

    Parameters
    ----------
    session : A Django session
        the sassion to get players from

    Returns
    -------
    list(Player)
        A list of the players in session
    """

    serialized_players = session.get("players")
    logger.debug("serialized_players got from session: %s", serialized_players)
    session_p: list[Player] = []

    if serialized_players:
        for p in serialized_players:
            session_p.append(Player.decode(p))

        logger.debug("Players in session: %s", session_p)
    else:
        serialized_players = []
    return session_p


def update_session_players(players: list[Player]) -> None:
    """update players in current session

    Parameters
    ----------
    players : list(Players)
        The new list of players to set the session players too
    """

    logger.debug("updating session Players to be: %s", players)
    serialized_players = []
    for p in players:
        serialized_players.append(p.serialize())

    session["players"] = serialized_players
