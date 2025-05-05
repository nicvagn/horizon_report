"""Data model for a CFC rated tournament"""
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

from .fields import PairingSystemField, ProvinceField, CfcIdField
from .. import logger


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

    name = models.CharField(
        help_text="Name of the tournament.",
        max_length=60,
        default="the tournament"
    )
    num_rounds = models.IntegerField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    rating_type = models.CharField(max_length=1, null=True)
    pairing_system = PairingSystemField()
    province = ProvinceField()

    to_cfc = CfcIdField(null=True)
    td_cfc = CfcIdField(null=True)

    slug = models.SlugField(null=True, unique=True)

    def _generate_slug(self):
        """Generate a slug using the tournament name and start date."""

        slug = self.SLUG_FORMAT.format(
            name=self.tournament_name,
            date=self.start_date,
        )

        t = Tournament.objects.filter(start_date=self.start_date)
        # if a tournament exists with that slug, make slug unique by getting all
        # tournaments with that start date, and adding that number +1 to slug
        if t:
            slug = f"{slug}-{t.count()}"

        logger.info("tournament Slug generated: %s", slug)

        return slug

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
