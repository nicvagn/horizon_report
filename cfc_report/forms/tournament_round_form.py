"""tournament_round_form.py: Round Form for CFC rated tournament"""
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

from django import forms


class TournamentRoundForm(forms.Form):
    """for getting info on a CFC rated tournament

    Attributes
    ----------

    """

    round_number = forms.IntegerField(
        required=True, label="Round Number", initial=1)

