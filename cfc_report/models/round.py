"""Data models related to putting on a CFC rated tournament"""
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

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .Tournament import Tournament


class Round(models.Model):
    """A Round in a CFC-rated tournament

    Attributes
    ----------
    round_num : IntegerField
        the round of its tournament this is
    """

    round_num = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)]
    )

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
