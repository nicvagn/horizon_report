"""general overview view for creating a Report for a CFC Rated tournament."""
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

from django.shortcuts import render
from django.views import View

from cfc_report.models.tournament import Tournament, Round
from . import logger


class CreateReportView(View):
    """general Report overview for the report in construction."""

    template_name = "cfc_report/create/report.html"

    def get(self, request, *args, **kwargs):
        """Handle GET request for report overview.

        Args:
            request: The HTTP request
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Rendered template with tournament and rounds context
        """
        t_id = request.session["tournament_id"]
        t_info = request.session["tournament_info"]
        tournament = Tournament.objects.get(pk=t_id)
        # Get players from the tournament roster
        players = tournament.roster.players.all()
        # Fetch the tournament's built rounds
        rounds = Round.objects.filter(tournament=tournament).order_by('round_num')

        logger.info("CreateReportView.get w tournament: %s rounds: %s players: %s"
                    % (tournament, rounds, players))

        context = {
            "tournament_name": t_info["name"],
            "rounds": rounds,
            "players": players
        }
        return render(request, self.template_name, context)
