"""services relating to tournements in sessions in cfc_report app"""

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
from cfc_report.models.tournament import Round, Tournament

# get the current session
session = SessionStore()


def get_rounds():
    """Get the rounds from this session

    Uses
    ----
    session : Django session
        the current session got from session store
    """


def get_tournament() -> Tournament:
    """get the tournament worked on in this session

    Uses
    ----
    session : A Django session
        the session got from the store. Must include "TournamentPK"
        The session key must be the primary key of a tournament or 404

    Returns
    -------
    models.Tournament being worked on in this session.
    """
    key = session.get("TournamentPK")
    logger.info("session.get('TournamentPK') gave: %s", key)

    return get_object_or_404(Tournament, pk=key)


def get_tournament_info():  # -> "TournamentInfo":
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

    logger.info(
        "get_tournament_name() got %s from session['tournamentInfo'] %s",
        tournament_name,
        info,)
    return tournament_name


def get_building_round_number() -> int:
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

    get = session.get("building_round")

    logger.debug("get_building_round_number: session get: %s", get)

    if get is None:
        raise ReferenceError("'building_round' is None in session")

    return int(get)


def set_building_round_number(rnd: int) -> None:
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

    session["building_round"] = rnd


def finalize_round() -> None:
    """Save this round, and prepair to add another one

    side-effects
    ------------
    - round_number++
    - create and save a round model
    - reset matches in round to None
    """

    round_number = get_building_round_number()

    logger.debug(
        "session.finalize_round() entered. Finalizing rnd: %s, matches: %s",
        round_number,
    )
    rnd = Round(round_num=round_number)
    # save round
    rnd.save()
    logger.debug("Tournament round %s made and saved. round: %s",
                 round_number, rnd)

    # prepare for next round
    logger.debug("set ['building_round'] to %s, session keys: %s",
                 rnd,
                 session.keys())

    set_building_round_number(round_number + 1)
    # reset the matches
    session["matches"] = None

    logger.debug("session prepaired for round %s", round_number)


def is_last_round() -> bool:
    """Check to see if this is the last round of the tourniment we are building
    Uses
    ----
    session : A Django session
        the session got from the session store
    """
    cur_round = get_building_round_number()

    logger.debug("is_last_round entered on round %s", round)

    info = get_tournament_info()

    # check if number of rounds < cur_round.
    lr = int(info["num_rounds"]) < cur_round

    logger.debug("is_last_round() found: %s", lr)
    return lr


def set_tournament_info(info: dict) -> None:
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
    session["building_round"] = 1
