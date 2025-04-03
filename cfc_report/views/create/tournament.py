"""view for creating a tournament in a cfc report"""

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
from cfc_report.models import Player
from cfc_report.services import session_services
from cfc_report.services.ctr_builder import CTR_builder


def preview_ctr(request) -> HttpResponse:
    """Preview chess report, see all the players, rounds and games that will be
    in the report

    Arguments
    ---------
    request : HttpRequest

    Notes
    -----
    Uses:
        session_services["TournamentInfo"]
        CTR_builder service
    """
    session = request.session
    logger.debug("create.preview_report entered with request: %s", request)
    # get tournament information
    t_info = session_services.get_tournament_info(session=session)

    logger.debug("Tournament Info got: %s", t_info)
    ctr = CTR_builder(t_info, session)
    logger.debug("|CTR| created: %s", ctr)

    context = {
        "tournament_name": session_services.get_tournament_name(session=session),
        "ctr": str(ctr),
        "tms": "TMS NOT DONE",
    }

    return render(request, "cfc_report/show/preview-report.html", context)


def finalize_report(request) -> HttpResponse:
    """Finalize a chess tournament report

    Arguments
    ---------
    request : HttpRequest
    """
    logger.debug("Create.finalize_report entered with request: %s", request)

    # get tournament information
    t_info = session_services.get_tournament_info(session=request.session)

    logger.debug("Tournament Info got: %s", t_info)
    ctr = CTR_builder(t_info, session_services)
    ctr.save()
    logger.debug("|CTR| created and saved: %s", ctr)

    ctr.write_file(t_info)
    context = {"ctr": str(ctr)}

    return render(request, "cfc_report/show/ctr.html", context)


def preview(request):
    """Preview the tournament report"""
    session = request.session
    # get the tournament info set in Create.initial()
    tournament_info = session_services.tournament.get_tournament_info(session=session)

    # get information on tournament players from the session_services
    players: list[Player] = session_services.player.get_players()

    context = {
        "name": tournament_info["name"],
        "province": tournament_info["province"],
        "time_format": "blitz",
        "num_players": len(players),
        "players": players,
        "td_cfc": tournament_info["td_cfc"],
        "to_cfc": tournament_info["to_cfc"],
    }
    logger.debug("context: %s", context)
    return render(request, "cfc_report/show/index.html", context)
