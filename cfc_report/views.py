"views for cfc_report" ""
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
import logging
from django.shortcuts import render
from .models import Player, TournamentDirector, TournamentOrganizer
from .services import database as db
from .services.player import create_player
# db functions get_TDs, get_TOs, get_players, add_player

# set up logger
logger = logging.getLogger(__name__)

# TODO: rm
reports = [{
    "name": "report1",
    "url": "report url"
}, {
    "name": "report2",
    "url": "report2 url"
}]


def index(request):
    """Main index page"""
    player_list = db.get_players()
    return render(
        request, "home/index.html", {
            "reports": reports,
            "players": player_list,
            "players_heading": "Player's in Database",
        })


def create_report(request):
    """show view to create a report for the cfc"""
    logger.debug("create_report entered with request: %s", request)
    # if is the form being submitted
    if request.method == "POST":
        query_dict = request.POST
        logger.debug("POST request with value: %s", query_dict)

        # create tournament report

    players = db.get_players()
    context = {"database_players": db.get_players()}
    return render(request, "create/index.html", context)


def view_report(request):
    """display a CFC report"""

    logger.debug("view_report entered with request: %s", request)
    # FIXME:
    TO, _ = TournamentOrganizer.objects.get_or_create(name="Base TO",
                                                      cfc_id=111111)
    TD, _ = TournamentDirector.objects.get_or_create(name="Base TD",
                                                     cfc_id=222222)

    player_list = db.get_players()
    num_players = player_list.count()
    context = {
        "title": "The Masters",
        "province": "SK",
        "time_format": "blitz",
        "TD_cfc": TD.cfc_id,
        "TO_cfc": TO.cfc_id,
        "tournament_date": "06/06/87",
        "players": player_list,
        "num_players": num_players,
    }
    return render(request, "show/index.html", context)


def add_player(request):
    """view to add player to tournament players database"""
    logger.debug("add_player entered with request %s", request)
    # if is the form being submitted
    if request.method == "POST":
        query_dict = request.POST
        logger.debug("POST request with value: %s", query_dict)

        player: Player = create_player(query_dict["player_name"],
                                       query_dict["player_cfc_id"])
        logger.debug("Player %s made.", player)
        # add player to db
        db.add_player(player)
        logger.debug("Made Player added to database")

    # render the requested page.
    return render(request, "add_player/index.html", {"method": request.method})
