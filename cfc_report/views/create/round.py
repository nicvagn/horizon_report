"""Create round in a report for a CFC Rated tournament."""
# Copyright (C) 2024 Nicolas Vaagen
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
from django.views.generic import View
from cfc_report import logger
from cfc_report.models import Round
# TODO: Create a view to gennerate the model
class Round()


def round(request) -> HttpResponse:
    """Enter info for a round in a chess tournament, create the round model

    Arguments
    ---------
    request : HttpRequest
    """

    logger.debug("Create.round entered with request: %s", request)
    # round we are building
    cur_round = session.get_tournament_round_number()
    # create Round model in dadabase
    new_round = Round(round_num=cur_round, tournament=session.get_tournament())
    new_round.save()
    logger.debug("new round created. Round: %s", new_round)

    context = {
        "entered_matches": session.get_matches(),
        "round_number": cur_round,
        "rounds": session.get_rounds(),
    }
    return render(request, "cfc_report/create/round.html", context)


def confirm_round(request) -> HttpResponse:
    """Confirm a round for submission. If confirmed, finalize the round,
    else return to edditing it

    Arguments
    ---------
    request : HttpRequest
    """

    tournament_info = session.get_tournament_info()
    context = {
        "tournament_name": tournament_info["name"],
        "round_number": session.get_tournament_round_number(),
        # HACK: FIXME figgure out db sessions
        "matches": db.get_matches(),
        "players": db.get_players(),
    }
    logger.debug(
        "Create.confirm_round entered, confirming round completion.\n \
         TournamentInfo: %s \n context: %s \n",
        tournament_info,
        context,
    )

    return render(request, "cfc_report/create/confirm-round.html", context)
