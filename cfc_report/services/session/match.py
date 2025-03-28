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
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import get_object_or_404

from cfc_report.models.person import Player
from cfc_report.models.tournament import Match, Round, Tournament
from cfc_report.services import database
from cfc_report import logger
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import get_object_or_404

from cfc_report.models.person import Player
from cfc_report.models.tournament import Match, Round, Tournament
from cfc_report.services import database
session = SessionStore()


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
            "Could not find match %s in session matches %s", m, get_matches()
        )
    logger.debug("match with pk %s removed. matches now %s", pk, new_matches)
    session["matches"] = new_matches
