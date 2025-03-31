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

from django.http import HttpResponse
from django.shortcuts import render

from cfc_report import logger
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

def preview_report(request) -> HttpResponse:
    """Preview chess report, see all the players, rounds and games that will be
    in the report

    Arguments
    ---------
    request : HttpRequest
    """

    logger.debug("create.preview_report entered with request: %s", request)
    # get tournament information
    t_info = session.get_tournament_info()

    logger.debug("Tournament Info got: %s", t_info)
    ctr = CTR_builder(t_info, session)
    logger.debug("|CTR| created: %s", ctr)

    context = {
        "tournament_name": session.get_tournament_name(),
        "ctr": str(ctr),
        "tms": "TMS NOT DONE",
    }

    return render(request, "cfc_report/show/preview-report.html", context)
