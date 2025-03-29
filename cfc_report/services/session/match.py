"""services relating to chess matches in sessions in cfc_report app"""

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
from cfc_report.models.tournament import Match
from cfc_report.services import database
from django.contrib.sessions.backends.db import SessionStore

session = SessionStore()


def get_matches() -> [Match]:
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
    tournament_rnd = session.tournament.building_round_number()
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


def remove_match_by_pk(pk) -> None:
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
            "Could not find match with pk: %s in session matches %s" % (
                pk, get_matches())
        )
    logger.debug("match with pk %s removed. matches now %s", pk, new_matches)
    session["matches"] = new_matches
