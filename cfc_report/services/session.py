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
from cfc_report import logger
from django.contrib.sessions.backends.db import SessionStore
import json

from . import database
from ..models import Match, Player, Round, Tournament

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


def get_players_by_id() -> "dict{CfcId:Player}":
    """get the players in current session

    Uses
    ----
    session : A Django session
        the session got from the session store

    Returns
    -------
    players: "dict{CfcId:Player}"
        A dict of the players in session by there id
    """

    session_players = session.get("players_by_cfc")
    logger.debug("players got from session: %s", session_players)
    players: "dict{CfcId:Player}" = {}

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


def remove_player_by_id(cfc_id: "CfcId") -> None:
    """remove a player from session by id

    Side-effects
    ------------
    removes player with cfc id given from session

    Parameters
    ----------
    cfc_id : CfcId
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

    logger.info("matches got from session: %s", session_matches)

    return session_matches


def create_match(
        white_id: "CfcId", black_id: "CfcId", result: "w,b,or d") -> Match:
    """Create a chess match in database, and adds it to this session
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
    white_player = database.get_player_by_cfc(white_id)
    black_player = database.get_player_by_cfc(black_id)

    chess_match = database.add_match(white_id, black_id, result)


    if session.has_key("matches"):
        # update it
        session["matches"].append(chess_match)
    else:
        # create it
        session["matches"] = [chess_match]

    return chess_match


def remove_match_by_pk(pk: "PrimaryKey"):
    """remove a match from this session by it's primarry key

    Parameters
    ----------
    pk : the primary key of the match

    Uses
    ----
    session : Django session
        the current session got from session store

    Side Effects
    ------------
    removes the match from this session
    """
    old_matches = get_matches()
    logger.debug("removing match with pk: %s\n all matches: %s",
                 pk, old_matches)
    match_found = False
    new_matches = []
    # check all the matches in order appending them if match.pk != pk
    for m in old_matches:
        if m.pk == pk:
            logger.debug("found match for removal")
            match_found = True
        else:
            new_matches.append(m)

    if match_found is False:
        raise RuntimeError("Could not find match %s in session matches %s",
                           m,
                           get_matches())
    logger.debug("match with pk %s removed. matches now %s", pk, new_matches)
    session["matches"] = new_matches


def get_tournament_info() -> "TournamentInfo":
    """get the TournamentInfo from this session

    Uses
    ----
    session : A Django session
        the session got from the session store

    Returns
    -------
    "TournamentInfo"
        or {"name": self.name,
            "num_rounds": self.num_rounds,
            "date": str(self.date),
            "pairing_system": str(self.pairing_system),
            "province": str(self.province),
            # TournamentOrganizer CFC id
            "to_cfc": str(self.to_cfc),
            # TournamentDirector CFC id
            "td_cfc": str(self.td_cfc),
        }
        from tournament info form
    """
    logger.debug("session keys: %s", session.keys())

    get = session.get("TournamentInfo")

    logger.debug("session get: %s", get)

    return get


def set_tournament_round(rnd: int) -> None:
    """set the tournament round we are building from this session

    Parameters
    ----------
    rnd : int
        the round number to set the round we are building to

    Uses
    ----
    session : A Django session
        the session got from the session store
    """
    logger.debug("session keys: %s", session.keys())

    session["TournamentRound"] = rnd


def get_tournament_round() -> int:
    """get the tournament round we are building from this session

    USES
    ----
    session : A Django session
        the session got from the session store

    Returns
    -------
    int : the round number
    """
    logger.debug("session 'TournamentRound': %s", session["TournamentRound"])

    return int(session["TournamentRound"])



def set_tournament_info(info: "TournamentInfo") -> None:
    """set the tournament info for this session

    Parameters
    ----------
    info : "TournamentInfo"
        or {"name": self.name,
            "num_rounds": self.num_rounds,
            "date": str(self.date),
            "pairing_system": str(self.pairing_system),
            "province": str(self.province),
            # TournamentOrganizer CFC id
            "to_cfc": str(self.to_cfc),
            # TournamentDirector CFC id
            "td_cfc": str(self.td_cfc),

        from tournament info from form

    Uses
    ----
    session : A Django session
        the session got from the session store

    """
    logger.debug("session key TournamentInfo set to %s", info)
    session["TournamentInfo"] = info

    # start building at round 1
    session["TournamentRound"] = 1

def finalize_round() -> None:
    """Save the round being built in the session, and prepair to add another one
    be built.

    side-effects
    ------------
    - incrument tournamentRound in session
    - reset matches in round to None
    """
    breakpoint()
    round_number = get_tournament_round()

    logger.debug("finalize_round: round %s finalized ", round_number)
    rnd = Round(round_number=round_number)
    rnd.save()
    logger.debug("Tournament round %s made and saved. round: %s", round_number, rnd)


    session["matches"] = new_matches

    session["TournamentRound"] += 1


def dumby_populate():
    """populate session w dummby data"""
    players = database.get_players()

    breakpoint()
