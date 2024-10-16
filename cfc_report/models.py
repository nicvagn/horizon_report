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

# custom fields


class CfcId(models.IntegerField):
    """A CFC ID field
    validators :
        must be x where 1000000 > x > 99999
    """
    validators = [MinValueValidator(100000), MaxValueValidator(999999)]

    def __init__(self):
        super().__init__()


class PairingSystem(models.CharField):
    """A tournament pairing system for a chess tournament"""
    PAIRING_SYSTEMS = {
        "SW": "swiss",
        "RR": "round robin",
        "DR": "double round robin"
    }

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 2
        # assert args[0] in self.PAIRING_SYSTEMS.keys()
        super().__init__(*args, **kwargs)


class Province(models.CharField):
    """A canadian province field
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
        # assert len(args) == 1
        # assert args[0] in self.PROVINCES.keys()
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
    """
    name = models.CharField(max_length=20)
    cfc_id = CfcId()

    def __str__(self):
        return f"Player: {self.name} CFC: {self.cfc_id}"


class Roster(models.Model):
    """A roster of players in a cfc rated tournament

    Attributes
    ----------
    players : list(Player)
        players in roster
    size : int
        number of players in this roster
    """
    players = []


class TournamentDirector(models.Model):
    """A tournament director for a cfc chess tournament.

    Attributes
    ----------
    name : models.CharField
        name of TournamentDirector
    cfc_id : CfcId
        CFC ID of TournamentDirector
    """
    name = models.CharField(max_length=20)
    cfc_id = CfcId()

    def __str__(self):
        return f"Tournament Director: {self.name}, CFC: {self.cfc_id}"


class TournamentOrganizer(models.Model):
    """A tournament organizer for a cfc chess tournament.

    Attributes
    ----------
    name: models.CharField
        name of TournamentOrganizer
    cfc_id: CfcId
        CFC ID of TournamentOrganizer
    """
    name = models.CharField(max_length=20)
    cfc_id = CfcId()

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
        Player if winner, None if draw
    """

    white = Player()
    black = Player()
    winner = Player()


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
    to_cfc : CfcId
        The CFC ID of the TournamentOrganizer
    td_cfc : CfcId
        The CFC ID of the TournamentDirector
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
    to_cfc = CfcId()  # TournamentOrganizer CFC id
    td_cfc = CfcId()  # TournamentDirector CFC id

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
    __________
    tournament : Tournament
        The Tournament this report is for

    Methods
    _______

    """
    tournament = Tournament()
