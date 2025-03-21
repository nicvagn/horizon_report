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
from django.forms import SelectDateWidget

from .. import logger
from .fields import CfcIdField, PairingSystemField, ProvinceField


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

    name = forms.CharField(required=True, label="Tournament Name", initial="Test Open", max_length=60)
    num_rounds = forms.IntegerField(required=True, label="Number of Rounds", initial=1)
    date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],)
    pairing_system = PairingSystemField(required=True, label="Pairing system used")
    province = ProvinceField(required=True)
    # TournamentOrganizer CFC id
    to_cfc = CfcIdField(required=True, label="Tournament Organizer CFC id", initial="000000")
    # TournamentDirector CFC id
    td_cfc = CfcIdField(required=True, label="Tournament Director CFC id", initial="000000")


class RoundForm(forms.Form):
    """for getting information on a round in a chess tournament
    TODO
    """

    # TODO: make so you can enter match info and create matches for the round


class MatchForm(forms.Form):
    """A form for entering the data for a single Match
    TODO
    """

    white = CfcIdField()
    black = CfcIdField()
    winner = CfcIdField()
