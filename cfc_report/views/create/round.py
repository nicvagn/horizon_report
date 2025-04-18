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

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from cfc_report import logger
from cfc_report.forms import RoundForm
from cfc_report.models import Round, Tournament, Match


def _create_round(tournament, round_number):
    """Create a new round associated with a tournament.

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


def create_round(request):
    """
    Handle the creation of a new round in a tournament.
    """
    logger.info("round.create_round entered, with request: %s", request)
    if request.method == "POST":
        breakpoint()
        form = RoundForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            tournament_id = form.cleaned_data["tournament"]
            round_number = form.cleaned_data["number"]

            # Validate and retrieve the associated tournament
            tournament = get_object_or_404(Tournament, id=tournament_id)

            # Use the helper function to create the round
            new_round = _create_round(tournament, round_number)

            logger.info("Created Round #%d for tournament: %s", round_number, tournament)

            # Redirect to round list or a success page
            return redirect("tournament-detail", pk=tournament.id)
        else:
            # If the form is invalid, return errors
            return render(request, "cfc_report/create/round.html", {"form": form})

    # If GET request, display an empty form
    form = RoundForm()

    context = {"form": form, "round_number": request.session.get("round_number"),
               "matches": Match.objects.all()}
    return render(request, "cfc_report/create/round.html", context)
