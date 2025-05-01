"""Data model for a CFC rated tournament roster of Players"""
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

from django.db import models

from cfc_report.models.tournament import Tournament


class Roster(models.Model):
    """A roster of players in a CFC-rated tournament

    Attributes
    ----------
    tournament : OneToOneField
        the tournament this roster is for
    """

    tournament = models.OneToOneField(
        Tournament,
        on_delete=models.CASCADE,
        related_name='roster'
    )
    players = models.ManyToManyField("Player")
