"""services relating to cfc_report app"""
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
from cfc_report.models import Player
from cfc_report import LOGGER_NAME
# get the logger for cfc_report module. Should be set up.
logger = logging.getLogger(LOGGER_NAME)


def create_player(name: str, cfc_id: any) -> Player:
    """create a chess player with a cfc id
        parameters:
            name: the players name
            cfc_id: something that can be casted to an 6 character int
        returns:
            The created Player
    """
    # make sure cfc id is valid form
    try:
        cfc = int(cfc_id)

        # ensure cfc id is 6 characters
        if cfc < 100000 or cfc > 999999:
            raise ValueError("CFC ID not 6 characters")

    except ValueError as ex:
        logger.error("CFC ID not valid form, value: %s", cfc_id)
        raise ex

    p = Player(name=name, cfc_id=cfc)

    logger.info("Player: name=%s, cfc_id=%s made.", name, cfc_id)

    return p
