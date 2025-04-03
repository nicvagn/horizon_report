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

from django import forms


class PairingSystemField(forms.ChoiceField):
    """A tournament pairing system field for a chess tournament.

    Attributes
    ----------
    PAIRING_SYSTEM_CHOICES : dict[str, str]
        Defines the available pairing system codes and their corresponding names.
    """
    PAIRING_SYSTEM_CHOICES = {
        "SW": "Swiss",
        "RR": "Round Robin",
        "DR": "Double Round Robin",
    }

    def __init__(self, *args, **kwargs):
        kwargs["choices"] = self.PAIRING_SYSTEM_CHOICES.items()
        super().__init__(*args, **kwargs)
