"""forms.py: Forms for CFC rated tournament"""
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
from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms
from .constants import LOGGER_NAME
logger = logging.getLogger(LOGGER_NAME)

# defining fields


class CfcIdField(forms.IntegerField):
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


class PairingSystem(forms.CharField):
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


class Province(forms.CharField):
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


class TournamentForm(forms.Form):
    """for getting info on a CFC rated tournament

    Attributes
    ----------
    name : forms.CharField
        name of the tournament
    num_rounds : forms.IntegerField
        number of rounds
    date : forms.DateField
        The date of the tournament
    pairing_system : PairingSystem
        The pairing system used in this tournament.
    province : Province
        The canadian province this tournament was held
    to_cfc : CfcIdField
        The CFC ID of the TournamentOrganizer
    td_cfc : CfcIdField
        The CFC ID of the TournamentDirector

    """

    name = forms.CharField(max_length=30)
    num_rounds = forms.IntegerField()
    date = forms.DateField()
    pairing_system = PairingSystem()
    province = Province()
    to_cfc = CfcIdField()  # TournamentOrganizer CFC id
    td_cfc = CfcIdField()  # TournamentDirector CFC id

    def add_player(self, player: "Player"):
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
