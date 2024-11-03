"""create cfc reports"""
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

from cfc_report import logger
from cfc_report.models import Player, Tournament


def create(t: Tournament):
    """create a report given a Tournament
    todo
    """
    report = {
        "title": t.name,
        "province": t.province,
        "time_format": "blitz",
        "td_cfc": t.td_cfc,
        "to_cfc": t.to_cfc,
        "tournament_date": t.date,
        "players": t.players,
        "num_players": len(t.players),
    }

    logger.debug("report created: %s", report)
    return report
