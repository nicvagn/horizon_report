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
from django.shortcuts import get_object_or_404

from ..models import Match, Player, Round, Tournament
from . import database

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

    logger.info("matches got from session: %s, of type: %s",
                session_matches, type(session_matches))

    return session_matches


def create_match(white_id: "CfcId", black_id: "CfcId", result: "w,b,or d") -> Match:
    """Create a chess match in this session
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
    tournament_rnd = get_tournament_round_number()
    chess_match = Match(
        white=white_player, black=black_player, result=result,
        round_number=tournament_rnd)

    if session.has_key("matches") and session["matches"] is not None:
        # update it
        session["matches"].append(chess_match)
    else:
        # create it
        session["matches"] = [chess_match]

    return chess_match


def remove_match_by_pk(pk: "PrimaryKey") -> None:
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
        raise RuntimeError(
            "Could not find match %s in session matches %s", m, get_matches()
        )
    logger.debug("match with pk %s removed. matches now %s", pk, new_matches)
    session["matches"] = new_matches

def get_rounds() -> "Queryset":
    """Get the rounds from this session

    Uses
    ----
    session : Django session
        the current session got from session store

    """


def finalize_round() -> None:
    """Save this round, and prepair to add another one

    side-effects
    ------------
    - round_number++
    - create and save a round model
    - reset matches in round to None
    """

    round_number = get_tournament_round_number()
    matches = get_matches()

    logger.debug(
        "session.finalize_round() entered. Finalizing rnd: %s, matches: %s",
        round_number,
        matches,
    )
    rnd = Round(round_num=round_number, )
    # save round
    rnd.save()
    logger.debug("Tournament round %s made and saved. round: %s", round_number, rnd)

    logger.debug("round made and saved. round: %s", rnd)
    # prepare for next round
    set_tournament_round_number(round_number + 1)
    # reset the matches
    session["matches"] = None

    logger.debug("session prepaired for round %s", round_number)

#def get_tournament() -> Tournament:
    #"""get the tournament worked on in this session
#
    #Uses
    #----
    #session : A Django session
        #the session got from the session store
#
    #Returns
    #-------
    #models.Tournament being worked on in this session.
    #"""
#
    #key = get_tournament_name()
#
    #return get_object_or_404(Tournament, pk=key)
#



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


def get_tournament_name() -> str:
    """get the name of the tournament we are building

    Uses
    ----
    session : A Django session
        the session got from the session store
    Returns
    -------
    str : the tournament name
    """

    info = session["TournamentInfo"]

    tournament_name = info["name"]

    logger.info("get_tournament_name() got %s from session['tournamentInfo'] %s",
                tournament_name,
                info,)
    return tournament_name


def get_tournament_round_number() -> int:
    """get the number of the tournament round we are building from this session

    Uses
    ----
    session : A Django session
        the session got from the session store
    Returns
    -------
    int : the round number
    """
    logger.debug("session keys: %s", session.keys())

    get = session.get("TournamentRound")

    logger.debug("get_tournament_round: session get: %s", get)

    return int(get)


def set_tournament_round_number(rnd: int) -> None:
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


def is_last_round() -> bool:
    """Check to see if this is the last round of the tourniment we are building
    Uses
    ----
    session : A Django session
        the session got from the session store
    """
    cur_round = get_tournament_round_number()

    logger.debug("is_last_round entered on round %s", round)

    info = get_tournament_info()

    # check if number of rounds < cur_round.
    lr = int(info["num_rounds"]) < cur_round

    logger.debug("is_last_round() found: %s", lr)
    return lr


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
