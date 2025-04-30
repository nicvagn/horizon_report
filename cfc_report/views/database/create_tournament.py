"""views for creating tournament models and adding to the database"""
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

from django.shortcuts import redirect

from cfc_report.models.tournament import Tournament, Round
from . import logger


def tournament_initial(request):
    """Create database models from TournamentReportInfoFormView info"""

    info = request.session["tournament_info"]
    tournament = Tournament(
        tournament_name=info["name"],
        num_rounds=info["num_rounds"],
        start_date=info["start_date"],
        end_date=info["end_date"],
        pairing_system=info["pairing_system"],
        province=info["province"], )

    tournament.save()

    logger.info("report.initial: info: %s", info)

    request.session["tournament_id"] = tournament.pk

    # create a model for the first round
    round1 = Round(tournament=tournament, round_num=1)
    round1.save()
    request.session["round_pk_list"] = [round1.pk]

    logger.info("report.initial: round with pk %s saved. session['round_pk'] set to pk", round1.pk)
    return redirect("report-tournament-players")
