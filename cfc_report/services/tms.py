""" work with, and produce tms cfc file """
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
# Copyright (C) 2024  Nicolas Vaagen
from typing import List

# make a ctr tournament report file
from cfc_report import logger
from cfc_report.models import Match, Player, Tournament


class CtrCreationException(Exception):
    """Something went wrong with ctr creation"""
    pass


class TMS:
    """TMS is a wrapper class for TMS (Tournament Report) File format"""
    def __init__():
        tms = []


if __name__ == "__main__":
    # test
    T = {"name": "my test tornament",
         "num_rounds": 4,
         "pairing_system": "Swiss",
         "td_cfc": "111111",
         "to_cfc": "222222",
         "date_year": "1",
         "date_month": "1",
         "date_day": "1", }
    tms = TMS(T)
    tms.write_to_file()
