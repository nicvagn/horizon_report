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

from cfc_report.utils.cfc_id_utils import is_cfc_id_valid
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
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        label="Start Date",
        required=True,
        initial=datetime.date.today().strftime('%Y-%m-%d'),
    )

    def clean_start_date(self):
        """Ensure the start date is not in the past, and format it into an
        ISO 8601 string."""
        start_date = self.cleaned_data['start_date']

        if start_date < datetime.date.today():
            raise ValidationError('Start date cannot be in the past.')

        # DateTime obj are not json serializable
        return start_date.isoformat()

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        label="End Date",
        required=True,
        initial=datetime.date.today().strftime("%Y-%m-%d"),
    )

    def clean_end_date(self):
        """Validate that the end date occurs after the start date, and format it
            into an ISO 8601 string.
        """
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data['end_date']
        if start_date and datetime.date.fromisoformat(start_date) > end_date:
            raise ValidationError('End date must be <= the start date.')
        return end_date.isoformat()

    pairing_system = PairingSystemField(
        required=True, label="Pairing system used")

    def clean_pairing_system(self):
        """ensure pairing system is valid"""
        pairing_system = self.cleaned_data['pairing_system']
        if pairing_system not in PairingSystemField.PAIRING_SYSTEM_CHOICES.keys():
            raise ValidationError('Invalid pairing system.')
        return pairing_system

    province = ProvinceField(required=True)

    def clean_province(self):
        """ensure province system is valid"""
        province = self.cleaned_data['province']
        if province not in ProvinceField.PROVINCES.keys():
            raise ValidationError('Invalid province.')
        return province

    # TournamentOrganizer CFC id
    to_cfc = CfcIdField(
        required=True, label="Tournament Organizer CFC id", initial="111111")

    def clean_to_cfc(self):
        """Validate the CFC ID format for the Tournament Organizer."""
        to_cfc = self.cleaned_data['to_cfc']

        if not is_cfc_id_valid(to_cfc):
            raise ValidationError('Tournament Organizer CFC ID must be a 6-digit number.')
        return to_cfc

    # TournamentDirector CFC id
    td_cfc = CfcIdField(
        required=True, label="Tournament Director CFC id", initial="222222")

    def clean_td_cfc(self):
        """Validate the CFC ID format for the Tournament Director."""
        td_cfc = self.cleaned_data['td_cfc']

        if not is_cfc_id_valid(td_cfc):
            raise ValidationError('Tournament Director CFC ID must be a 6-digit number.')
        return td_cfc
