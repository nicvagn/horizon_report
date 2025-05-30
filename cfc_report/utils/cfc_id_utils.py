"""Helpers for CFC ID etc"""
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

import re

from django.core.validators import RegexValidator


def is_cfc_id_valid(cfc_id: str | int) -> bool:
    """Validates whether the provided CFC ID is a 6-digit numeric identifier.

    Parameters
    ----------
    cfc_id : str | int
        The CFC ID, this is a 6-char string of digits.

    Returns
    -------
    bool
        True if valid, False otherwise.
    """
    return bool(re.match(r'^\d{6}$', str(cfc_id)))


class CfcIdValidator(RegexValidator):
    """Validates whether the provided CFC ID is a 6-digit numeric identifier."""

    def __init__(self):
        super().__init__(
            regex=r'^\d{6}$',
            message='CFC ID must be a 6-digit number.',
            code='invalid_cfc_id'
        )
