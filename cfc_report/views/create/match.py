"""view for creating a cfc report match"""
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

from django.shortcuts import render, get_object_or_404

from cfc_report import logger
from cfc_report.models import (Player, Match, Round, )


def chess_match(request):
    """Enter information about a chess match
    Arguments
    ---------
    request : HttpRequest
        if POST a request containing a chess match
    """

    session = request.session
    breakpoint()
    # The form for creating matches is in match.html
    logger.debug("Create.match entered with request: %s", request)
    # if is the form being submitted
    if request.method == "POST":
        match_info = request.POST
        logger.debug("POST request with value: %s", match_info)
        result = match_info["result"]
        if result == Match.RESULT_CHOICES[Match.RESULT_BLACK]:
            result = Match.RESULT_BLACK
        elif result == Match.RESULT_CHOICES[Match.RESULT_WHITE]:
            result = Match.RESULT_WHITE
        elif result == Match.RESULT_CHOICES[Match.RESULT_DRAW]:
            result = Match.RESULT_DRAW
        else:
            logger.error("Unknown Match Result: %s", result)
            result = Match.RESULT_UNKNOWN

        # get the cfc ids
        black_id = match_info["black"]
        white_id = match_info["white"]
        # get the players
        black = get_object_or_404(Player, cfc_id=black_id)
        white = get_object_or_404(Player, cfc_id=white_id)
        rnd = get_object_or_404(
            Round, round_num=session.get_tournament_round_number())
        # create the chess match model, and save it to the db
        match = Match(white=white, black=black, result=result,
                      round=rnd)
        logger.debug(
            "chess_match entered: black_id %s, white_id: %s, result: %s,  \
            winner: %s",
            black_id,
            white_id,
            result,
        )
        match.save()

    # Continue letting user add more games
    context = {
        "tournament_players": session.get_players(),
        "round_number": session.get_tournament_round_number(),
        "entered_matches": session.get_matches(),
    }

    return render(request, "cfc_report/create/match.html", context)
