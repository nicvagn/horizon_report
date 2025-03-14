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

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from . import logger
from .model_fields import CfcIdField, PairingSystemField, ProvinceField

# models relating to a CFC Rated chess tournament.


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
    cfc_id = CfcIdField()
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

    def jsonify(self) -> "JSON":
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
    def decode(json_player: "JSON"):
        """Decode a jsonified into a Player object

        Parameters
        ----------
        sp : "JSON"
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
    decode(json_td: "JSON")
    """

    def __str__(self):
        return f"Tournament Director: {self.name}, CFC: {self.cfc_id}"

    @staticmethod
    def decode(json_td: "JSON"):
        """Decode a jsonified into a Player object

        Parameters
        ----------
        json_td : "JSON"
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
    def decode(json_to: "JSON"):
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
    round_number : Int
        What round of the tournament this game is for
    """

    RESULT_CHOICES = [("b", "0 - 1"), ("w", "1 - 0"),
                      ("d", "0.5 - 0.5"), ("_", "_")]

    white = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="white_player"
    )
    black = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="black_player"
    )
    result = models.CharField(
        max_length=1, choices=RESULT_CHOICES, default=RESULT_CHOICES[3]
    )
    round_number = models.IntegerField()

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

    name = models.CharField(help_text="Tournament Name.", primary_key=True,
                            max_length=40)
    num_rounds = models.IntegerField()
    roster = models.ForeignKey(
        Roster,
        on_delete=models.CASCADE,
        related_name="tournament_roster",
        default=False,
    )
    rounds = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        related_name="rounds_in_tournament",
        default=False,
    )

    date = models.DateField()
    pairing_system = PairingSystemField()
    province = ProvinceField()
    to_cfc = CfcIdField()  # TournamentOrganizer CFC id
    td_cfc = CfcIdField()  # TournamentDirector CFC id

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
    ctr : CTR
        A wrapper class around the cfc ctr file
    tms : TMS
        A wraper class around the cfd tms file
    Methods
    -------

    """

    tournament = Tournament()
    ctr = None
    tms = None

    def __str__(self):
        return f"tournament: {self.tournament}"
