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

from cfc_report import logger
from cfc_report.models import Round


def create_round(tournament, round_number):
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
