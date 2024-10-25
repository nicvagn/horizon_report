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
import logging
from typing import TypedDict
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from .constants import LOGGER_NAME
logger = logging.getLogger(LOGGER_NAME)


class SerializedPlayer(TypedDict):
    """A serialized Player ready to be JSON
    Attributes
    ----------
    name : str
        Player's name
    cfc_id : str
        Player's cfc_id, CFC id's must be 6 numbers, ie: 222333
    """
    name: str
    cfc_id: str


class CfcIdField(models.IntegerField):
    """A CFC ID field
    Attributes
    ----------
    validators :
        int in field x must be x where 1000000 > x > 99999
    """
    validators = [MinValueValidator(100000), MaxValueValidator(999999)]

    def __str__(self):
        return str(super())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PairingSystem(models.CharField):
    """A tournament pairing system for a chess tournament
    Attributes
    ----------
    PAIRING_SYSTEM : dict{str:str}
        Pairing system for the tournament
    """
    PAIRING_SYSTEMS = {
        "SW": "Swiss",
        "RR": "round robin",
        "DR": "double round robin",
    }

    def __init__(self, *args, **kwargs):
        # Set the max length of field two be 2 chars
        kwargs["max_length"] = 2
        kwargs["choices"] = PairingSystem.PAIRING_SYSTEMS

        super().__init__(*args, **kwargs)


class Province(models.CharField):
    """A canadian province field

    Attributes
    ----------
    PROVINCES : dict[str : str]
        province acronym key to province name
    PROVINCES{key} : str
        The key to the PROVINCES dict
        must be:
            max_length: 2
            must be in form 'SK'
    """
    PROVINCES = {
        "ON": "Ontario",
        "QC": "Quebec",
        "NS": "Nova Scotia",
        "NB": "New Brunswick",
        "MB": "Manitoba",
        "BC": "British Columbia",
        "PE": "Prince Edward Island",
        "SK": "Saskatchewan",
        "AB": "Alberta",
        "NL": "Newfoundland and Labrador",
    }

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 2
        kwargs["choices"] = self.PROVINCES
        super().__init__(*args, **kwargs)


# models relating to a CFC Rated chess tournament.

class Player(models.Model):
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
    serialize(self)
        create a serialized version of this Player
    decode(cls) : Player
        classmethod to decode a serialized player into a python object
    """
    name = models.CharField(max_length=20)
    cfc_id = CfcIdField()
    slug = models.SlugField(default="", null=False)
    # make sure slug exists for every player

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
            "Player: (%s) saved and slug (%s) created for it", self, self.slug)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """get the absolute url of this model

        Returns
        -------
        The absolute url to access this player
        """
        return reverse("player", args=[self.slug])

    def serialize(self) -> SerializedPlayer:
        """Make a SerializedPlayer typed dict from this Player

        Returns
        -------
        A dict containing all the information to recreate this player.
        """
        sp: SerializedPlayer = {"name":
                                self.name, "cfc_id": self.cfc_id}
        return sp

    def __str__(self):
        return f"Player: {self.name} CFC: {self.cfc_id}"

    @staticmethod
    def decode(sp: SerializedPlayer):
        """Decode a SerializedPlayer into a Player object

        Parameters
        ----------
        sp : SerializedPlayer
            the SerializedPlayer TypedDict to decode player from

        Returns
        -------
        decoded player : Player
            The decoded Player object
        """
        return Player(name=sp["name"], cfc_id=sp["cfc_id"])


class Roster(models.Model):
    """A roster of players in a cfc rated tournament

    Attributes
    ----------
    players : ForeignKey
        players in roster

    Methods
    _______
    size : int
        number of players in this roster
    """

    players = models.ForeignKey(Player, on_delete=models.CASCADE)

    def size(self):
        """Number of Player ie: size of this roster"""
        raise NotImplementedError


class TournamentDirector(Player):
    """A tournament director for a cfc chess tournament.

    Attributes
    ----------
    name : models.CharField
        name of TournamentDirector
    cfc_id : CfcIdField
        CFC ID of TournamentDirector
    """

    def __str__(self):
        return f"Tournament Director: {self.name}, CFC: {self.cfc_id}"


class TournamentOrganizer(Player):
    """A tournament organizer for a cfc chess tournament.

    Attributes
    ----------
    name: models.CharField
        name of TournamentOrganizer
    cfc_id: CfcIdField
        CFC ID of TournamentOrganizer
    """

    def __str__(self):
        return f"Tournament Organizer: {self.name}, CFC: {self.cfc_id}"


class Match(models.Model):
    """A cfc rated chess match

    Attributes
    ----------
    white : Player
        the White player in the match
    black : Player
        the black player in the match
    winner:
        Player if winner, False if draw
    """

    white = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="white_player")
    black = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="black_player")
    winner = models.ForeignKey(
        Player, default=None, on_delete=models.CASCADE, related_name="winning_player")


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
    to_cfc : CfcIdField
        The CFC ID of the TournamentOrganizer
    td_cfc : CfcIdField
        The CFC ID of the TournamentDirector

    Methods
    -------
    add_player(player)
        add a player to the tournament
    """

    def __init__(self):
        super().__init__()
        # start tournament with no players
        self.players = []

    name = models.CharField(max_length=30)
    num_rounds = models.IntegerField()
    date = models.DateField()
    pairing_system = PairingSystem()
    province = Province()
    to_cfc = CfcIdField()  # TournamentOrganizer CFC id
    td_cfc = CfcIdField()  # TournamentDirector CFC id

    def add_player(self, player: Player):
        """Choose a player to be in created tournament

        Arguments
        ---------
        player : Player
            Chosen player

        Returns
        -------
            None
        """
        raise NotImplementedError

    def __str__(self):
        return f"""Tournament name: {self.name}
        Number of rounds: {self.num_rounds}
        date: {self.date}
        Pairing System: {self.pairing_system}
        province: {self.province}
        TournamentOrganizer CFC: {self.to_cfc}
        TournamentDirector CFC: {self.td_cfc}
        """


class Report(models.Model):
    """A CFC Report for a tournament

    Attributes
    ----------
    tournament : Tournament
        The Tournament this report is for

    Methods
    -------

    """
    tournament = Tournament()

    def __str__(self):
        return f"tournament: {self.tournament}"
