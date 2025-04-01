"""view for creating a cfc report"""

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
from django.shortcuts import get_object_or_404, render

from cfc_report import logger
from cfc_report.models import Match, Player, Round
from cfc_report.services import session

def report(request) -> HttpResponse:
    """Create report"""

    tournament_info = session.get_tournament_info()
    context = {
        "tournament_name": tournament_info["name"],
        "round_number": session.get_tournament_round_number(),
        "matches": session.get_matches(),
        "players": session.get_players(),
    }
    return render(request, "cfc_report/create/report.html", context)
