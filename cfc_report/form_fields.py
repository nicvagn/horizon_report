"""form_fields.py: Form field's for CFC report builder"""
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
from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms


class CfcIdField(forms.IntegerField):
    """A CFC ID field

    Attributes
    ----------
    validators :
        int in field x must be x where 1000000 > x > 99999
    """

    def __init__(self, *args, **kwargs):
        kwargs["label"] = "CFC id"
        kwargs["validators"] = [MinValueValidator(
            100000), MaxValueValidator(999999)]
        super().__init__(*args, **kwargs)


class PairingSystemField(forms.ChoiceField):
    """A tournament pairing system for a chess tournament

    Attributes
    ----------
    PAIRING_SYSTEM : dict{str:str}
        Pairing system for the tournament
    """
    PAIRING_SYSTEMS = {
        "SW": "Swiss",
        "RR": "Round Robin",
        "DR": "Double Round Robin",
    }

    def __init__(self, *args, **kwargs):
        kwargs["choices"] = self.PAIRING_SYSTEMS
        kwargs["label"] = "Pairing System"
        super().__init__(*args, **kwargs)


class ProvinceField(forms.ChoiceField):
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
        kwargs["choices"] = self.PROVINCES
        kwargs["label"] = "Province"
        super().__init__(*args, **kwargs)
