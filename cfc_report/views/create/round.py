"""Create a round in a report for a CFC Rated tournament."""
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

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from cfc_report.forms import RoundForm
from cfc_report.models import Round, Tournament, Match
from cfc_report.utils.session_utils import get_session_players
from . import logger


def _create_round(tournament, round_number):
    """Helper: Create a new round associated with a tournament.

    Parameters
    ----------
    tournament : Tournament
        The tournament to which the round belongs.
    round_number : int
        The number of the round.

    Returns
    -------
    Round
        The created Round instance.
    """
    round_instance = Round(tournament=tournament, number=round_number)
    round_instance.save()
    logger.info("Created Round #%d for tournament: %s", round_number, tournament)
    return round_instance


def create_round_view(request: HttpRequest, round_num=None) -> HttpResponse:
    """Create a round interactively

    Notes
    -----
    Gets matches for the current tournament from the session.

    Parameters
    ----------
    request : HttpRequest
        http request from the view, used to get the session
    round_num : int
        Number of the round to create.
    """

    logger.debug(
        "create_round_view entered with request.session: %s and  round_num: %s",
        request.session,
        round_num,
    )

    # If GET request, display an empty form
    form = RoundForm()

    t_id = request.session.get("tournament_id")
    matches = Match.objects.filter(
        round__tournament_id=t_id) if t_id else []

    players = get_session_players(request)

    context = {"form": form, "round_number": request.session.get("round_number"),
               "matches": matches, "players": players}
    return render(request, "cfc_report/create/round.html", context)
