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
# set up logging
import json

from django import forms
from django.forms import SelectDateWidget, ChoiceField

from . import logger
from .constants import LOGGER_NAME
from .form_fields import CfcIdField, PairingSystemField, ProvinceField
from .models import Match
from .services import session

class TournamentInfoForm(forms.Form):
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

    name = forms.CharField(label="Tournament Name",
                           initial="test data", max_length=60)
    num_rounds = forms.IntegerField(label="Number of Rounds", initial=0)
    date = forms.DateField(widget=SelectDateWidget)
    pairing_system = PairingSystemField(label="Pairing system used")
    province = ProvinceField()
    # TournamentOrganizer CFC id
    to_cfc = CfcIdField(label="Tournament Organizer CFC id", initial="000000")
    # TournamentDirector CFC id
    td_cfc = CfcIdField(label="Tournament Director CFC id", initial="000000")

    def jsonify(self) -> str:
        """Create string JSON representation of form

        Returns
        -------
        The JSON string with all the form information in it
        """
        try:
            j = json.dumps({"name": self.name,
                            "num_rounds": self.num_rounds,
                            "date": str(self.date),
                            "pairing_system": str(self.pairing_system),
                            "province": str(self.province),
                            # TournamentOrganizer CFC id
                            "to_cfc": str(self.to_cfc),
                            # TournamentDirector CFC id
                            "td_cfc": str(self.td_cfc),
                            })
        except AttributeError as err:
            logger.warning("Failure to jasonify %s", self)
            raise err

        logger.debug(
            "json created: \n %s", j)
        return j


class RoundForm(forms.Form):
    """for getting information on a round in a chess tournament
    TODO
    """



   

    # TODO: make so you can enter match info and create matches for the round


class MatchForm(forms.Form):
    """A form for entering the data for a single Match
    TODO
    """

    session_players = session.get_players()

    white = ChoiceField(choices=session_players)
    black = ChoiceField(choices=session_players)
    winner = ChoiceField(choices=session_players)
