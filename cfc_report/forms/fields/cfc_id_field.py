"""
cfc_id_field.pyi - form fields
"""

# Copyright (C) 2025 Nicolas Vaagen
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

from cfc_report.utils.cfc_id_utils import CfcIdValidator


class CfcIdField(forms.CharField):
    """A CFC ID field for validating Canadian Federation id.

    Validates that the ID is a 6-digit integer

    Attributes
    ----------
    default_validators : list
        List of validators applied to the field. Contains CfcIdValidator.
    widget : TextInput
        The widget used for rendering the field.
    error_messages : dict
        Custom error messages for validation failures.
    """
    default_validators = [CfcIdValidator()]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', forms.TextInput(
            attrs={'maxlength': '6', 'pattern': r'\d{6}'}))
        kwargs.setdefault('max_length', 6)
        kwargs.setdefault('min_length', 6)
        kwargs.setdefault('error_messages', {
            'invalid': 'Enter a valid CFC ID (6 digits)',
            'required': 'CFC ID is required',
            'max_length': 'CFC ID must be exactly 6 digits',
            'min_length': 'CFC ID must be exactly 6 digits',
        })
        super().__init__(*args, **kwargs)
