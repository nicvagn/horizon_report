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

from django.shortcuts import render

from cfc_report.models import (Match, Round, )
from . import logger


def chess_match(request):
    """Enter information about a chess match
    Arguments
    ---------
    request : HttpRequest
        if POST a request containing a chess match
    """

    # The form for creating matches is in match-form.html
    logger.debug("Create.match.chess_match entered with request: %s", request)
    # if is the form being submitted
    if request.method == "POST":
        match_info = request.POST
        logger.debug("chess_match: POST request with value: %s", match_info)
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
        black = match_info["black"]
        white = match_info["white"]
        logger.debug("CFC ids(black: %s, white: %s)", black, white)
        rnd = Round.objects.get(pk=request.session["round_pk"])
        # create the chess match model and save it to the db
        match = Match(white=white, black=black, result=result,
                      round=rnd)
        logger.debug(
            "chess_match entered and saved: black_id %s, white_id: %s, \
            result: %s, round: %s",
            black,
            white,
            result,
            rnd
        )
        match.save()

    # Continue letting user add more games
    context = {
        "tournament_players": get_session_players(request),
        "round_number": request.session["round_number"],
        "entered_matches": get_session_matches(request),
    }

    return render(request, "cfc_report/create/match-form.html", context)
