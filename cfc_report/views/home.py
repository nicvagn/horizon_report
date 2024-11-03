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
from .. import logger

from django.shortcuts import render

from ..constants import LOGGER_NAME
from ..models import Player
from ..services import database as db


def index(request):
    """Main index page"""
    player_list = db.get_players()

    request.session["players"] = [
        Player.jsonify(Player(name="Joe Blow", cfc_id="989898")),
        Player.jsonify(Player(name="Lo Blow", cfc_id="184494"))
    ]

    return render(
        request, "cfc_report/home/index.html", {
            "reports": {},
            "players": player_list,
            "players_heading": "Player's in Database",
        })
