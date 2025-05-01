"""Data model for a CFC rated tournament chess match"""
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

from .fields import CfcIdField
from .round import Round


class Match(models.Model):
    """A CFC-rated chess match

    Attributes
    ----------
    white : Player
        the White player in the match
    black : Player
        the black player in the match
    result : CharField
        KEY: (b == black victory, w == white victory, d == no victory)
    round : ForeignKey
        The round of the tournament this game is for
    """
    RESULT_BLACK = "B"
    RESULT_WHITE = "W"
    RESULT_DRAW = "D"
    RESULT_UNKNOWN = "_"

    RESULT_CHOICES = {RESULT_BLACK: "0 - 1",
                      RESULT_WHITE: "1 - 0",
                      RESULT_DRAW: "0.5 - 0.5",
                      RESULT_UNKNOWN: "NOT SURE"}

    white = CfcIdField()
    black = CfcIdField()

    result = models.CharField(
        max_length=1, choices=RESULT_CHOICES, default=RESULT_UNKNOWN
    )
    round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        related_name="tournament_round",
    )

    def get_absolute_url(self):
        return reverse("select-match-round", kwargs={"pk": self.pk})

    def __str__(self):
        return (
            f"MATCH - "
            f" white: ({self.white}),"
            f" black: ({self.black}),"
            f" result: ({self.result}),"
        )
