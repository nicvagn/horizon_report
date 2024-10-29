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
from .database import get_player_by_cfc

logger = logging.getLogger(LOGGER_NAME)

# get the current session
session = SessionStore()


def get_players() -> list[Player]:
    """get the players in current session

    Uses
    ----
    session : A Django session
        the session got from the session store

    Returns
    -------
    list(Player)
        A list of the players in session
    """

    session_players = session.get("players_by_cfc")
    logger.debug("players got from session: %s", session_players)
    players: list[Player] = []

    if session_players:
        for cfc_id in session_players:
            players.append(get_player_by_cfc(cfc_id))

        logger.debug("Players in session: %s", players)
    else:
        logger.warning("No players gotten from session")

    return players


def get_player_ids() -> list[str]:
    """get the cfc id's of players in current session 

    Uses
    ----
    session : A Django session
        the session got from the session store

    Returns
    -------
    list(str)
        A list of the cfc id's in session.
        A cfc id is a 6 character numeric str
    """

    session_players = session.get("players_by_cfc")

    logger.debug("session players id's gotten: %s", session_players)
    return session_players


def update_players(players: list[Player]) -> None:
    """update players in current session

    Parameters
    ----------
    players : list(Players)
        The new list of players to set the session players too
    """

    logger.debug("updating session Players to be: %s", players)
    session_players_cfc_id = []
    for p in players:
        session_players_cfc_id.append(p.cfc_id)

    session["players_by_cfc"] = session_players_cfc_id


def add_player_by_id(cfc_id: "CfcId") -> None:
    """add a player to the current session

    Side-effects
    ------------
    creates session["players_by_cfc"] if it does not exist.
    If it does adds cfc_id

    Parameters
    ----------
    cfc_id : CfcId
        some player's cfc id to add to list
    """

    if "players_by_cfc" in session:
        session["players_by_cfc"].append(cfc_id)
    else:
        session["players_by_cfc"] = [cfc_id]
