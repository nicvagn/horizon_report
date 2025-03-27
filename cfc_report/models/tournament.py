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
from django.urls import reverse
from django.utils.text import slugify

from .fields import CfcIdField, PairingSystemField, ProvinceField
from .person import Player, TournamentDirector, TournamentOrganizer

"""models relating to a CFC Rated chess tournament."""


class Tournament(models.Model):
    """A cfc rated chess tournament

    Attributes
    ----------
    name : models.CharField
        name of the tournament
    num_rounds : models.IntegerField
        number of rounds
    date : models.DateField
        The date of the tournament
    pairing_system : PairingSystem
        The pairing system used in this tournament.
    province : Province
        The canadian province this tournament was held
    tournament_organizer : TournamentOrganizer
        The TournamentOrganizer of the tournament
    tournament_director : TournamentDirector
        The TournamentDirector of the tournament
    """

    name = models.CharField(help_text="Tournament Name.", primary_key=False,
                            max_length=40)
    num_rounds = models.IntegerField()

    date = models.DateField()
    pairing_system = PairingSystemField()
    province = ProvinceField()

    tournament_director = models.OneToOneField(TournamentDirector,
                                               on_delete=models.CASCADE,
                                               related_name="TD")

    tournament_organizer = models.OneToOneField(TournamentOrganizer,
                                                on_delete=models.CASCADE,
                                                related_name="TO")

    def __str__(self):
        return f"""Tournament name: {self.name}
        Number of rounds: {self.num_rounds}
        date: {self.date}
        Pairing System: {self.pairing_system}
        province: {self.province}
        """


class Round(models.Model):
    """A Round in a cfc rated tournament

    Attributes
    ----------
    round_num : IntegerField
        the round of it's tournament this is
    """

    round_num = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)]
    )

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)


class Roster(models.Model):
    """A roster of players in a cfc rated tournament

    Attributes
    ----------
    players : ForeignKey
        players in roster

    """

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)


class Match(models.Model):
    """A cfc rated chess match

    Attributes
    ----------
    white : Player
        the White player in the match
    black : Player
        the black player in the match
    result : CharField
        KEY: (b == black victory, w == white victory, d == no victory)
    round : ForignKey
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

    white = models.OneToOneField(
        Player, on_delete=models.CASCADE, related_name="white_player"
    )
    black = models.OneToOneField(
        Player, on_delete=models.CASCADE, related_name="black_player"
    )
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
            f"MATCH - [ "
            f" white: ({self.white}),"
            f" black: ({self.black}),"
            f" result: ({self.result}),"
            f" round number: ({self.round_number}) ]"
        )
