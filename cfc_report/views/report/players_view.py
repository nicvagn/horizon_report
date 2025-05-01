"""view for selecting players in a Report for a CFC Rated tournament."""
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
from django.shortcuts import render, redirect
from django.views import View

from cfc_report.models.player import Player


class TournamentPlayersView(View):
    """view for selecting players in a Report for a CFC Rated tournament."""

    template_name = "cfc_report/create/tournament-players.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET request - display available players."""
        players = Player.objects.all()
        return render(request, self.template_name, {'players': players})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle POST request - process selected players."""
        selected_players = request.POST.getlist('selected_players')
        if not selected_players:
            return render(request, self.template_name, {
                'error': 'Please select at least one player'
            })

        request.session['players'] = selected_players
        return redirect('report-create-round')
