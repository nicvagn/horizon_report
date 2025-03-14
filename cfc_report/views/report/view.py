"""view a cfc report"""
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
from django.http import HttpResponse
from django.shortcuts import render
from cfc_report.services import database


def report(request) -> HttpResponse:
    """display a CFC report"""

    logger.debug("view.report entered with request: %s", request)

    player_list = database.get_players()
    num_players = player_list.count()
    report = {
        "name": "The Masters",
        "province": "SK",
        "time_format": "blitz",
        "td_cfc": "111111",  # FIXME
        "to_cfc": "222222",
        "date": "06/06/87",
        "players": player_list,
        "num_players": num_players,
    }
    return render(request, "cfc_report/show/index.html", report)
