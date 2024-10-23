"""views for cfc_report index"""
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
import logging
from django.shortcuts import render
from django.http.response import HttpResponse
from ..constants import LOGGER_NAME
from ..models import Player, TournamentDirector, TournamentOrganizer
from ..forms import TournamentForm
from ..services import database as db, session, player as player_services
# set up logger
# get the logger for cfc_report module. Should be set up.
logger = logging.getLogger(LOGGER_NAME)


def index(request):
    """Main index page"""
    player_list = db.get_players()

    request.session["tournament_players"] = [Player.serialize(Player(name="Joe Blow",
                                                                     cfc_id="989898")),
                                             Player.serialize(Player(name="Lo Blow",
                                                                     cfc_id="184494"))]

    return render(
        request, "cfc_report/home/index.html", {
            "reports": {},
            "players": player_list,
            "players_heading": "Player's in Database",
        })