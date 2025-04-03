"""province_fields.py: province Form field's for CFC report builder"""
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

from django import forms


class ProvinceField(forms.ChoiceField):
    """
    A form field for representing Canadian provinces.
    """
    # Maximum allowed length for province code
    PROVINCE_CODE_MAX_LENGTH = 2

    # Mapping of province acronyms to province names
    PROVINCES: dict[str, str] = {
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

    # Constant for choice field options, extracted for clarity
    PROVINCES_CHOICES = PROVINCES.items()

    def __init__(self, *args, **kwargs):
        """
        Initialize the ProvinceField with predefined province choices.
        """
        super().__init__(choices=self.PROVINCES_CHOICES, *args, **kwargs)
