"""Data services for modifying and creating data for a CFC rated tournament"""
# horizon_pair
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
from django.db.models import QuerySet
from cfc_report.models import (Player, TournamentDirector,
                               TournamentOrganizer)


logger = logging.getLogger("horizon_report")


def get_players() -> QuerySet:
    """Get players in database
    returns:
        QuerySet of players in db
    """
    all_players = Player.objects.all()
    logger.debug("get_players got these players from db: %s", all_players)
    return all_players


def add_player(p: Player) -> None:
    """Add a player to the database
    parameters:
        p: The models.Player object to add
    """
    logger.debug("player %s added to db", p)
    p.save()


def get_TDs() -> QuerySet:
    """Get TournamentDirector's in database
    returns:
        QuerySet of TD's
    """
    tds = TournamentDirector.objects.all()
    logger.debug("get_TDs got %s", tds)
    return tds


def get_TOs() -> QuerySet:
    """Get TournamentDirector's in database
    returns:
        QuerySet of TD's
    """
    tos = TournamentOrganizer.objects.all()
    logger.debug("get_TOs got: %s", tos)
    return tos
