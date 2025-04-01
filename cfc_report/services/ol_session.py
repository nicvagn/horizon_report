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
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import get_object_or_404

from cfc_report import logger
from cfc_report.models.person import Player
from cfc_report.models.tournament import Match, Round, Tournament
from cfc_report.services import database

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
    players : list(Player)
        A list of the players in session
    """

    session_ids = session.get("players_by_cfc")
    logger.debug("cfc id's got from session: %s", session_ids)
    players: list[Player] = []

    # go through the session player id's and fetch players from db
    if session_ids:
        for cfc_id in session_ids:

            p = database.get_player_by_cfc(cfc_id)
            players.append(p)

            logger.debug("session_id: %s got %s", cfc_id, p)

        logger.debug("Players in session: %s", players)
    else:
        logger.warning("No players gotten from session")

    return players


def get_players_by_id():
    """get the players in current session

    Uses
    ----
    session : A Django session
        the session got from the session store

    Returns
    -------
    players : "dict{str(cfc id):Player}"
        A dict of the players in session by there id
    """

    session_players = session.get("players_by_cfc")
    logger.debug("players got from session: %s", session_players)
    players = {}

    if session_players:
        for cfc_id in session_players:
            logger.debug("session_players: %s", session_players)

            p = database.get_player_by_cfc(cfc_id)

            players[cfc_id] = p

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

    # should return an empty list if None
    if session_players is None:
        session_players = []

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


def add_player_by_id(cfc_id: str) -> None:
    """add a player to the current session

    Side-effects
    ------------
    creates session["players_by_cfc"] if it does not exist.
    If it does adds cfc_id

    Parameters
    ----------
    cfc_id : String CFC id ie: 123123
        some player's cfc id to add to list
    """
    if "players_by_cfc" in session:
        session["players_by_cfc"].append(cfc_id)
    else:
        session["players_by_cfc"] = [cfc_id]


def remove_player_by_id(cfc_id: str) -> None:
    """remove a player from session by id

    Side-effects
    ------------
    removes player with cfc id given from session

    Parameters
    ----------
    cfc_id : str
        some player's cfc id to remove from the session list
    """
    session_players = session.get("players_by_cfc")

    logger.debug("players in session by cfc i: %s", session_players)

    session_players.remove(cfc_id)

    logger.debug("removed %s, session_players now %s", cfc_id, session_players)


def get_matches() -> list("Match"):
    """Get the matches in the session
    Uses
    ----
    session : A Django session
        the active session

    Returns
    -------
    A list of the matches
    """
    session_matches = session.get("matches")

    logger.info("matches got from session: %s, of type: %s",
                session_matches, type(session_matches))

    return session_matches


def create_match(white_id, black_id, result) -> Match:
    """Create a chess match in this session
    Arguments
    ---------
    result : one of Match.RESULT_CHOICES ie:
        RESULT_CHOICES = [(RESULT_BLACK, "0 - 1"), (RESULT_WHITE, "1 - 0"),
                        (RESULT_DRAW, "0.5 - 0.5"), (RESULT_UNKNOWN, "_")]
    Uses
    ----
    session - the django session got from the session store

    side-effects
    ------------
    modifies the session "matches"

    Returns
    -------
    the created match
    """
    # get match players from database
    white_player = database.get_player_by_cfc(white_id)
    black_player = database.get_player_by_cfc(black_id)

    tournament_rnd = session.get("building_round")

    chess_match = Match(
        white=white_player, black=black_player, result=result,
        round=tournament_rnd)

    if session.has_key("matches") and session["matches"] is not None:
        # update it
        session["matches"].append(chess_match)
    else:
        # create it
        session["matches"] = [chess_match]

    return chess_match
