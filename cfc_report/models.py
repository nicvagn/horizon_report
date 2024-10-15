"""Data models for CFC rated tournament"""
# horizon_pair
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

# models relating to a CFC Rated chess tournament.


class CfcId(models.IntegerField):
    """A CFC ID field"""
    validators = [MinValueValidator(100000), MaxValueValidator(999999)]


class Player(models.Model):
    """A chess player with a CFC id"""
    name = models.CharField(max_length=20)
    cfc_id = CfcId()

    def __str__(self):
        return f"Player: {self.name} CFC: {self.cfc_id}"


class TournamentDirector(models.Model):
    """A tournament director for a cfc chess tournament."""
    name = models.CharField(max_length=20)
    cfc_id = CfcId()

    def __str__(self):
        return f"Tournament Director: {self.name}, CFC: {self.cfc_id}"


class TournamentOrganizer(models.Model):
    """A tournament director for a cfc chess tournament."""
    name = models.CharField(max_length=20)
    cfc_id = CfcId()

    def __str__(self):
        return f"Tournament Organizer: {self.name}, CFC: {self.cfc_id}"


class Tournament(models.Model):
    """A cfc rated chess tournament"""
    name = models.CharField(max_length=30)
    num_rounds = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"""Tournament name: { self.name }
        Number of rounds: { self.num_rounds }
        date: {self.date}"""
