"""Data models for CFC rated tournament"""

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
import json

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .. import logger
from .fields import CfcIdField

# models relating to a CFC Rated chess tournament.


class CfcId(models.Model):
    """A CFC ID number, a six char number

    Attributes
    ----------
    number : a cfc id number in range 100000 - 999999
    """

    number = CfcIdField()


class PersonWithCfcId(models.Model):
    """A Person with a CFC id

    Attributes
    ----------
    name : models.CharField
        name of the person
    cfc_id : CfCId
        CFC Id of the person
    slug : SlugField
        unique slug for this person url

    Methods
    -------
    save(self)
        save the model in the db with a added slug attribute
        to make url
    serialize(self)
        create a serialized version of this Player
    decode(cls) : Player
        classmethod to decode a serialized player into a python object
    """

    name = models.CharField(max_length=20)
    cfc_id = models.ForeignKey(CfcId, on_delete=models.CASCADE)
    slug = models.SlugField(default="", unique=True, null=False)
    # make sure slug exists for every person

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

        self.slug = slugify(self.name)
        logger.info(
            "PersonWithCfdId: (%s) saved and slug (%s) created for it",
            self,
            self.slug
        )
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """get the absolute url of this model

        Returns
        -------
        The absolute url to access this person
        """
        return reverse("player", args=[self.slug])

    def jsonify(self):
        """Make a JSON Person string from this Person

        Returns
        -------
        A JSON str containing all the information to
        recreate this player.
        """
        jp = json.dumps({"name": self.name, "cfc_id": self.cfc_id})
        logger.debug("JSON Person made: %s", jp)
        return jp


class Player(PersonWithCfcId):
    """A chess player with a CFC id

    Attributes
    ----------
    name : models.CharField
        name of the player
    cfc_id : CfCId
        CFC Id of the player
    slug : SlugField
        unique slug for this players url

    Methods
    -------
    save(self)
        save the model in the db with a added slug attribute
        to make url
    jsonify(self)
        create a serialized JSON version of this Player
    decode(cls) : Player
        classmethod to decode a serialized player into a python object
    """

    def __str__(self):
        return f"Player: {self.name} CFC: {self.cfc_id}"

    @staticmethod
    def decode(json_player):
        """Decode a jsonified into a Player object

        Parameters
        ----------
        sp
            the JSON string to decode player from

        Returns
        -------
        decoded player : Player
            The decoded Player object
        """
        jp = json.loads(json_player)
        logger.debug("decoded %s from %s json", jp, json_player)
        return Player(name=jp["name"], cfc_id=jp["cfc_id"])


class TournamentDirector(PersonWithCfcId):
    """A tournament director for a cfc chess tournament.

    Attributes
    ----------
    name : models.CharField
        name of TournamentDirector
    cfc_id : CfcIdField
        CFC ID of TournamentDirector

    Methods
    -------
    decode(json_td)
    """

    def __str__(self):
        return f"Tournament Director: {self.name}, CFC: {self.cfc_id}"

    @staticmethod
    def decode(json_td):
        """Decode a jsonified into a Player object

        Parameters
        ----------
        json_td
            the JSON string to decode TournamentDirector from

        Returns
        -------
        decoded TournamentDirector : TournamentDirector
            The decoded Player object
        """
        jp = json.loads(json_td)
        logger.debug("decoded %s from %s json", jp, json_td)
        return TournamentDirector(name=jp["name"], cfc_id=jp["cfc_id"])


class TournamentOrganizer(PersonWithCfcId):
    """A tournament organizer for a cfc chess tournament.

    Attributes
    ----------
    name: models.CharField
        name of TournamentOrganizer
    cfc_id: CfcIdField
        CFC ID of TournamentOrganizer

    Methods
    -------
    decode(json_to)
        turn JSON TournamentOrganizer to TournamentOrganizer
    """

    def __str__(self):
        return f"Tournament Organizer: {self.name}, CFC: {self.cfc_id}"

    @staticmethod
    def decode(json_to):
        """Decode a jsonified into a TournamentOrganizer object

        Parameters
        ----------
        sp : "JSON"
            the JSON string to decode TournamentOrganizer from

        Returns
        -------
        decoded to : TournamentOrganizer
            The decoded Player object
        """
        jp = json.loads(json_to)
        logger.debug("decoded %s from %s json", jp, json_to)
        return TournamentDirector(name=jp["name"], cfc_id=jp["cfc_id"])
