"""tournament_info_form.py: info Form for CFC rated tournament"""
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
# set up logging

import datetime

from django import forms
from django.core.exceptions import ValidationError

from .fields import CfcIdField, PairingSystemField, ProvinceField


class TournamentInfoForm(forms.Form):
    """for getting info on a CFC rated tournament

    Attributes
    ----------
    name : forms.CharField
        name of the tournament
    num_rounds : forms.IntegerField
        number of rounds
    start_date : forms.DateField
        The start date of the tournament
    end_date : forms.DateField
        The start date of the tournament
    pairing_system : PairingSystem
        The pairing system used in this tournament.
    province : Province
        The canadian province this tournament was held
    to_cfc : CfcIdField
        The CFC ID of the TournamentOrganizer
    td_cfc : CfcIdField
        The CFC ID of the TournamentDirector
    """

    name = forms.CharField(
        required=True, label="Tournament Name",
        initial="Test Open", max_length=60)

    def clean_name(self):
        """Validate the tournament name to ensure it meets requirements.
        The name must be at least 2 characters long.
        """
        name = self.cleaned_data['name']

        if len(name) < 2:
            raise ValidationError('Invalid Tournament Name: name to short.')

        return name

    num_rounds = forms.IntegerField(
        required=True, label="Number of Rounds", initial=1)

    def clean_num_rounds(self):
        """Validate that the number of rounds is a positive integer."""
        num_rounds = self.cleaned_data['num_rounds']
        if num_rounds <= 0:
            raise ValidationError('The number of rounds must be a positive integer.')
        return num_rounds

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Start Date",
        required=True,
        initial=datetime.date.today,
    )

    def clean_start_date(self):
        """Ensure the start date is not in the past."""
        start_date = self.cleaned_data['start_date']
        if start_date < datetime.date.today():
            raise ValidationError('Start date cannot be in the past.')
        return start_date

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="End Date",
        required=True,
        initial=datetime.date.today,
    )

    def clean_end_date(self):
        """Ensure the end date is after the start date."""
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data['end_date']
        if start_date and end_date <= start_date:
            raise ValidationError('End date must be after the start date.')
        return end_date

    pairing_system = PairingSystemField(
        required=True, label="Pairing system used")
    province = ProvinceField(required=True)
    # TournamentOrganizer CFC id
    to_cfc = CfcIdField(
        required=True, label="Tournament Organizer CFC id", initial="111111")

    def clean_to_cfc(self):
        """Validate the CFC ID format for the Tournament Organizer."""
        to_cfc = self.cleaned_data['to_cfc']
        if not to_cfc.isdigit() or len(to_cfc) != 6:
            raise ValidationError('Tournament Organizer CFC ID must be a 6-digit number.')
        return to_cfc

    # TournamentDirector CFC id
    td_cfc = CfcIdField(
        required=True, label="Tournament Director CFC id", initial="222222")

    def clean_td_cfc(self):
        """Validate the CFC ID format for the Tournament Director."""
        td_cfc = self.cleaned_data['td_cfc']
        if not td_cfc.isdigit() or len(td_cfc) != 6:
            raise ValidationError('Tournament Director CFC ID must be a 6-digit number.')
        return td_cfc
