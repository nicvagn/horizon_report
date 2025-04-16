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

from cfc_report.models import Round, Tournament


class RoundForm(forms.ModelForm):
    """
    A form for creating or updating a Round instance.
    """

    class Meta:
        model = Round
        fields = ["tournament", "round_num"]
        labels = {
            "tournament": "Tournament",
            "round_num": "Round Number",
        }
        widgets = {
            "tournament": forms.Select(attrs={"class": "form-control"}),
            "round_num": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter round number",
                "min": 1
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate tournament options
        self.fields["tournament"].queryset = Tournament.objects.all()
