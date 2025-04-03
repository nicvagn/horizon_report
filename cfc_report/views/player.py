"""views for cfc_report players"""
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

from .. import logger
from ..models.person_with_cfc_id_models import Player


def add_player(request):
    """view to add player to tournament players database
    Notes
    -----
    Side effects:
        modifies the database via services.db.add_player

    Parameters
    ----------
    request : HttpRequest
    """
    logger.debug("add_player entered with request %s", request)
    # if is the form being submitted
    if request.method == "POST":
        query_dict = request.POST
        logger.debug("POST request with value: %s", query_dict)

        player: Player = Player.create(
            query_dict["player_name"], query_dict["player_cfc_id"])
        logger.debug("Player %s made.", player)
        # add player to db
        player.save()
        logger.debug("Made Player added to database")

    # render the requested page.
    return render(request, "cfc_report/create/player.html",
                  {"method": request.method})
