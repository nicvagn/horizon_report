"""create a player in database"""
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

from .models import Player


def create_player(name: str, cfc_id) -> Player:
    """create a chess player with a cfc id"""
    # make sure cfc id is valid form
    try:
        cfc = int(cfc_id)

        # ensure cfc id is 6 characters
        if cfc < 100000 or cfc > 999999:
            raise ValueError("CFC ID not 6 characters")

    except ValueError as ex:
        logging.error("CFC ID not valid form, value: %s", cfc_id)
        raise ex

    # make player model
    p = Player(name=name, cfc_id=cfc)

    return p
