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
from django.shortcuts import get_object_or_404

from cfc_report import logger
from cfc_report.models.tournament import Round, Tournament
from cfc_report.types import TournamentInfo


def get_rounds():
    """Get the rounds from this session_services

    Uses
    ----
    session_services : Django session_services
        the current session_services got from session_services store
    """


def get_tournament(session) -> Tournament:
    """get the tournament worked on in this session_services

    Uses
    ----
    session_services : A Django session_services
        the session_services got from the store. Must include "TournamentPK"
        The session_services key must be the primary key of a tournament or 404

    Returns
    -------
    models.Tournament being worked on in this session_services.
    """
    key = session.get("TournamentPK")
    logger.info("session_services.get('TournamentPK') gave: %s", key)
    return get_object_or_404(Tournament, slug=key)


def get_tournament_info(session) -> TournamentInfo:
    """get the TournamentInfo from this session_services

    Uses
    ----
    session_services : A Django session_services
        the session_services got from the session_services store

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
    logger.debug("session_services keys: %s", session.keys())

    get = session.get("TournamentInfo")

    logger.debug("session_services get: %s", get)

    return get


def get_tournament_name(session) -> str:
    """get the name of the tournament we are building

    Uses
    ----
    session_services : A Django session_services
        the session_services got from the session_services store
    Returns
    -------
    str : the tournament name
    """

    info = session["TournamentInfo"]

    tournament_name = info["name"]

    logger.info(
        "get_tournament_name() got %s from session_services['tournamentInfo'] %s",
        tournament_name,
        info, )
    return tournament_name


def get_building_round_number(session) -> int:
    """get the number of the tournament round we are building from this session_services

    Uses
    ----
    session_services : A Django session_services
        the session_services got from the session_services store
    Returns
    -------
    int : the round number
    """
    logger.debug("session_services keys: %s", session.keys())

    get = session.get("BuildingRound")

    logger.debug("get_building_round_number: session_services get: %s", get)

    if get is None:
        raise ReferenceError("'building_round' is None in session_services")

    return int(get)


def set_building_round_number(session, rnd=1) -> None:
    """set the tournament round we are building from this session_services

    Parameters
    ----------
    rnd : int
        the round number to set the round we are building to

    Uses
    ----
    session : A Django session_services
        the session_services got from the session_services store
    """

    session["BuildingRound"] = rnd


def finalize_round(session) -> None:
    """Save this round, and prepair to add another one

    side-effects
    ------------
    - round_number++
    - create and save a round model
    - reset matches in round to None
    """

    round_number = get_building_round_number()

    logger.debug(
        "session_services.finalize_round() entered. Finalizing rnd: %s, matches: %s",
        round_number,
    )
    rnd = Round(round_num=round_number)
    # save round
    rnd.save()
    logger.debug("Tournament round %s made and saved. round: %s",
                 round_number, rnd)

    # prepare for next round
    logger.debug("set ['building_round'] to %s, session_services keys: %s",
                 rnd,
                 session.keys())

    set_building_round_number(round_number + 1)
    # reset the matches
    session["matches"] = None

    logger.debug("session_services prepared for round %s", round_number)


def set_tournament_info(session, info: TournamentInfo) -> None:
    """set the tournament info for this session_services

    Parameters
    ----------
    session : A Django session_services
        the session_services got from the session_services store

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

    Notes
    -----
    sets TournamentInfo, TournamentPK, and BuildingRound in the session_services
    """
    logger.debug("session_services key TournamentInfo set to %s", info)
    session["TournamentInfo"] = info

    # set the primary key for accessing the tournament fro
    session["TournamentPK"] = f"{info['name']}|{info['date']}"
    # start building at round 1
    session["BuildingRound"] = 1
