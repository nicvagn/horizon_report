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

from .fields import CfcIdField, PairingSystemField, ProvinceField
from .. import logger

"""models relating to a CFC Rated chess tournament."""


class Tournament(models.Model):
    """A CFC-rated chess tournament.

    Attributes
    ----------
    tournament_name : models.CharField
        The name of the tournament.
    num_rounds : models.IntegerField
        The number of rounds in the tournament.
    start_date : models.DateField
        The date the tournament was started.
    end_date : models.DateField
        The date the tournament was ended.
    pairing_system : PairingSystem
        The pairing system used in this tournament.
    province : Province
        The Canadian province where this tournament was held.
    slug : models.SlugField
        A unique slug for the tournament.
    """

    SLUG_FORMAT = "{name}|{date}"

    tournament_name = models.CharField(
        help_text="Name of the tournament.",
        max_length=60
    )
    num_rounds = models.IntegerField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    pairing_system = PairingSystemField()
    province = ProvinceField()
    slug = models.SlugField(null=True, unique=True)

    def _generate_slug(self):
        """Generate a slug using the tournament name and start date."""

        slug = self.SLUG_FORMAT.format(
            name=self.tournament_name,
            date=self.start_date,
        )

        t = Tournament.objects.filter(slug=slug)
        # if a tournament exists with that slug, make slug unique
        if t:
            slug = f"{slug}-{t.count()}"

        logger.info("tournament Slug generated: %s", slug)

    def save(self, *args, **kwargs):
        """create slug url before saving
        Override of save()

        Arguments
        ---------
        *args and **kwargs - passed on to super().save(...)

        Returns
        -------
        None
        """
        if not self.slug:
            self.slug = self._generate_slug()
        logger.info(
            "Tournament (%s) saved with slug (%s)",
            self,
            self.slug
        )
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the absolute URL for the tournament."""
        return f"/tournaments/{self.slug}/"

    def __str__(self):
        """String representation of the Tournament."""
        return self.tournament_name


class Round(models.Model):
    """A Round in a cfc rated tournament

    Attributes
    ----------
    round_num : IntegerField
        the round of its tournament this is
    """

    round_num = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)]
    )

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)


class Roster(models.Model):
    """A roster of players in a cfc rated tournament

    Attributes
    ----------
    tournament : OneToOneField
        the tournament this roster is for
    """

    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE)


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
