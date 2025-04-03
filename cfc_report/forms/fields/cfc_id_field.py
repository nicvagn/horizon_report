"""
cfc_id_field.py

This module contains custom form field definitions for creating and handling
form fields in the CFC (Custom Form Creator) report builder.

The functionality provided here is focused on facilitating field-related
features specifically designed for the report builder use case.

"""

# Metadata
__author__ = "nrv"
__version__ = "0.0.1"

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
from django.core.validators import MaxValueValidator, MinValueValidator


class CfcIdField(forms.IntegerField):
    """A CFC ID field for validating Canadian Federation Codes.

    Validates that the ID is a 6-digit integer where:
      - 100,000 <= ID <= 999,999 (inclusive).

    Attributes
    ----------
    MIN_VALUE : int
        The minimum value allowed for the CFC ID (inclusive).
    MAX_VALUE : int
        The maximum value allowed for the CFC ID (inclusive).
    DEFAULT_VALIDATORS : list
        default validators applied to the field.
    """
    MIN_VALUE = 100000
    MAX_VALUE = 999999
    DEFAULT_VALIDATORS = [
        MinValueValidator(MIN_VALUE),
        MaxValueValidator(MAX_VALUE)
    ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("validators", self.DEFAULT_VALIDATORS)
        super().__init__(*args, **kwargs)
