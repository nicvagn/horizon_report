"""Django views"""
# horizon_pair
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

from django.shortcuts import render, reverse

from . import models

players = [
    models.Player(name="NicOlass Vhhhhd", cfc_id="444444"),
    models.Player(name="NicOlass Vhhhhd", cfc_id="444444"),
    models.Player(name="NicOlass Vhhhhd", cfc_id="444444"),
    models.Player(name="NicOlass Vhhhhd", cfc_id="444444"),
]

TO = models.TournamentOrganizer(name="Vlad the Impailer", cfc_id="123123")
TD = models.TournamentDirector(name="Jonny Boy", cfc_id="4443434")


def view_report(request):
    """display a CFC report"""
    player_list = []
    for p in players:
        player_list.append(str(p.name))
    num_players = len(player_list)
    context = {
        "title": "The Masters",
        "province": "SK",
        "time_format": "blitz",
        "TD_cfc": TD.cfc_id,
        "TO_cfc": TO.cfc_id,
        "tournament_date": "9/11",
        "players": player_list,
        "num_players": num_players,
    }
    return render(request, "report/view_report.html", context)


def create_report(request):
    """create a report for the cfc"""
    context = {"players": ["11111", "222222", "333333", "44444"]}
    return render(request, "report/create_report.html", context)
