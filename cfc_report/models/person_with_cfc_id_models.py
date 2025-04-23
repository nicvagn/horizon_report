"""People with CfcId models."""
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
from django.urls import reverse
from django.utils.text import slugify

from .fields import CfcIdField
from .tournament import Tournament
from .. import logger


class PersonWithCfcId(models.Model):
    """A Person with a CFC id, associated with tournaments."""
    name = models.CharField(max_length=40)
    cfc_id = CfcIdField()
    tournaments = models.ManyToManyField(Tournament)
    slug = models.SlugField(default="", unique=True, null=False)

    def save(self, *args, **kwargs):
        """Creates slug URL before saving the object."""
        self.slug = self._generate_slug()
        logger.info(
            "PersonWithCfcId: (%s) saved and slug (%s) created for it",
            self,
            self.slug
        )
        super().save(*args, **kwargs)

    def _generate_slug(self) -> str:
        """Helper method to generate slug based on name and cfc_id."""
        return slugify(f"{self.name}-{self.cfc_id}")

    def get_absolute_url(self):
        """Returns the absolute URL to access this person."""
        return reverse("player", args=[self.slug])

    @classmethod
    def create(cls, name: str, cfc_id: int) -> "PersonWithCfcId":
        """
        Factory method to create a new instance of PersonWithCfcId.
        """
        return cls(name=name, cfc_id=cfc_id)


class Player(PersonWithCfcId):
    """A chess player with a CFC id."""

    def __str__(self):
        return f"{self.name} CFC: {self.cfc_id}"


class TournamentDirector(PersonWithCfcId):
    """A tournament director for a CFC chess tournament."""

    def __str__(self):
        return f"Tournament Director: {self.name}, CFC: {self.cfc_id}"


class TournamentOrganizer(PersonWithCfcId):
    """A tournament organizer for a CFC chess tournament."""

    def __str__(self):
        return f"Tournament Organizer: {self.name}, CFC: {self.cfc_id}"
