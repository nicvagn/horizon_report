"""player models for CFC report builder"""
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

from django.db import models

from .fields import CfcIdField
from .tournament import Tournament
from .. import logger


class Player(models.Model):
    """A player with a CFC id, associated with tournaments. The base model for CFC API.

    Attributes
    ----------
    Identification:
        cfc_id : CfcIdField
            Canadian Federation of Chess ID (primary key)
        fide_id : IntegerField
            International Chess Federation ID
        cfc_expiry : DateField
            Expiration date of CFC membership

    Personal Info:
        name_first : CharField
            Player's first name
        name_last : CharField
            Player's last name
        addr_city : CharField
            City of residence
        addr_province : CharField
            Province of residence (2-letter code)

    Ratings:
        regular_rating : IntegerField
            Standard chess rating
        regular_indicator : IntegerField
            Indicator for regular rating confidence
        quick_rating : IntegerField
            Quick chess rating
        quick_indicator : IntegerField
            Indicator for quick rating confidence

    Relations:
        tournaments : ManyToManyField
            Tournaments this player participated in
        slug : SlugField
            URL-friendly unique identifier

    Notes
    -----
    player is the base model used in the CFC API.
    Players can be both organizers and directors.
    """

    # Identification
    cfc_id: CfcIdField = CfcIdField(primary_key=True)
    fide_id: models.IntegerField = models.IntegerField(default=0)
    cfc_expiry: models.DateField = models.DateField(null=True)

    # Personal Information
    name_first: models.CharField = models.CharField(max_length=40)
    name_last: models.CharField = models.CharField(max_length=40)
    addr_city: models.CharField = models.CharField(max_length=80, null=True)
    addr_province: models.CharField = models.CharField(max_length=2, null=True)

    # Ratings
    regular_rating: models.IntegerField = models.IntegerField(default=0)
    regular_indicator: models.IntegerField = models.IntegerField(default=0)
    quick_rating: models.IntegerField = models.IntegerField(default=0)
    quick_indicator: models.IntegerField = models.IntegerField(null=True)

    # Relations
    tournaments = models.ManyToManyField(Tournament)
    slug: models.SlugField = models.SlugField(default="", unique=True, null=False)

    def save(self, *args, **kwargs):
        """Creates slug URL before saving the object."""
        self.slug = self._generate_slug()
        logger.info(
            "(%s) saved. slug (%s) created for it",
            self,
            self.slug
        )
        super().save(*args, **kwargs)

    def _generate_slug(self) -> str:
        return f"{self.__name__}|{self.cfc_id}"

    def get_absolute_url(self):
        pass

    @classmethod
    def create(cls, name: str, cfc_id: int) -> "Player":
        """
        Factory method to create a new instance of Player.

        Parameters
        ----------
        name : str
            Full name of the player in format "First Last"
        cfc_id : int
            Canadian Federation of Chess ID number

        Returns
        -------
        Player
            New instance of Player with the basic information set

        Raises
        ------
        ValueError
            If the name format is invalid (doesn't contain first and
             last name separated by a space)
        """
        # Split the full name into parts
        name_parts = name.strip().split()
        if len(name_parts) < 2:
            raise ValueError("Name must include both first and last name")

        # Extract first and last name
        name_first = name_parts[0]
        name_last = " ".join(name_parts[1:])  # Join remaining parts as last name

        # Create and return a new player instance
        return cls(
            name_first=name_first,
            name_last=name_last,
            cfc_id=cfc_id,
            regular_rating=0,
            quick_rating=0
        )
